import os, configparser, shutil, re, time, traceback, random, sys, openpyxl, socket
from info import *
from selenium.webdriver.common.by import By
from sms_activate import get_sms, get_code
from selenium.webdriver.remote.file_detector import UselessFileDetector
from selenium.webdriver.support.relative_locator import locate_with
from geo_randomizer_polygon import get_points, group_id_list

russian_female_names = ['Anastasia', 'Maria', 'Daria', 'Yulia', 'Anna', 'Ekaterina', 'Olga', 'Natalia', 'Elena',
                        'Irina', 'Alexandra', 'Polina', 'Ksenia', 'Kristina', 'Vera', 'Tatiana', 'Sofiya', 'Alina',
                        'Arina', 'Svetlana', 'Nadezhda', 'Galina', 'Margarita', 'Yana', 'Taisiya', 'Lyudmila', 'Zoya',
                        'Valentina', 'Elizaveta', 'Ulyana', 'Lidiya', 'Viktoriya', 'Yaroslava', 'Yekaterina', 'Mariya',
                        'Yelena', 'Zinaida', 'Raisa', 'Marina', 'Tamara', 'Margarita', 'Inna', 'Alla', 'Sofiya',
                        'Anastasiya', 'Evgeniya', 'Ekaterina', 'Lyubov', 'Irina', 'Angelina', 'Lyudmila', 'Nina',
                        'Alena', 'Tatyana', 'Natalya', 'Anna', 'Kristina', 'Svetlana', 'Darya', 'Sofia', 'Valeriya',
                        'Valentina', 'Kira', 'Marianna', 'Galina', 'Veronika', 'Roza', 'Lubov', 'Anastasia', 'Margarita',
                        'Diana', 'Katya', 'Aurora', 'Yuliya', 'Olga', 'Sofiya', 'Inna', 'Natalia', 'Svetlana', 'Angelina',
                        'Irina', 'Taisiya', 'Anna', 'Yana', 'Elizaveta', 'Polina', 'Kseniya', 'Aleksandra', 'Olivia',
                        'Mariya', 'Eva', 'Sara', 'Lidiya', 'Alina', 'Raisa', 'Victoria', 'Kira', 'Yekaterina', 'Alienor']

russian_male_names = ['Александр', 'Алексей', 'Анатолий', 'Андрей', 'Антон', 'Аркадий', 'Арсений', 'Артем', 'Борис',
    'Вадим', 'Валентин', 'Валерий', 'Василий', 'Виктор', 'Виталий', 'Владимир', 'Владислав', 'Вячеслав', 'Геннадий',
    'Георгий',  'Глеб', 'Григорий', 'Даниил', 'Денис', 'Дмитрий', 'Евгений', 'Егор', 'Иван', 'Игорь', 'Илья',
    'Константин', 'Лев', 'Леонид', 'Максим', 'Марат', 'Марк', 'Михаил', 'Никита', 'Николай', 'Олег', 'Павел',
    'Петр', 'Роман', 'Руслан', 'Семен', 'Сергей', 'Станислав', 'Тимур', 'Федор', 'Юрий', 'Ярослав']

config = configparser.ConfigParser()

config.read('config.ini')
photos_dir = config.get('Settings', 'photos_dir')
dir = config.get('Settings', 'dir')
city = config.get('Settings', 'geo')
port = config.get('Settings', 'port')
group_id = config.get('Settings', 'group_id')
reg_variable = config.get('Settings', 'reg_variable')
PASSWORD = 'PASS'

RED = "\033[31m"
BLUE = "\033[34m"
BOLD = "\033[1m"
RESET = "\033[0m"
YELLOW = "\033[33m"

if PASSWORD in os.environ:
    password = os.environ[PASSWORD]
else:
    password = input("Введите пароль: ")

