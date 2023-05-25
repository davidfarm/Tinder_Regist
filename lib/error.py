from selenium.webdriver.common.by import By
import traceback, inspect
from core.check import *

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

def handle_error_click(driver, xpath, error_code):
    element = driver.find_element(By.XPATH, xpath)
    element.click()

def error_find_element(driver, xpath,error_code):
    element = driver.find_element(By.XPATH, xpath)

"""time.sleep итератор, чтоб не ждать фиксировано 5 сек, а итерировать при ошибке 5 раз за каждую сек"""


def handle_error_send_keys(driver, xpath, key, error_code):
    element = driver.find_element(By.XPATH, xpath)
    element.clear()
    element.send_keys(key)




def error_handler(func_name):
    def decorate(func):
        def wrapper(*args, **kwargs):
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if func_name == "google_auth":
                        print(BOLD + YELLOW + "Ошибка Google авторизации" + RESET)
                    elif func_name == "login_in_tinder":
                        print(BOLD + YELLOW + "Ошибка при входе в тиндер" + RESET)
                    elif func_name == "sms_registration":
                        print(BOLD + YELLOW + "Ошибка СМС регистрации" + RESET)
                    elif func_name == "model_profile":
                        print(BOLD + YELLOW + "Ошибка первого блока регистрации ()" + RESET)
                    elif func_name == "photos_fold":
                        print(BOLD + YELLOW + "Ошибка второго блока регистрации (ФОТО)" + RESET)
                    elif func_name == "model_profile_2":
                        print(BOLD + YELLOW +"Ошибка третьего блока регистрации ()" + RESET)
                    elif func_name == "end_registr":
                        print(BOLD + YELLOW +"Ошибка завершения регистрации" + RESET)
                    else:
                        print("404 Error")

                    continue_var = input_dialog(func,YELLOW + f"Для продолжения регистрации введите команду: " + RESET)
                    if continue_var == "re":
                        continue
                    elif continue_var == "skip":
                        #return
                        raise StopIteration
                    elif continue_var == "next":
                        break
                    elif continue_var == "10":
                        print("Всегда помни Десятое правило")
                        continue
                    else:
                        print(LIGRED + "Неверный ввод, попробуйте снова." + RESET)
        return wrapper
    return decorate

def input_dialog(func, text):
    while True:
        user_input = input(text)
        if user_input in ["re", "skip", "next", "10"]:
            return user_input
        else:
            print("Неверный ввод, попробуйте снова.")

