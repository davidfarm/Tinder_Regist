import time, traceback, configparser, os, random
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector
from lib.info import *


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
reg_variable = config.get('Settings', 'reg_variable')

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
