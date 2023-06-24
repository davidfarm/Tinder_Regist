from core import *
from core.config import config_data
from core.dataset import european_female_names_en, european_male_names_en, russian_female_names_ru, \
    russian_male_names_ru, russian_female_names_en, russian_male_names_en


@error_handler("login_in_tinder")
def login_in_tinder(driver):
    """Logining in Tinder"""
    time.sleep(1)
    driver.get("https://tinder.com")
    try:
        timer(clicker, driver, "//div[@class='D(f)--ml']//div[1]//button[1]//div[2]//div[2]")
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
        timer(clicker, driver, "/html[1]/body[1]")
    except:
        timer(clicker, driver, "//span[@class='nsm7Bb-HzV7m-LgbsSe-BPrWId']")
    timer(driver.switch_to.window, driver.window_handles[1])
    try:
        timer(clicker, driver, "//div[contains(@class,'fFW7wc-ibnC6b-sM5MNb TAKBxb')]//div[@class='fFW7wc-ibnC6b']")
    except:
        timer(clicker, driver, "//div[contains(@class,'fFW7wc-ibnC6b-sM5MNb TAKBxb')]//div[@class='fFW7wc-ibnC6b']")
    try:
        timer(clicker, driver, "/html[1]/body[1]/div[1]/div[1]/div[1]/div[1]/main[1]/div[3]/div[1]")
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
    log_dispatcher.info(to_write=f'arguments to search base fold: {photos_dir, photos_folder}')
    base_fold = fold_names(photos_dir, photos_folder)
    log_dispatcher.info(to_write=f'base_fold res = {base_fold}')
    log_dispatcher.info(to_write=f'arguments to search full folder: {photos_dir}\\{base_fold}, {photos_folder}')
    full_folder = fold_names(photos_dir + "\\" + base_fold, photos_folder)

    for true_photo_fold in full_folder:
        if true_photo_fold.startswith(photos_folder):
            print('break')
            break

    # error here

    photos_path = get_photos_path(photos_dir + "\\" + base_fold + '\\' + full_folder)
    time.sleep(1)
    ret = True
    for ph_id in photos_path:
        ph_id1 = os.path.abspath(ph_id)
        timer(driver.find_element, By.XPATH, "//input[@type='file']").send_keys(ph_id1)
        while True:
            if ret:
                try:
                    timer(driver.find_element, By.CSS_SELECTOR,
                          "button[class='c1p6lbu0'] div[class='l17p5q9z']").click()  # new interface
                    break
                except:
                    ret = False
            else:
                try:
                    timer(clicker, driver,
                          "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/button[2]/div[2]/div[2]")
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
        timer(clicker, driver, "//div[contains(text(),'I agree')]")
    except:
        pass
    time.sleep(1)
    if config_data.get_name_variation == 'european':
        female_name = european_female_names_en[random.randint(0, 99)]
        male_name = european_male_names_en[random.randint(0, 49)]
    elif config_data.get_name_variation == 'slavic_ru':
        female_name = russian_female_names_ru[random.randint(0, 99)]
        male_name = russian_male_names_ru[random.randint(0, 49)]
    elif config_data.get_name_variation == 'slavic_en':
        female_name = russian_female_names_en[random.randint(0, 99)]
        male_name = russian_male_names_en[random.randint(0, 49)]
    else:
        female_name = russian_female_names_en[random.randint(0, 99)]
        male_name = russian_male_names_en[random.randint(0, 49)]
    time.sleep(1)
    timer(sender, driver, "//input[@placeholder='MM']", random.randint(1, 12))
    timer(sender, driver, "//input[@placeholder='DD']", random.randint(1, 28))

    if config_data.get_reg_variable == 'female':
        timer(sender, driver, "//input[@id='name']", female_name)
        timer(sender, driver, "//input[@placeholder='YYYY']", random.randint(1998, 2003))
        timer(clicker, driver, "//span[normalize-space()='Woman']")
        timer(clicker, driver, "//span[normalize-space()='Men']")
    else:
        timer(sender, driver, "//input[@id='name']", male_name)
        timer(sender, driver, "//input[@placeholder='YYYY']", random.randint(1990, 1998))
        timer(clicker, driver, "//span[normalize-space()='Man']")
        timer(clicker, driver, "//span[normalize-space()='Women']")
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
        clicker(driver, "(//div[@class='l17p5q9z'])[8]")
    except:
        clicker(driver, "//div[@class='D(f) Fxd(r) Ac(sb) W(100%)']//div[3]//div[1]")
    timer(clicker, driver, "(//button[@role='option'])[3]")
    time.sleep(1)
    try:
        clicker(driver, "//div[contains(text(),'Continue')]")
        try:
            driver.find_element(By.CSS_SELECTOR, "button[type='submit'] div[class='l17p5q9z']").click()
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
        log_dispatcher.info(to_write='end_reg start')
        timer(clicker, driver, "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[3]/button[1]/div[2]/div[2]")
        log_dispatcher.info(to_write='click to allow')
        time.sleep(1)
        timer(clicker, driver, "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[3]/button[1]/div[2]/div[2]")
        log_dispatcher.info(to_write='end_reg finaly')
        time.sleep(1)
    except Exception as e:
        log_dispatcher.info(to_write=f'EXCEPTION RUN END REG: {e}')


def set_preference(driver):
    timer(clicker, driver, "(//div[@class='D(b) Pos(r) Expand Bdrs(50%)'])[1]")

    actions = ActionChains(driver)
    right_slider = driver.find_element(By.XPATH, "(//div[@class='t60fo43'])[2]")
    time.sleep(1)
    left_slider = driver.find_element(By.XPATH, "(//button[@role='slider'])[2]")
    actions.click_and_hold(right_slider).move_by_offset(160, 0).release().perform()
    actions.click_and_hold(left_slider).move_by_offset(40, 0).release().perform()

    timer(clicker, driver, "(//*[name()='path'])[1]")
