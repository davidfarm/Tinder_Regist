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
    timer(handle_error_send_keys, driver, "//input[@aria-label='OTP code digit 1']", code, 110)
    timer(handle_error_click, driver, "//div[contains(text(),'Continue')]", 105)

    """Проверка на бан"""
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[@class='CenterAlign Fxd(c) M(a)']")
    except:
        pass

