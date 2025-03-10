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
    browser.add_cookie({"name": "MUSIC_U", "value": "005139E9402832955B85535F704E745BAFBED9BE4D39EE9704DEB962EA5A42E1E61CF1EFBB0E10E6ADD3C6E2B6744650A15BF2F3B7C0F3CF7314CEBE73C02D00C0DAC826301D262E430E92EC5C302DD38605148DE429BBE1DE7D6B078DFE369C971F1434F7E277A779B1A6A30E9F913FF814D5C7A35A3B185DF54E2E247A9DB0E1FC9A2689A84994F457FBE96AA6AC00C9E44C785FEF2B99FB167E4E2864C6E1C90D7EAC5B612C24AF7A8EEE6526D7AEDCC4BCDAA6CBFACD0432338C955197978366338D32F46BADD57B6D25E51CCC32A58B5557F143776E9DD6F9196FA5671D9F6B56ABF013B860151644D961A4E59732C1EBE196644E9EF93F091CF752E88BA5740D02B8A4080A5D7A9EFD59C686E5C2BB337EC9714930EC99BF498675928A13020D04D1B274C49E66363F8A849EA3DA774662936AE62CE9EE5054F84B7EFF8AE7CB337ACC2E93303CCDDC3ED4B8174A29E42299FE4DB291D41CD0089B4B48A1"})
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
