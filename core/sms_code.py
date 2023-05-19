import re, time
from selenium.webdriver.common.by import By
from sms_activate import get_sms, get_code


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
    try:
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[contains(text(),'Continue')]").click()
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
    driver.find_element(By.XPATH, "//input[@aria-label='OTP code digit 1']").send_keys(code)
    time.sleep(3)
    driver.find_element(By.XPATH, "//div[contains(text(),'Continue')]").click()
    time.sleep(5)

    """Проверка на бан"""
    try:
        driver.find_element(By.XPATH, "//div[@class='CenterAlign Fxd(c) M(a)']")
    except:
        pass

