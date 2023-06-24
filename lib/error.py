import time

from core.check import baned
from lib.ban_dispatcher import ban_dp
from lib.text import info
from selenium.webdriver.common.by import By
import traceback, inspect
from lib.info import *
from lib import *


class LoginError:
    def __init__(self):
        self.error_messages = {
            105: "105 - Ошибка поиска элемента",
            110: "110 - Ошибка ввода данных",

        }

    def handle_error(self, error_code):
        return self.error_messages.get(error_code, "404 - Неизвестная ошибка")


def handle_error_click_lock(driver, xpath, error_code):
    retry = True
    while retry:
        try:
            element = driver.find_element(By.XPATH, xpath)
            element.click()
            retry = False
        except Exception:
            error = LoginError()
            print(error.handle_error(error_code))
            retry = False


def clicker(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)
    element.click()


def sender(driver, xpath, key):
    element = driver.find_element(By.XPATH, xpath)
    element.clear()
    element.send_keys(key)


def finder(driver, xpath):
    element = driver.find_element(By.XPATH, xpath)


def timer(t_func, *args, **kwargs):
    for i in range(30):
        time.sleep(0.5)
        try:
            result = t_func(*args, **kwargs)
            break
        except Exception as e:
            # print(i)   #debug
            pass

    return result


def timer2(t_func, *args, **kwargs):
    for i in range(30):
        time.sleep(0.5)
        try:
            result = t_func(*args, **kwargs)
            return result
        except Exception as e:
            # print(i)   #debug
            pass

    return result


def error_handler(func_name):
    def decorate(func):
        def wrapper(*args, **kwargs):
            global flag
            while True:
                try:

                    return func(*args, **kwargs)
                except Exception as e:
                    error_traceback = traceback.format_exc()
                    flag = True
                    if func_name == "starter":
                        log_dispatcher.info(to_write='critical error when creating a session\n' + error_traceback)
                        print(RED + BOLD + "Крит при создании сессии." + RESET)

                        time.sleep(2)
                        print(YELLOW + "Начинаю попытку создания новой сессии..." + RESET)
                        time.sleep(2)
                        flag = False
                        continue
                    if func_name == "google_auth":
                        log_dispatcher.info(to_write='Google authorization error\n' + error_traceback)
                        print(BOLD + DARK_YELLOW + "Ошибка Google авторизации (info - для подробностей)" + RESET)
                        flag = True
                    elif func_name == "login_in_tinder":
                        log_dispatcher.info(to_write='Tinder authorization error\n' + error_traceback)
                        print(BOLD + DARK_YELLOW + "Ошибка при входе в тиндер (info - для подробностей)" + RESET)
                        if not baned(ban_dp.get_driver):
                            log_dispatcher.info(to_print='Аккаунт забанен, исправляю', to_write='Account is banned')
                            ban_dp.set_status('Ban')
                            break
                    elif func_name == "sms_registration":
                        if not baned(ban_dp.get_driver):
                            log_dispatcher.info(to_print='Аккаунт забанен, исправляю', to_write='Account is banned')
                            ban_dp.set_status('Ban')
                            break
                        log_dispatcher.info(to_write='SMS registration error\n' + e)
                        print(BOLD + DARK_YELLOW + "Ошибка СМС регистрации (info - для подробностей)" + RESET)
                    elif func_name == "model_profile":
                        log_dispatcher.info(to_write='Error in block 5.1\n' + e)

                        if not baned(ban_dp.get_driver):
                            log_dispatcher.info(to_print='Аккаунт забанен, исправляю', to_write='Account is banned')
                            ban_dp.set_status('Ban')
                            break
                        print(BOLD + DARK_YELLOW + "Ошикба в блоке 5.1 (info - для подробностей)" + RESET)
                    elif func_name == "photos_fold":
                        if not baned(ban_dp.get_driver):
                            log_dispatcher.info(to_print='Аккаунт забанен, исправляю', to_write='Account is banned')
                            ban_dp.set_status('Ban')
                            break
                        log_dispatcher.info(to_write='Error in block 5.2\n' + error_traceback)
                        print(BOLD + DARK_YELLOW + "Ошикба в блоке 5.2 (info - для подробностей)" + RESET)
                    elif func_name == "model_profile_2":
                        if not baned(ban_dp.get_driver):
                            log_dispatcher.info(to_print='Аккаунт забанен, исправляю', to_write='Account is banned')
                            ban_dp.set_status('Ban')
                            break
                        log_dispatcher.info(to_write='Error in block 5.3\n' + error_traceback)
                        print(BOLD + DARK_YELLOW + "Ошикба в блоке 5.3 (info - для подробностей))" + RESET)
                    elif func_name == "end_registr":
                        log_dispatcher.info(to_write='Error in block 5.4\n' + error_traceback)
                        print(BOLD + DARK_YELLOW + "Ошикба в блоке 5.4" + RESET)
                    else:
                        log_dispatcher.info(to_write='Unknown error\n' + error_traceback)
                        print("404 Error")

                    if flag:
                        continue_var = input_dialog(func,
                                                    YELLOW + f"Для продолжения регистрации введите команду: " + RESET)
                        if continue_var == "re":
                            continue
                        elif continue_var == "skip":
                            # return
                            raise StopIteration
                        elif continue_var == "next":
                            break
                        elif continue_var == "10":
                            print("Всегда помни Десятое правило")
                            continue
                        elif continue_var == "ку":
                            print(BOLD + RED + "КУ-КУ Блядь." + RESET)
                        elif continue_var == "info":
                            info()
                        else:
                            print(LIGRED + "Неверный ввод, попробуйте снова." + RESET)

        return wrapper

    return decorate


def input_dialog(func, text):
    while True:
        user_input = input(text)
        log_dispatcher.info(to_write=f'Input command in 173 line error.py: {user_input}')
        if user_input in ["re", "skip", "next", "10", "ку", "info"]:
            return user_input
        else:
            print("Неверный ввод, попробуйте снова.")
