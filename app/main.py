import re
import time
import traceback

from app import *
from core.check import check, baned
from core.google_auto import google_auth
from core.logger import log_dispatcher, session_dp

from lib.ban_dispatcher import ban_dp

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
        self.count_ban = 0
        self.count_run_sms_reg = 0

        self.log_dispatcher = log_dispatcher
        self.session_dp = session_dp
        self.log_dispatcher.info(to_write='########################### NEW SESSION ###########################')
        self.count_email = check()  # тут пишется версия проги
        self.ban_dp = ban_dp
        self.PHOTOS_DIR = config_data.get_photos_dir
        self.CITY = config_data.get_city
        self.PORT = config_data.get_port
        self.GROUP_ID = config_data.get_group_id
        self.REG_VARIABLE = config_data.get_reg_variable
        self.CHANGE_ACCOUNT_SETTINGS = config_data.get_change_account
        self.gmail_check = check_gmail()
        security()
        self.session_count = self.count_email

    def run_start_session(self):

        self.email, self.password, self.reserve, self.driver, self.photos_folder, self.session_name, self.group_ids, \
            self.profile_id, self.name_id = start_session(self.PORT, self.CITY, self.GROUP_ID)
        ban_dp.set_dp(self.driver)
        self.session_data = [self.email, self.password, self.reserve, self.photos_folder, self.profile_id]
        msg = f"\nID Создаваемой сессии: {self.name_id} ; Осталось зарегистрировать: {self.session_count}\n"
        self.session_count -= 1
        log_dispatcher.info(to_print=msg, to_write=msg + '\n' + str(self.session_data))

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
            log_dispatcher.info(to_print=msg, to_write='EXCEPTION!!! exel was not closed\n\n\n')

    def run_login_tinder(self):
        log_dispatcher.info(to_write='run_login_tinder')
        login_in_tinder(self.driver)
        time.sleep(0.5)
        ban_dp.set_status('Active')

    def run_sms_registration(self):
        log_dispatcher.info(to_write='run_sms_registration')
        res = sms_registration(self.driver)
        log_dispatcher.info(to_write=f'result sms reg: {res}')
        ban_dp.set_status('Active')

    # def run_baned(self):
    #     # not work, need test
    #     time.sleep(2)
    #     if baned(self.driver):
    #         log_dispatcher.info(to_write='ACCOUNT IS BANNED')
    #         self.work_status = 'banned'
    #     else:
    #         log_dispatcher.info(to_write='account not banned')
    #         self.work_status = 'is_run'

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
        set_preference(self.driver)

    def finalization_invalid_session(self):
        log_dispatcher.info(to_print='Регистрация не завершена, записываю данные сессии...')
        msg = f'{self.session_data}\n' \
              f'session name: {self.session_name}\n'

        self.session_dp.info(to_write=msg)
        log_dispatcher.info(to_print='закрываю сессию...')
        rename(self.PORT, self.profile_id, self.session_name, self.group_ids)
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


