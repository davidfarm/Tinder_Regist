import time, traceback
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.common.by import By


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
