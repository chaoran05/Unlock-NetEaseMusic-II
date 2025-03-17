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
    browser.add_cookie({"name": "MUSIC_U", "value": "00BC075CEB80F550946768B8984AF518D4AFF8935D2083BD46422B313EB9F4261C055433C6CA51BDB44772AEC3A3F86499FDD31738B359931E3A6AC3DE6726D46B6FEC164E10BF3D95E37F752EDA191F8696BCA4656DF920194936638782A65A112A33B4992C43A4BC64D1729DCC4D28B9ED146C74DCB43854F88DBCE93209F716EF9409429305E7620016A1E11BCC9B9FBBE546D53FA457A50C8F18546BE892598BCF3DAB77D71CC575198747602DA16F4A9A76FF753986A3383A54330B4B63F911EE796A15B21F73AB97FDB3C9CD50153515CD9626245DBD2C38FC8BDD9D60B1D58DD6C0D2D75EE5F8C38741D2F83197EDC27EF27375414A0A3F247CA88730EF5FAF856FDAA5C1858AC6F12327D25AA655403D194A284728802F06269D39C80095AE9DC1172D6896BA05086F770A9DFCD7052C32BB72969B1D4F015BA0CD362FCC59BB3DC76CC12E79F0124A93F62E63ACB7EAF4180E07121940EAE00AE04FFB"})
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
