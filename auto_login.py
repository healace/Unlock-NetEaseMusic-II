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
    browser.add_cookie({"name": "MUSIC_U", "value": "0063D406FFD23ACB3FDC083BE69E97F181EC3CCA6FFF7ECD42AC33DA5DD0D4923B23D7177686875117033CB484688FE54CDCDDA18B4551D045F178A3F7F7FA9822C4C6A14B33892DA293DFFDFA529377CDD6AF08A95092B1604E06FCD74B88A0D8EE0B72AD0FB209E0E1CABF77A1643F7F094B57F2C04BBBD13820C56C8713AA76B03B14244315EC43B7D0C177146B9AF9C05FE67446F7E4AFFE2A6F4D83720D1B12CBC65DB5322B57BFBF0C88D257A2B4A92E2F7878766136A876A2F3245E2D6648D4BD2C35480665B00832A805449CCFF4D112E864AB8FA759505B4530BD101080842F7FD4CC388085081090AA08C6DB74C02C02EE2905F18DC4D1B113B8041A422CBB7B7D0F77004821D158D3537154289C9DAAD53A4986E93BD801230436EBCD3D9772EF4C4BBFC6DB24183E42B7098A041926C6AAE3E43076F31A951482B0B0BCB851245159F8F7B1D16B5A9EC63C785421E5EFBF37A4AEB5C32DC9888558"})
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
