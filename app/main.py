import json
import re
import time
import traceback

from app import *
from core.check import check, baned
from core.google_auto import google_auth
from core.logger import log_dispatcher, session_dp
from lib.ban_dispatcher import ban_dp
from lib.text import info

run = None


class Registration:
    def __init__(self, log_dispatcher, ban_dp, session_dp):
        self.session_data = None
        self.gmail_check = None
        self.count_email = None
        self.CHANGE_ACCOUNT_SETTINGS = None
        self.REG_VARIABLE = None
        self.GROUP_ID = None
        self.PORT = None
        self.CITY = None
        self.PHOTOS_DIR = None
        self.name_id = None
        self.profile_id = None
        self.group_ids = None
        self.session_name = None
        self.photos_folder = None
        self.driver = None
        self.reserve = None
        self.password = None
        self.email = None
        self.PORT = None

        self.count_ban = 0
        self.count_run_sms_reg = 0

        self.log_dispatcher = log_dispatcher
        self.session_dp = session_dp
        self.log_dispatcher.info(to_write='########################### NEW SESSION ###########################')
        self.count_email = check()  # тут пишется версия проги
        self.ban_dp = ban_dp
        self.PHOTOS_DIR = config_data.get_photos_dir
        self.CITY = config_data.get_city
        self.GROUP_ID = config_data.get_group_id
        self.REG_VARIABLE = config_data.get_reg_variable
        self.CHANGE_ACCOUNT_SETTINGS = config_data.get_change_account
        self.min_age = config_data.get_min_age
        self.max_age = config_data.get_max_age
        self.gmail_check = check_gmail()
        security()
        self.session_count = self.count_email

    def run_start_session(self):

        self.email, self.password, self.reserve, self.driver, self.photos_folder, self.session_name, self.group_ids, \
            self.profile_id, self.name_id, self.PORT = start_session(self.CITY, self.GROUP_ID)
        ban_dp.set_dp(self.driver)

        self.session_data = [self.email, self.password, self.reserve, self.photos_folder, self.session_name, self.group_ids, self.GROUP_ID]
        msg = f"\nID Создаваемой сессии: {self.name_id} ; Осталось зарегистрировать: {self.session_count}\n"
        self.session_count -= 1
        log_dispatcher.info(to_print=msg, to_write=msg + '\n' + str(self.session_data))

    # def add_extension(self):
    #     extension_path = 'extension\\'

    def run_google_auth(self):
        log_dispatcher.info(to_write='run_google_auth')
        try:
            res = google_auth(self.driver, self.email, self.password, self.reserve)
            if res == 'error auth':
                pass
            time.sleep(0.5)
            ban_dp.set_status('Active')

        except PermissionError:
            msg = 'Закрой файл экселя и попробуй снова'
            log_dispatcher.info(to_print=msg, to_write='EXCEPTION!!! exel was not closed\n\n\n', msg_type='error')

    def run_login_tinder(self):
        log_dispatcher.info(to_write='run_login_tinder')
        login_in_tinder(self.driver)
        time.sleep(0.5)
        ban_dp.set_status('Active')

    def run_sms_registration(self):
        log_dispatcher.info(to_write='run_sms_registration')
        time.sleep(5)
        res = sms_registration(self.driver)
        log_dispatcher.info(to_write=f'result sms reg: {res}')
        ban_dp.set_status('Active')

    def run_register(self):
        log_dispatcher.info(to_write='run model_profile')
        model_profile(self.driver)
        time.sleep(0.5)
        ban_dp.set_status('Active')
        log_dispatcher.info(to_write='run photos fold')
        photos_fold(self.driver, self.PHOTOS_DIR, self.photos_folder)
        time.sleep(0.5)
        ban_dp.set_status('Active')
        log_dispatcher.info(to_write='run model_profile2')
        model_profile_2(self.driver)
        time.sleep(0.5)
        ban_dp.set_status('Active')

    def run_end_reg(self):
        log_dispatcher.info(to_write='run end_reg')
        end_registr(self.driver)
        time.sleep(0.5)
        ban_dp.set_status('Active')

    def run_set_preference(self):
        log_dispatcher.info(to_write='run end_reg')
        set_preference(self.driver, self.CHANGE_ACCOUNT_SETTINGS, self.min_age, self.max_age)
        time.sleep(0.5)
        ban_dp.set_status('Active')

    def finalization_invalid_session(self):
        log_dispatcher.info(to_print='Регистрация не завершена, записываю данные сессии...', msg_type='error')
        session_data = {'mail': self.email,
                        'password': self.password,
                        'reserve': self.reserve,
                        'session name': self.session_name,
                        }

        self.session_dp.info(to_write=json.dumps(session_data))
        log_dispatcher.info(to_print='закрываю сессию...', msg_type='error')
        rename(self.PORT, self.profile_id, self.session_name, self.group_ids, is_finaly=False)
        try:
            self.driver.quit()
        except Exception:
            pass

    def __call__(self, *args, **kwargs):
        self.run_google_auth()
        self.run_login_tinder()
        self.run_sms_registration()
        self.run_register()
        self.run_end_reg()
        self.run_set_preference()


