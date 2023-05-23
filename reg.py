from lib.geo_randomizer_polygon import get_points, group_id_list
import configparser
from core.check import *
from core.sms_code import *
from core.tinder_login import *
from core.google_auto import *


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


def input_dialog(func, text, *args):
    """User interface"""
    h = input(text)
    match h:
        case "re":
            func(*args)
        case "skip":
            continue_var = True
            return continue_var
        case "next":
            pass
        case _:
            print("Wrong input, try again")
            input_dialog(func, *args)

def new_session(session_name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password, latitude, longitude, port, city, group_ids):
    """Creating new session"""
    global profile_id
    profile_id = create_profile(session_name=session_name, port=port)
    time.sleep(2)
    update_profile_proxy(profile_id=str(profile_id), proxy_port=proxy_port, proxy_username=proxy_username,
                         proxy_host=proxy_host,
                         proxy_password=proxy_password, proxy_type=proxy_type, port=str(port))
    latitude, longitude = get_points(city)
    update_profile_geo(profile_id, latitude, longitude, port)
    time.sleep(2)
    driver = create_driver(profile_id, port)
    time.sleep(1)
    update_profile_group(profile_id=str(profile_id), port=port, group_id=group_ids)
    rename(port, profile_id, session_name, group_ids)
    return driver

def start_session(port, city, group_id):
    """Starting session"""
    global group_ids
    global session_name
    email, password, reserve = parse_gmail("res/gmail.xlsx")
    latitude, longitude = get_points(city)
    group_ids = group_id_list(group_id, port)
    session_name = parse_line("res/session_names")
    photos_folder = scan_photos_id(session_name)
    proxy_host = "proxy.soax.com"
    proxy_type = "SOCKS"
    proxy_username = "rUfgRb6QMNgjiLYv"
    proxy_password = "wifi;fr;;;paris"
    ports = ["9266", "9267", "9268", "9269", "9270", "9271", "9272", "9273", "9274", "9275",
                "9276", "9277", "9278", "9279", "9280", "9281", "9282", "9283", "9284", "9285",
                "9286", "9287", "9288", "9289", "9290", "9291", "9292", "9293", "9294", "9295",
                "9296", "9297", "9298", "9299", "9300", "9301", "9302", "9303", "9304", "9305",
                "9306", "9307", "9308", "9309", "9310", "9311", "9312", "9313", "9314", "9315",
                "9316", "9317", "9318", "9319", "9320", "9321", "9322", "9323", "9324", "9325",
                "9326", "9327", "9328", "9329", "9330", "9331", "9332", "9333", "9334", "9335",
                "9336", "9337", "9338", "9339", "9340", "9341", "9342", "9343", "9344", "9345",
                "9346", "9347", "9348", "9349", "9350", "9351", "9352", "9353", "9354", "9355",
                "9356", "9357", "9358", "9359", "9360", "9361", "9362", "9363", "9364", "9365"]
    proxy_port = ports[random.randint(0,99)]
    driver = new_session(session_name, proxy_host, proxy_port, proxy_type, proxy_username, proxy_password, latitude,
                         longitude, port, city, group_ids)
    return email, password, reserve, driver, photos_folder

def rename(port, profile_id, session_name, group_ids):
    session_rename = session_name + " !reg"
    update_profile(port=port, session_rename=session_rename, profile_id=profile_id, group_id=group_ids)


def reg():
    check()
    for i in range(1000):
        try:
            print(f"ITERATION NUMBER: {i}")
            """Parsing account information and creating session"""
            try:
                email, password, reserve, driver, photos_folder = start_session(port, city, group_id)
            except:
                print("Ошибка при создании сессии, проверь EXEL файл, возможно он открыт")
                time.sleep(0.5)
                input("Если проверил, и всё закрыто, нажми ENTER для перезпуска")
                email, password, reserve, driver, photos_folder = start_session(port, city, group_id)

            """Log in into your google account"""
            try:
                google_auth(driver, email, password, reserve)
            except:
                try:
                    time.sleep(1)
                    google_auth(driver, email, password, reserve)
                except:
                    traceback.print_exc()
                    continue_var = input_dialog(google_auth, "Ошибка при входе в гугл аккаунт   ", driver, email, password, reserve)
                    if continue_var:
                        continue

            """Log in into tinder account"""
            try:
                login_in_tinder(driver)
            except:
                traceback.print_exc()
                continue_var = input_dialog(login_in_tinder, "Ошибка при входе в тиндер   ", driver)
                if continue_var:
                    continue
            finally:
                driver.switch_to.window(driver.window_handles[0])

            time.sleep(15)

            """Submiting your phone number"""
            try:
                sms_registration(driver)
            except:
                traceback.print_exc()
                continue_var = input_dialog(sms_registration, "Ошибка при вводе номера   ", driver)
                if continue_var:
                    continue

            """Creating profile"""
            try:
                model_profile(driver)
            except:
                traceback.print_exc()
                continue_var = input_dialog(model_profile, "Ошибка при заполнении анкеты   ", driver, photos_dir, photos_folder)
                if continue_var:
                    continue
            try:
                photos_fold(driver, photos_dir, photos_folder)
            except:
                traceback.print_exc()
                continue_var = input_dialog(photos_fold, "Ошибка при загрузки фото   ", driver, photos_dir, photos_folder)
                if continue_var:
                    continue
            try:
                model_profile_2(driver)
            except:
                traceback.print_exc()
                continue_var = input_dialog(model_profile_2, "Ошибка при заполнении анкеты   ", driver, photos_dir, photos_folder)
                if continue_var:
                    continue

            time.sleep(10)
            """Allowing notifications"""
            try:
                try:
                    driver.find_element(By.XPATH, "//div[@class='l17p5q9z'][normalize-space()='Allow']").click()
                except:
                    driver.find_element(By.XPATH, "(//div[contains(text(),'Allow')])[1]").click()
                time.sleep(2)
                try:
                    driver.find_element(By.XPATH, "//div[@class='l17p5q9z'][normalize-space()='Enable']").click()
                except:
                    driver.find_element(By.XPATH, "//div[contains(text(),'Enable')]").click()
                time.sleep(3)
            except:
                h = input("Отправьте мне любой символ после регистрации   ")

            """Exception section"""
        except Exception:
            traceback.print_exc()
            continue
        finally:
            rename(port, profile_id, session_name, group_ids)
            try:
                driver.quit()
            except:
                traceback.print_exc()
                h = input("Close Driver and press enter")


if password == 'GwLbQhUY':
    reg()
else:
    print("Ты лох, пароль не верный.")