class RunAll(Registration):
    def __init__(self, log_dispatcher, ban_dp, session_dp):
        super().__init__(log_dispatcher, ban_dp, session_dp)

        self.all_func = [
            'self.run_start_session',
            'self.run_google_auth',
            'self.run_login_tinder',
            'self.run_sms_registration',
            'self.run_register',
            'self.run_end_reg'
        ]

    def __call__(self, i=0, *args, **kwargs):
        pattern_skip = re.compile(r"skip", re.IGNORECASE)
        pattern_next = re.compile(r"next", re.IGNORECASE)
        pattern_re = re.compile(r"re", re.IGNORECASE)
        pattern_ky = re.compile(r"ку", re.IGNORECASE)
        try:
            for _ in range(self.count_email):
                log_dispatcher.info(to_write=f'len(all_func: {len(self.all_func)})')
                while i < int(len(self.all_func) - 1):
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
                            log_dispatcher.info(to_print='Этот аккаунт забанен, исправить не получилось')
                            raise StopIteration('Account banned, cant fix it')

                # if self.CHANGE_ACCOUNT_SETTINGS:
                #     self.run_set_preference()
                self.run_end_reg()
                i = 0
                time.sleep(1)
                log_dispatcher.info(to_print='Аккаунт зарегестрировано!', to_write='Account was created!\n\n\n')
                rename(self.PORT, self.profile_id, self.session_name, self.group_ids)
                log_dispatcher.info(to_print='закрываю сессию...')
                time.sleep(2)
                self.driver.quit()

        # except StopIteration:
        #     command = input('Повтори команду...\n')
        #     log_dispatcher.info(to_write=f'Input command in 180 line main.py: {command}')
        #     if pattern_skip.search(command):
        #         log_dispatcher.info(to_write='StopIteration, input skip, finalization session...')
        #         self.finalization_invalid_session()
        #         log_dispatcher.info(to_write='Finalization complete...')
        #         self.__call__()
        #
        #     if pattern_next.search(command):
        #         self.__call__(i=int(i + 1))
        #
        #     if pattern_re.search(command):
        #         self.__call__(i=i)
        #     else:
        #         log_dispatcher.info(to_print='Вы ввели не корректную команду, закрываю сессию',
        #                             to_write='StopIteration, Uncorrect command, finalization session...')
        #         self.finalization_invalid_session()
        #         log_dispatcher.info(to_write='Finalization complete...')
        #         return
        #
        #     time.sleep(1)
        #     log_dispatcher.info(to_print='закрываю сессию...')
        #     rename(self.PORT, self.profile_id, self.session_name, self.group_ids)
        #     self.driver.quit()

        except Exception as ex:
            error_traceback = traceback.format_exc()
            msg = f'Коротко об ошибке: \n{ex}\n' \
                  f'Функция: {self.all_func[i]}\n' \
                  f'Если ты считаешь, что программа отработала неправильно - отправь файл логов и скриншот консоли\n' \
                  f'Так же можешь отправить файл логов после завершения работы скрипта, это будет полезно первое время\n' \
                  f' Обрати внимание, что ошибки типа "Плохая прокси и т.п." на даный момент' \
                  f' не фиксятся\n\n\n'
            log_dispatcher.info(to_print=msg, to_write=f'EXCEPTION!! {error_traceback}')
            time.sleep(0.5)

            if self.all_func[i] == 'self.run_sms_registration':
                if self.count_run_sms_reg < 1:
                    self.count_run_sms_reg += 1
                    self.__call__(i=int(i - 1))
                    return
                else:
                    log_dispatcher.info(to_print='Не удалось в автоматическом режиме исправить ошибку регистрации',
                                        to_write='Cant fix sms_reg error')
            command = input('Ожидаю команду...\n')
            log_dispatcher.info(to_write=f'Input command in 213 line main.py: {command}')

            if pattern_skip.search(command):
                log_dispatcher.info(to_write='ex, input skip, finalization session...')
                self.finalization_invalid_session()
                log_dispatcher.info(to_write='Finalization complete...')
                self.__call__()

            if pattern_next.search(command):
                self.__call__(i=int(i + 1))

            if pattern_re.search(command):
                self.__call__(i=i)

            if pattern_ky.search(command):
                log_dispatcher.info(to_print='Саламалейкум брат')
                self.__call__(i=i)

            else:
                log_dispatcher.info(to_print='Вы ввели не корректную команду, закрываю сессию',
                                    to_write='ex, Uncorrect command, finalization session...')
                self.finalization_invalid_session()
                log_dispatcher.info(to_write='Finalization complete...')
                return


if __name__ == '__main__':
    # try:
    run = RunAll(log_dispatcher, ban_dp, session_dp)
    run()
    # except KeyboardInterrupt:
    #     run.finalization_invalid_session()
    # except Exception as ex:
    #     error_traceback = traceback.format_exc()
    #     log_dispatcher.info(to_write=f'finaly exception:\n'
    #                                  f'{error_traceback}')
