# from core import *
from core.config import *
from lib.info import check_gmail, RESET, RED, BOLD, BLUE
from selenium.webdriver.common.by import By

import os
import time
import requests

version = '0.6.4'


def check():
    log_dispatcher.info(to_print=f"Версия программы: {version}", msg_type='error')
    log_dispatcher.info(to_print=f"Проверка состояния...")
    time.sleep(0.5)

    if os.path.exists(config_data.get_photos_dir):
        msg = 'Путь в норме'
        log_dispatcher.info(to_print=msg, to_write=msg)
    else:
        msg = 'Путь не верный'
        log_dispatcher.info(to_print=msg,
                            to_write=f'EXCEPTION!!! File path is not correct!'
                                     f'\nSet path: {config_data.get_photos_dir} \n\n\n',
                            msg_type='error')

    time.sleep(0.5)
    try:
        count_email = check_gmail()
        msg = f'Кол-во почт в программе: {count_email}'
        log_dispatcher.info(to_print=msg, to_write=msg)
    except Exception as ex:
        log_dispatcher.info(to_write=f'\n\n\n{ex}')

    time.sleep(0.5)
    try:
        filename = 'res/session_names'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                content = f.read()
                num_lines = content.count('\n')
                msg = f'Кол-во имен в session_names: {num_lines + 1}'
                log_dispatcher.info(to_print=msg, to_write=msg)
        else:
            msg = f'Файл {filename} не найден.'
            log_dispatcher.info(to_print=msg, to_write=msg, msg_type='error')



    except:
        pass
    time.sleep(0.5)

    if config_data.get_reg_variable == "female":
        print("Ты регистрируешь " + RESET + RED + BOLD + "Женские" + RESET + " Аккаунты")
    else:
        print("Ты регистрируешь " + RESET + BLUE + BOLD + "Мужские" + RESET + " Аккаунты")

    val = input("Готов продолжить? Y/N\n")
    while val.lower() != 'y':
        if val.lower() == 'n':
            log_dispatcher.info(to_print='Завершаю работу...', msg_type='error')
            time.sleep(4)
            exit()
        val = input("Не пиши херню, вот варианты - Y/N: \n")
    msg = 'Ну что, процесс пошел? Скрещивай пальчики...\n'
    log_dispatcher.info(to_print=msg, to_write='Start work')

    return count_email


def check_port_con(port):
    url = f'http://127.0.0.1:{port}/'
    try:
        requests.get(url, timeout=1)
        msg = f'Подключение к порту {port} установлено'
        log_dispatcher.info(to_write=msg)
    except:
        msg = f'Подключение к порту {port} не удалось установить'
        log_dispatcher.info(to_print=msg, to_write=msg, msg_type='error')
    time.sleep(0.5)


def baned(driver):
    try:
        res = driver.find_element(By.XPATH, "//h3[normalize-space()='You Have Been Banned From Tinder']")
        if res:
            return False
    except:
        return "baned", 1
