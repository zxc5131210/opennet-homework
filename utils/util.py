# utils/selenium_utils.py

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_and_clickable(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(locator)
    )

def wait_for_presence(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )

def scroll_down(driver, times=1, delay=1):
    for _ in range(times + 1):
        driver.execute_script("""
            window.scrollBy({
                top: 100,
                behavior: 'smooth'
            });
        """)
        time.sleep(delay)