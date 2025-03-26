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
    browser.add_cookie({"name": "MUSIC_U", "value": "0085C4E4F8C319CA0258439989489BA950B61F3460821F468F8916E2020E8795829A2B81449F261DC0E63D998C1047D51B7420F507C558E00B8F3F15C20C8B4C467D4ACACBA1899D794DF4756F09ECFB76DF08262FBF0C40D659EC3AE445E9F8328EFAB544BC62162ADA4D5AC7375D9921185725A0B477615AEAAACA3356DD8C2782888C7B3B154C508867B5EB9065C4A239AA5652CAE215717523F78CEA22C06768654FA5D4326C601B59798CDB82F15852CE118B4C63CC81BC8F1DC0902667C0D6ED5839330D67F3B92A6E1C7417DAAAF441BA3002FCF08163F363B274A416E63B20C9FD3B3894A3DA3B46D2715FCA14A4E976AA09A34D010E76BC16F5D049259574310E54A59BFA7DEA9A491440994878B6B3E7A0321618A83969B35F19E7BD64F25FCD90DD3A740B6126C3CC695963C7ED9E4C0EF21C2162571C2D2AC88E1FB081B399BE1482916D9F7A1EB1CB6EE0B5FF4B7C57F551D7FEA93FEB0B0EEA38"})
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
