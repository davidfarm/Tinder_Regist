from core import *


@error_handler("sms_registration")
def sms_registration(driver):
    base_flg = True
    while base_flg:
        timer(clicker, driver, "/html[1]/body[1]/div[2]/main[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]")
        country, phone_number, id = get_sms("United Kingdom", "Lithuania", "Sweden", 16, 44, 46, 2, 3, 1)
        try:
            timer(sender, driver, "//input[@placeholder='Search']", country)
        except:
            time.sleep(2)
            driver.find_element(By.TAG_NAME, "input").send_keys(country)
            pass
        timer(clicker, driver, "//div[@role='button']")
        timer(sender, driver, "//input[@name='phone_number']", phone_number)
        timer(clicker, driver, "//div[contains(text(),'Continue')]")
        try:
            timer(clicker, driver, "//div[contains(text(),'Continue')]")
        except:
            pass

        flg = False
        tot = 0
        while not flg:
            for i in range(60):
                tot += i
                time.sleep(1)
                sms = get_code(id)
                code = re.sub('\D', '', sms["status"].strip())
                if code != "":
                    timer(sender, driver, "//input[@aria-label='OTP code digit 1']", code)
                    timer(clicker, driver, "//div[contains(text(),'Continue')]")
                    flg = True
                    flg1 = False
                    break
                else:
                    flg1 = True
                    pass
            while flg1:
                log_dispatcher.info(to_write='sms code not received')
                send = input(YELLOW + f"Код не пришел. Ожидание кода {tot}с. Введите символ для продолжения: " + RESET)
                # if send == "y":
                #     flg = False
                #     base_flg = False
                #     break
                # elif send == "n":
                flg = True
                base_flg = False
                log_dispatcher.info(to_print='Повторяю попытку смс-авторизации, ошибку ниже игнорируй...',
                                    to_write='sms-code not received', msg_type='error')
                raise ValueError
                # elif send == "re":
                #     flg = True
                #     clicker(driver, "//button[normalize-space()='Update Contact Info']")
                #     break
                # else:
                #     log_dispatcher.info(to_print='Не верная команда, команды: y/n', msg_type='error')
            if flg:
                base_flg = False
                break

    """Проверка на бан"""
    try:
        time.sleep(2)
        driver.find_element(By.XPATH, "//div[@class='CenterAlign Fxd(c) M(a)']")
    except:
        pass
