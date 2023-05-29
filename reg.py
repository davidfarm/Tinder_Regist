from core.check import *
from core.sms_code import *
from core.core import *
from core.google_auto import *
from core.tinder_login import *


config = configparser.ConfigParser()

config.read('config.ini')
photos_dir = config.get('Settings', 'photos_dir')
city = config.get('Settings', 'geo')
port = config.get('Settings', 'port')
group_id = config.get('Settings', 'group_id')
reg_variable = config.get('Settings', 'reg_variable')
PASSWORD = 'PASS'

if PASSWORD in os.environ:
    password = os.environ[PASSWORD]
else:
    password = input("Введите пароль: ")

def reg():
    count_email = check()
    for i in range(count_email):
        try:
            email, password, reserve, driver, photos_folder, session_name, group_ids, \
                profile_id, name_id = start_session(port, city, group_id)
            check_gmail = check_gmail()
            print(PURPLE + BOLD + f"\nID Создаваемой сессии: {name_id} ; Осталось зарегистрировать: {check_gmail - 1}\n" + RESET)
            google_auth(driver, email, password, reserve)
            login_in_tinder(driver)
            sms_registration(driver)
            model_profile(driver)
            photos_fold(driver, photos_dir, photos_folder)
            model_profile_2(driver)
            end_registr(driver)
            rename(port, profile_id, session_name, group_ids)
            time.sleep(1)
            driver.quit()
        except StopIteration:
            driver.quit()
            continue
        finally:
            driver.quit()

if password == 'GwLbQhUY':
    reg()
else:
    print("Ты лох, пароль не верный.")