class RunAll(Registration):
    def __init__(self, log_dispatcher, ban_dp, session_dp):
        super().__init__(log_dispatcher, ban_dp, session_dp)

        self.all_func = [
            'self.run_start_session',
            'self.run_google_auth',
            'self.run_login_tinder',
            'self.run_sms_registration',
            'self.run_register',
            'self.run_end_reg',
            'self.run_set_preference'
        ]

    def check_end_command(self, i):
        pattern_skip = re.compile(r"skip", re.IGNORECASE)
        pattern_next = re.compile(r"next", re.IGNORECASE)
        pattern_re = re.compile(r"re", re.IGNORECASE)
        pattern_ky = re.compile(r"ку", re.IGNORECASE)
        pattern_exit = re.compile(r"exit", re.IGNORECASE)
        pattern_info = re.compile(r"info", re.IGNORECASE)

        command = input('Ожидаю команду...\n')
        log_dispatcher.info(to_write=f'Input command in 213 line main.py: {command}')

        if pattern_skip.search(command):
            log_dispatcher.info(to_write='ex, input skip, finalization session...')
            self.finalization_invalid_session()
            log_dispatcher.info(to_write='Finalization complete...')
            self.__call__()

        elif pattern_next.search(command):
            self.__call__(i=int(i + 1))

        elif pattern_re.search(command):
            self.__call__(i=i)

        elif pattern_ky.search(command):
            log_dispatcher.info(to_print='Саламалейкум брат')
            self.__call__(i=i)

        elif pattern_exit.search(command):
            log_dispatcher.info(to_print='Закрываю сессию',
                                to_write='ex, exit, finalization session...', msg_type='error')
            self.finalization_invalid_session()
            log_dispatcher.info(to_write='Finalization complete...')
            return

        elif pattern_info.search(command):
            info()
            log_dispatcher.info(to_write='get info')
            self.check_end_command(i)

        else:
            log_dispatcher.info(to_print='Вы ввели не корректную команду',
                                to_write='ex, Uncorrect command, finalization session...', msg_type='error')
            self.check_end_command(i)

    def __call__(self, i=0, *args, **kwargs):

        try:
            for _ in range(self.count_email):
                log_dispatcher.info(to_write=f'len(all_func: {len(self.all_func)})')
                while i < int(len(self.all_func) -1):
                    log_dispatcher.info(to_write=f'i: {i}')
                    eval(f'{self.all_func[i]}()')
                    i += 1
                    log_dispatcher.info(to_write=self.all_func[i])
                    if ban_dp.get_status == 'Ban':
                        if self.count_ban < 2:
                            i = 2
                            self.count_ban += 1
                            ban_dp.set_status('Active')
                            log_dispatcher.info(to_write=f'count_ban: {self.count_ban}')
                        else:
                            log_dispatcher.info(to_print='Этот аккаунт забанен, исправить не получилось',
                                                msg_type='error')
                            raise StopIteration('Account banned, cant fix it')

                # if self.CHANGE_ACCOUNT_SETTINGS:
                self.run_set_preference()
                # self.run_end_reg()
                i = 0
                time.sleep(1)
                log_dispatcher.info(to_print='Аккаунт зарегестрировано!', to_write='Account was created!\n\n\n',
                                    msg_type='error')
                rename(self.PORT, self.profile_id, self.session_name, self.group_ids)
                log_dispatcher.info(to_print='закрываю сессию...', msg_type='error')
                time.sleep(2)
                self.driver.quit()

        except Exception as ex:
            error_traceback = traceback.format_exc()
            msg = f'Коротко об ошибке: \n{ex}\n' \
                  f'Функция: {self.all_func[i]}\n'

            log_dispatcher.info(to_print=msg, to_write=f'EXCEPTION!! {error_traceback}', msg_type='error')
            time.sleep(0.5)

            if self.all_func[i] == 'self.run_sms_registration':
                if self.count_run_sms_reg < 1:
                    self.count_run_sms_reg += 1
                    self.__call__(i=int(i - 1))
                    return
                else:
                    log_dispatcher.info(to_write='Cant fix sms_reg error', msg_type='error')

            self.check_end_command(i)


if __name__ == '__main__':
    # try:
    run = RunAll(log_dispatcher, ban_dp, session_dp)
    run()
    # reg = Registration(log_dispatcher, ban_dp, session_dp)
    # reg.run_start_session()
    # except KeyboardInterrupt:
    #     run.finalization_invalid_session()
    # except Exception as ex:
    #     error_traceback = traceback.format_exc()
    #     log_dispatcher.info(to_write=f'finaly exception:\n'
    #                                  f'{error_traceback}')
