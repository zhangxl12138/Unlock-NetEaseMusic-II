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
    browser.add_cookie({"name": "MUSIC_U", "value": "00C194959E266481D533E7A95FA690FA55DD1EC33486B2121C7942B22E27C1D8CFDC80DE0C04F8765D5BE5DFF9C08C52BBC083A188D363D36A45090106F7BFE83411D24EE9890A85194A04AA02A5E33386092E4BC39B8BB19FA2125AD5BE6E16177639954271EF3B3E3EF1132B166C36C360791602B49CCDE7D537CED594338461804D97D644EA7A86F9384E29226B2C161D6DA6AD3741BCDCC17246B368AEB5EE4336B297D597D5E639DACCE9558632456DD73ABDC2731723E4DF55237027D8D15C4BC0BC846363F4FF02AD86E80FA3A1E8649AD5AA8C5DCFDE798240A0648569922DA0FF365A10170515AA3063EA3174315A41F09F27AA4726B7C38213021B1DCB563A64043C5F1B6EB95A85AAC67AADCB418E0ADE3CAB2E5AA378EA866983796DAF6B318DCD8B63F402242669D869BE9093EAD449E837B2E70CA183884EB637595CCA00DF13BA5BEB962AD0F4C252454C9518A58B783B39BBD170AA18819B0A"})
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
