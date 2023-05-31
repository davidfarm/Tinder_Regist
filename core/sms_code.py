import re, time
from selenium.webdriver.common.by import By
from lib.sms_activate import get_sms, get_code
from lib.error import *

@error_handler("sms_registration")
def sms_registration(driver):
    """Account registration"""
    timer(handle_error_click, driver, "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]", 105)
    country, phone_number, id = get_sms("United Kingdom", "Lithuania", "Sweden", 16, 44, 46, 2, 3, 1)
    try:
        timer(handle_error_send_keys, driver, "//input[@placeholder='Search']", country, 110)
    except:
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "input").send_keys(country)
        pass
    timer(handle_error_click, driver, "//div[@role='button']", 105)
    timer(handle_error_send_keys, driver, "//input[@name='phone_number']",phone_number, 110)
    timer(handle_error_click, driver, "//div[contains(text(),'Continue')]", 105)
    try:
        timer(handle_error_click, driver, "//div[contains(text(),'Continue')]", 110)
    except:
        pass

    flg = False
    while not flg:
        for i in range(60):
            time.sleep(1)
            sms = get_code(id)
            code = re.sub('\D', '', sms["status"].strip())
            if code != "":
                timer(handle_error_send_keys, driver, "//input[@aria-label='OTP code digit 1']", code, 110)
                timer(handle_error_click, driver, "//div[contains(text(),'Continue')]", 105)
                flg = True
                flg1 = False
                break
            else:
                flg1 = True
                pass
        while flg1:
            send = input(f"Код не пришел. Ожидание кода {i}с. Для продолжения ожидания введите y")
            if send == "y":
                flg = False
                break
            elif send == "n":
                flg = True
                break
            else:
                print("Не верная команда, команды: y/n")
        if flg:
            break

    """Проверка на бан"""
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[@class='CenterAlign Fxd(c) M(a)']")
    except:
        pass

