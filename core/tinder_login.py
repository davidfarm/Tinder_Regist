import time, traceback, configparser, random
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.file_detector import UselessFileDetector
from lib.info import *
from lib.error import *

russian_female_names_en = ['Anastasia', 'Maria', 'Daria', 'Yulia', 'Anna', 'Ekaterina', 'Olga', 'Natalia', 'Elena',
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
russian_female_names_ru = ['Александра', 'Алена', 'Алина', 'Алиса', 'Алла', 'Анастасия', 'Ангелина', 'Анна', 'Арина',
                           'Валентина', 'Валерия', 'Варвара', 'Вера', 'Вероника', 'Виктория', 'Галина', 'Дарья', 'Ева',
                           'Евгения', 'Екатерина', 'Елена', 'Елизавета', 'Жанна', 'Злата', 'Инна', 'Ирина', 'Карина',
                           'Кира', 'Кристина', 'Ксения', 'Лариса', 'Лидия', 'Любовь', 'Людмила', 'Маргарита', 'Марина',
                           'Мария', 'Мила', 'Милана', 'Милена', 'Надежда', 'Наталья', 'Нина', 'Оксана', 'Олеся',
                           'Ольга', 'Полина', 'Раиса', 'Светлана', 'София', 'Тамара', 'Татьяна', 'Ульяна', 'Юлия',
                           'Яна', 'Ярослава', 'Агата', 'Агнесса', 'Алевтина', 'Алима', 'Алла', 'Альбина', 'Амалия',
                           'Анисья', 'Ариадна', 'Валентина', 'Валерия', 'Василиса', 'Вера', 'Вероника', 'Влада',
                           'Владислава', 'Галина', 'Дарина', 'Диана', 'Дина', 'Евгения', 'Екатерина', 'Елена',
                           'Елизавета', 'Жанна', 'Зарина', 'Зоя', 'Инга', 'Инесса', 'Ия', 'Камилла', 'Каролина',
                           'Кира', 'Клавдия', 'Кристина', 'Леся', 'Майя', 'Маргарита', 'Марина', 'Мирослава',
                           'Надежда', 'Наталья', 'Оксана', 'Ольга', 'Полина', 'Роза']
european_female_names_en = ['Emma', 'Olivia', 'Ava', 'Isabella', 'Sophia', 'Mia', 'Charlotte', 'Amelia', 'Harper',
                         'Evelyn', 'Abigail', 'Emily', 'Elizabeth', 'Mila', 'Ella', 'Avery', 'Sofia', 'Camila',
                         'Luna', 'Scarlett', 'Victoria', 'Penelope', 'Grace', 'Chloe', 'Layla', 'Zoey', 'Mila',
                         'Aria', 'Lily', 'Hannah', 'Lillian', 'Addison', 'Eleanor', 'Natalie', 'Liam', 'Aubrey',
                         'Stella', 'Savannah', 'Brooklyn', 'Leah', 'Zoe', 'Audrey', 'Samantha', 'Claire', 'Naomi',
                         'Eva', 'Scarlett', 'Lucy', 'Anna', 'Sofia', 'Elena', 'Layla', 'Gabriella', 'Faith', 'Violet',
                         'Mackenzie', 'Madison', 'Katherine', 'Julia', 'Alexa', 'Ruby', 'Alice', 'Kylie', 'Catherine',
                         'Bella', 'Kinsley', 'Alexandra', 'Alexis', 'Kaylee', 'Stella', 'Lucy', 'Anna', 'Savannah',
                         'Sarah', 'Victoria', 'Julia', 'Maria', 'Willow', 'Gianna', 'Liliana', 'Ellie', 'Hailey',
                         'Madeline', 'Adeline', 'Brooklyn', 'Alexa', 'Sadie', 'Josephine', 'Aria', 'Emilia', 'Autumn',
                         'Quinn', 'Nevaeh', 'Piper', 'Ruby', 'Serena', 'Serenity', 'Savannah', 'Naomi', 'Nora', 'Nova']
russian_male_names_en = ['Alexander', 'Alexey', 'Anatoly', 'Andrey', 'Anton', 'Arkady', 'Arseny', 'Artem', 'Boris',
                         'Vadim', 'Valentin', 'Valery', 'Vasily', 'Victor', 'Vitaly', 'Vladimir', 'Vladislav',
                         'Vyacheslav', 'Gennady', 'George', 'Gleb', 'Gregory', 'Daniel', 'Denis', 'Dmitry', 'Eugene',
                         'Yegor', 'Ivan', 'Igor', 'Ilya', 'Konstantin', 'Leo', 'Leonid', 'Maxim', 'Marat', 'Mark',
                         'Mikhail', 'Nikita', 'Nikolay', 'Oleg', 'Pavel', 'Peter', 'Roman', 'Ruslan', 'Semen', 'Sergei',
                         'Stanislav', 'Timur', 'Fedor', 'Yuri', 'Yaroslav']
russian_male_names_ru = ['Александр', 'Алексей', 'Анатолий', 'Андрей', 'Антон', 'Аркадий', 'Арсений', 'Артем', 'Борис',
                         'Вадим', 'Валентин', 'Валерий', 'Василий', 'Виктор', 'Виталий', 'Владимир', 'Владислав',
                         'Вячеслав', 'Геннадий', 'Георгий', 'Глеб', 'Григорий', 'Даниил', 'Денис', 'Дмитрий', 'Евгений',
                         'Егор', 'Иван', 'Игорь', 'Илья', 'Константин', 'Лев', 'Леонид', 'Максим', 'Марат', 'Марк',
                         'Михаил', 'Никита', 'Николай', 'Олег', 'Павел', 'Петр', 'Роман', 'Руслан', 'Семен', 'Сергей',
                         'Станислав', 'Тимур', 'Федор', 'Юрий', 'Ярослав']
european_male_names_en = ['Alexander', 'Alex', 'Andrew', 'Anthony', 'Arthur', 'Benjamin', 'Blake', 'Charles',
                          'Christopher', 'Daniel', 'David', 'Edward', 'Ethan', 'Gabriel', 'George', 'Henry', 'Isaac',
                          'Jacob', 'James', 'John', 'Jonathan', 'Joseph', 'Joshua', 'Liam', 'Lucas', 'Matthew',
                          'Michael', 'Nathan', 'Nicholas','Noah', 'Oliver', 'Patrick', 'Paul', 'Robert', 'Ryan',
                          'Samuel', 'Sean', 'Steven', 'Thomas', 'Teo','Timothy', 'Tyler', 'Victor', 'Vincent',
                          'William', 'Xavier', 'Zachary', 'Kevin', 'Richard', 'Eduard']

config = configparser.ConfigParser()
config.read('config.ini')
reg_variable = config.get('Settings', 'reg_variable')
name_variation = config.get('Settings', 'name_variation')

@error_handler("login_in_tinder")
def login_in_tinder(driver):
    """Logining in Tinder"""
    time.sleep(1)
    driver.get("https://tinder.com")
    try:
        timer(handle_error_click, driver, "//div[@class='D(f)--ml']//div[1]//button[1]//div[2]//div[2]", 105)
    except:
        pass
    timer(driver.find_element, By.CSS_SELECTOR, "a[class='c1p6lbu0 Miw(120px)'] div[class='l17p5q9z']").click()
    time.sleep(2)
    try:
        timer(driver.switch_to.frame, driver.find_element(By.TAG_NAME, "iframe"))
    except:
        time.sleep(5)
        timer(driver.switch_to.frame, driver.find_element(By.TAG_NAME, "iframe"))
    try:
        timer(handle_error_click, driver, "/html[1]/body[1]", 105)
    except:
        timer(handle_error_click, driver, "//span[@class='nsm7Bb-HzV7m-LgbsSe-BPrWId']", 105)
    timer(driver.switch_to.window, driver.window_handles[1])
    try:
        timer(handle_error_click, driver, "//div[contains(@class,'fFW7wc-ibnC6b-sM5MNb TAKBxb')]//div[@class='fFW7wc-ibnC6b']", 105)
    except:
        timer(handle_error_click, driver, "//div[contains(@class,'fFW7wc-ibnC6b-sM5MNb TAKBxb')]//div[@class='fFW7wc-ibnC6b']", 105)
    try:
        timer(handle_error_click, driver, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[3]/div[1]", 105)
    except:
        pass
    try:
        driver.switch_to.window(driver.window_handles[0])
    except:
        traceback.print_exc()
        pass

@error_handler("photos_fold")
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
    ret = True
    for ph_id in photos_path:
        ph_id1 = os.path.abspath(ph_id)
        timer(driver.find_element, By.XPATH, "//input[@type='file']").send_keys(ph_id1)
        while True:
            if ret:
                try:
                    timer(driver.find_element, By.CSS_SELECTOR,
                          "button[class='c1p6lbu0'] div[class='l17p5q9z']").click()  #new interface
                    break
                except:
                    ret = False
            else:
                try:
                    timer(handle_error_click, driver,
                          "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[2]/div[2]/div[2]", 105)
                    break
                except:
                    break


"""Java распаковка"""
#   file_input = driver.find_element(By.XPATH, "//input[@type='file']")
#   file_path = r"C:\Users\Мерлин\Мой диск\Мерлин\photo_2022-11-28_20-29-13.jpg"
#   driver.execute_script("arguments[0].setAttribute('value', arguments[1]);", file_input, file_path)
@error_handler("model_profile")
def model_profile(driver):
    """Creation of Tinder profile"""
    try:
        timer(handle_error_click, driver, "//div[contains(text(),'I agree')]", 105)
    except:
        pass
    time.sleep(1)
    if name_variation == 'european':
        female_name = european_female_names_en[random.randint(0, 99)]
        male_name = european_male_names_en[random.randint(0, 49)]
    elif name_variation == 'slavic_ru':
        female_name = russian_female_names_ru[random.randint(0, 99)]
        male_name = russian_male_names_ru[random.randint(0, 49)]
    elif name_variation == 'slavic_en':
        female_name = russian_female_names_en[random.randint(0, 99)]
        male_name = russian_male_names_en[random.randint(0, 49)]
    time.sleep(1)
    timer(handle_error_send_keys, driver, "//input[@placeholder='MM']", random.randint(1, 12), 110)
    timer(handle_error_send_keys, driver, "//input[@placeholder='DD']", random.randint(1, 28), 110)

    if reg_variable == 'female':
        timer(handle_error_send_keys, driver, "//input[@id='name']", female_name, 110)
        timer(handle_error_send_keys, driver, "//input[@placeholder='YYYY']", random.randint(1998, 2003), 110)
        timer(handle_error_click, driver, "//span[normalize-space()='Woman']", 105)
        timer(handle_error_click, driver, "//span[normalize-space()='Men']", 105)
    else:
        timer(handle_error_send_keys, driver, "//input[@id='name']", male_name, 110)
        timer(handle_error_send_keys, driver, "//input[@placeholder='YYYY']", random.randint(1990, 1998), 110)
        timer(handle_error_click, driver, "//span[normalize-space()='Man']", 105)
        timer(handle_error_click, driver, "//span[normalize-space()='Women']", 105)
    time.sleep(1)

@error_handler("model_profile_2")
def model_profile_2(driver):
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 1080)")
    time.sleep(0.5)
    continue_btn = driver.find_element(By.XPATH, "//span[normalize-space()='Continue']")
    continue_btn.location_once_scrolled_into_view
    time.sleep(1)
    try:
        handle_error_click(driver, "(//div[@class='l17p5q9z'])[8]", 105)
    except:
        handle_error_click(driver, "//div[@class='D(f) Fxd(r) Ac(sb) W(100%)']//div[3]//div[1]", 105)
    timer(handle_error_click, driver, "(//button[@role='option'])[3]", 105)
    time.sleep(1)
    try:
        handle_error_click( driver, "//div[contains(text(),'Continue')]", 105)
        try:
            driver.find_element( By.CSS_SELECTOR, "button[type='submit'] div[class='l17p5q9z']").click()
        except:
            driver.find_element(By.XPATH, "//span[normalize-space()='Continue']").click()
    except:
        pass
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, "//span[normalize-space()='Continue']").click()
    except:
        pass


def end_registr(driver):
    try:
        timer(handle_error_click, driver, "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[3]/button[1]/div[2]/div[2]", 105)
        time.sleep(1)
        timer(handle_error_click, driver, "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[3]/button[1]/div[2]/div[2]", 105)
        time.sleep(1)
    except:
        pass