def google_auth(driver, email, password, reserve):
    """Logining in google account"""
    driver.get(r'https://accounts.google.com/signin/v2/identifier?continue=' + \
               'https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1' + \
               '&flowName=GlifWebSignIn&flowEntry = ServiceLogin')
    #driver.implicitly_wait(15)

    loginBox = driver.find_element(By.XPATH, '//*[@id ="identifierId"]')
    loginBox.send_keys(email)

    time.sleep(3)

    nextButton = driver.find_elements(By.XPATH, '//*[@id ="identifierNext"]')
    nextButton[0].click()

    time.sleep(3)

    passWordBox = driver.find_element(By.XPATH,
        '//*[@id ="password"]/div[1]/div / div[1]/input')
    passWordBox.send_keys(password)

    time.sleep(3)

    nextButton = driver.find_elements(By.XPATH, '//*[@id ="passwordNext"]')
    nextButton[0].click()

    time.sleep(3)

    """Здесь запихнуть проверку на 3 сегмент"""

    try:
        driver.find_element(By.XPATH, "(//div[contains(@role,'link')])[4]").click()
        time.sleep(3)
        reserve_email = driver.find_element(By.XPATH, "//input[@id='knowledge-preregistered-email-response']")
        reserve_email.send_keys(reserve)
        time.sleep(3)
        try:
            next = locate_with(By.TAG_NAME, "button").near(reserve_email)
            time.sleep(2)
            next_elem = driver.find_element(next)
            next_elem.click()
        except:
            driver.find_element(By.CSS_SELECTOR, "button[class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 qIypjc TrZEUc lw1w4b'] span[class='VfPpkd-vQzf8d']").click()
        time.sleep(2)
    except:
        traceback.print_exc()
        pass
    """Верификация через телефон, элемент - кнопка возврата"""
#    driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[2]/div[1]/c-wiz[1]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]/span[1]")

def login_in_tinder(driver):
    """Logining in Tinder"""
    time.sleep(1)
    driver.get("https://tinder.com")
    time.sleep(8)
    try:
        driver.find_element(By.XPATH, "//div[@class='D(f)--ml']//div[1]//button[1]//div[2]//div[2]").click()
    except:
        pass
    driver.find_element(By.CSS_SELECTOR, "a[class='c1p6lbu0 Miw(120px)'] div[class='l17p5q9z']").click()
    time.sleep(10)
    driver.switch_to.frame(driver.find_element(By.TAG_NAME, "iframe"))
    time.sleep(6)
    try:
        driver.find_element(By.XPATH, "//span[@class='nsm7Bb-HzV7m-LgbsSe-BPrWId']").click()
    except:
        driver.find_element(By.XPATH, "/html[1]/body[1]").click()
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(5)
    try:
        driver.find_element(By.XPATH, "//div[contains(@class,'fFW7wc-ibnC6b-sM5MNb TAKBxb')]//div[@class='fFW7wc-ibnC6b']").click()
    except:
        driver.find_element(By.XPATH, "//div[contains(@class,'fFW7wc-ibnC6b-sM5MNb TAKBxb')]//div[@class='fFW7wc-ibnC6b']").click()
    time.sleep(4)
    try:
        driver.find_element(By.XPATH, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[3]/div[1]").click()
    except:
        pass
    try:
        driver.switch_to.window(driver.window_handles[0])
    except:
        traceback.print_exc()
        pass

def registration(driver):
    """Account registration"""
    driver.find_element(By.XPATH, "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]").click()
    country, phone_number, id = get_sms("United Kingdom", "Lithuania", "Sweden", 16, 44, 46, 2, 3, 1)
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(country)
    except:
        driver.find_element(By.TAG_NAME, "input").send_keys(country)
        pass
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[@role='button']").click()
    driver.find_element(By.XPATH, "//input[@name='phone_number']").send_keys(phone_number)
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[contains(text(),'Continue')]").click()
    time.sleep(30)
    sms = get_code(id)
    if sms["message"] == "Waiting for sms":
        driver.find_element(By.XPATH, "//button[normalize-space()='Update Contact Info']").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//input[@name='phone_number']").clear()
        time.sleep(2)
        driver.find_element(By.XPATH,
                            "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]").click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//input[@placeholder='Search']").send_keys(country)
        time.sleep(3)
        driver.find_element(By.XPATH, "//div[@role='button']").click()
        country = phone_number, id = get_sms("United Kingdom", "Lithuania", "Sweden", 16, 44, 46, 2, 1, 1)
        driver.find_element(By.XPATH, "//input[@name='phone_number']").send_keys(phone_number)
        driver.find_element(By.XPATH, "//div[contains(text(),'Continue')]").click()
        time.sleep(30)
        sms = get_code(id)

    code = re.sub('\D', '', sms["status"].strip())
    driver.find_element(By.XPATH, "//input[@aria-label='OTP code digit 1']").send_keys(code)
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[contains(text(),'Continue')]").click()
    time.sleep(5)

    """Проверка на бан"""
    try:
        driver.find_element(By.XPATH, "//div[@class='CenterAlign Fxd(c) M(a)']")
    except:
        pass


def photos_fold(driver, photos_dir, photos_folder):
    time.sleep(1)
    driver.file_detector = UselessFileDetector()
    base_fold = fold_names(photos_dir, photos_folder)
    full_folder = fold_names(photos_dir+"\\"+base_fold[0], photos_folder)
    for true_photo_fold in full_folder:
        if true_photo_fold.startswith(photos_folder):
            break
    photos_path = get_photos_path(photos_dir+"\\"+base_fold[0], true_photo_fold)
    time.sleep(1)
    for ph_id in photos_path:
        ph_id1 = os.path.abspath(ph_id)
        driver.find_element(By.XPATH, "//input[@type='file']").send_keys(ph_id1)
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[contains(text(),'Choose')]").click()
        time.sleep(2)

"""Java распаковка"""
#   file_input = driver.find_element(By.XPATH, "//input[@type='file']")
#   file_path = r"C:\Users\Мерлин\Мой диск\Мерлин\photo_2022-11-28_20-29-13.jpg"
#   driver.execute_script("arguments[0].setAttribute('value', arguments[1]);", file_input, file_path)




def model_profile(driver):
    """Creation of Tinder profile"""
    try:
        driver.find_element(By.XPATH, "//div[contains(text(),'I agree')]").click()
    except:
        pass
    time.sleep(2)
    female_name = russian_female_names[random.randint(0, 99)]
    male_name = russian_male_names[random.randint(0, 49)]
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@placeholder='MM']").send_keys(random.randint(1, 12))
    time.sleep(1)
    driver.find_element(By.XPATH, "//input[@placeholder='DD']").send_keys(random.randint(1, 28))
    time.sleep(1)

    if reg_variable == 'female':
        driver.find_element(By.XPATH, "//input[@id='name']").send_keys(female_name)
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//input[@placeholder='YYYY']").send_keys(random.randint(1998, 2003))
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//span[normalize-space()='Woman']").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//span[normalize-space()='Men']").click()
    else:
        driver.find_element(By.XPATH, "//input[@id='name']").send_keys(male_name)
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//input[@placeholder='YYYY']").send_keys(random.randint(1990, 1998))
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//span[normalize-space()='Man']").click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, "//span[normalize-space()='Women']").click()
    time.sleep(1)


