from core.core import start_session, sms_registration, rename
from core.google_auto import google_auth
from core.tinder_login import *
from lib.security import security

config = configparser.ConfigParser()

config.read('config.ini')
photos_dir = config.get('Settings', 'photos_dir')
city = config.get('Settings', 'geo')
port = config.get('Settings', 'port')
group_id = config.get('Settings', 'group_id')
reg_variable = config.get('Settings', 'reg_variable')


version = "0.5.3"


def reg():
    security()
    count_email = check()
    for i in range(count_email):
        try:
            email, password, reserve, driver, photos_folder, session_name, group_ids, \
                profile_id, name_id = start_session(port, city, group_id)
            gmail_check = check_gmail()
            print(PURPLE + BOLD + f"\nID Создаваемой сессии: {name_id} ; Осталось зарегистрировать: {gmail_check}\n" + RESET)
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


reg()