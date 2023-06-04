import time, openpyxl, configparser
from lib.info import *


config = configparser.ConfigParser()
config.read('config.ini')
reg_variable = config.get('Settings', 'reg_variable')
photos_dir = config.get('Settings', 'photos_dir')
port = config.get('Settings', 'port')

RED, BOLD, BLUE, RESET, YELLOW, PURPLE, LIGRED, DARK_YELLOW, CIAN = color()

def check():
    print(YELLOW + BOLD + "Проверка состояния...\n" + RESET)
    time.sleep(0.5)

    if os.path.exists(photos_dir):
        print("Путь в норме \u2705")
    else:
        print("Путь не верный \x1b[31m\x1b[1m✗\x1b[0m")

    time.sleep(0.5)
    try:
        count_email = check_gmail()
        print(f"Кол-во почт в программе: {count_email}")
    except:
        pass

    time.sleep(0.5)
    try:
        filename = 'res/session_names'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                content = f.read()
                num_lines = content.count('\n')
                print(f'Кол-во имен в session_names: {num_lines + 1}')
        else:
            print(f'Файл {filename} не найден.')
    except:
        pass
    time.sleep(0.5)

    url = f'http://127.0.0.1:{port}'
    try:
        requests.get(url, timeout=1)
        print(f'Подключение к порту {port} установлено \u2705')
    except:
        print(f'Подключение к порту {port} не удалось установить \x1b[31m\x1b[1m✗\x1b[0m')
    time.sleep(0.5)

    if reg_variable == "female":
        print("Ты регистрируешь " + RESET + RED + BOLD + "Женские" + RESET + " Аккаунты")
    else:
        print("Ты регистрируешь " + RESET + BLUE + BOLD + "Мужские" + RESET + " Аккаунты")

    val = input("Готов продолжить? Y/N\n")
    while val.lower() != 'y':
        if val.lower() == 'n':
            print("Завершаю работу...")
            time.sleep(4)
            exit()
        val = input("Не пиши херню, вот варианты - Y/N: \n")
    print("Ну что, процесс пошел? Скрещивай пальчики...\n")

    return count_email

