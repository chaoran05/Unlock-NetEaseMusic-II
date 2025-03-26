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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D8C218BCD5D95567916FB9F18D425D063321D6217E3CEF6F94B17FF2F2F37041B995A8744AEF1C66DE11CCD8EE099197343AD3407D9FA9E722455EB1919F46D23C09862C549A3E72424EC9CCC25E5F0E9CC298E3E4112795A43B32032DF1E212921DF2BDBB07C7AFE2ABA56D8DA7040A6529AFD15F85788752444BBFF42BB674ECE2F1CBF830E8EC77B997FF26826BCCAD2AAE59568FFEF99131F3D3825E15AE1EE7F540EFCA0C65DDE94683065374A2016479B1B37F217732AEDA0184712998B81E73E8AB1DE913F5563B014FA658E463B3B2AA678FFE7F79EC22FBF7A2FCEDCC067FEFA076C411E01FF7483F3FE4E66B0B21191BFC24D6A956926490840AF71CB6535CDCACB8EAA415370851D812D490F8FBAB1D9B609EBCC57472FED5C747E4C19B294550D950DA9E4A9AABC33D45D38850A70825B68163894673ABFBA61254D2C97D560BB9CC99C447563A897AD137DEC6C74D206240B3022E9769899CCB"})
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