def model_profile_2(driver):
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 1080)")
    time.sleep(2)
    continue_btn = driver.find_element(By.XPATH, "//span[normalize-space()='Continue']")
    time.sleep(2)
    continue_btn.location_once_scrolled_into_view
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[@class='D(f) Fxd(r) Ac(sb) W(100%)']//div[3]//div[1]").click()
    time.sleep(2)
    driver.find_element(By.XPATH, "(//button[@role='option'])[3]").click()
    continue_btn.click()

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

def check():
    if os.path.exists(photos_dir):
        print("Путь в норме \u2705")
    else:
        print("Путь не верный \x1b[31m\x1b[1m✗\x1b[0m")
    time.sleep(0.5)
    try:
        workbook = openpyxl.load_workbook('res/gmail.xlsx')
        worksheet = workbook['Sheet1']
        count = 0
        for cell in worksheet['A2:A' + str(worksheet.max_row)]:
            for row in cell:
                if row.value:
                    count += 1
        print(f"Кол-во почт в программе: {count}")
    except:
        pass
    time.sleep(0.5)
    try:
        filename = 'res/session_names'
        if os.path.isfile(filename):
            with open(filename, 'r') as f:
                content = f.read()
                num_lines = content.count('\n')
                print(f'Кол-во имен в session_names: {num_lines}')
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

def reg():
    """Сделать блок на проверку целосности путей, и вообще на работоспособность, если ошибка, тогда причину ошибки"""
    print(YELLOW + BOLD + "Проверка состояния...\n" + RESET)
    time.sleep(0.5)
    check()
    #val = input("Введите 'con' для продолжения, или 'ext' для завершения")
    val = input("Готов продолжить? Y/N\n")
    while val.lower() != 'y':
        if val.lower() == 'n':
            print("Завершаю работу...")
            time.sleep(4)
            exit()
        val = input("Не пиши херню, вот варианты - Y/N: \n")
    print("Ну что, процесс пошел? Скрещивай пальчики...\n")

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
                registration(driver)
            except:
                traceback.print_exc()
                continue_var = input_dialog(registration, "Ошибка при вводе номера   ", driver)
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
                driver.find_element(By.XPATH, "(//div[contains(text(),'Allow')])[1]").click()
                time.sleep(2)
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