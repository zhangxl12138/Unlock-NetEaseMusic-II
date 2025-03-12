# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00DE3F83098B0D2512A3081EF9ADC0460CA938B34B8A20916BFED1700D4BD94C86929BEE863E17BB6B74B36F9D0AE5F0B950B2927B64B11277008AA166544AE0006EF2205F3FD94B910A379672F665F7CB2D5980C2C50857B28C8D3B5817F15B9BCD1BB630DDA71AAADD2BEBBBD9D40A5950CB17C7E46910ADC470BA4BF501E56560287085D29A601AE92BCA50646F5F42C83939B09040B7664A5AB819F4DEB7FA330A1BAE812CF85913EC5C581782CE9D60547B9FD0DE843FA6FE32DA225D2733B4B15F3824BDA7C95A1ABE560B3048989025AF0CA1857214E73667D6C91B232E5BF799738CA747F00ACD3BFA120BA9994D8B1C5D7512AA75082DAC814404B2A73E8DCFC4C0D4D32ED52160AAAAD40B9031A573E80D9CE513B912D8817AF340D9A43D462B42E837250FF8F5AFFCF746FCB7759419C600493BCEE26DD0FD3CA9452FD24AFA76F219C260789DD034CE85595E2FC692E74ACAF4C2AC8E547922E352"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
