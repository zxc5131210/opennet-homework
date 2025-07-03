from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from utils.logger import setup_logger

# init
_driver: Optional[WebDriver] = None
logger = setup_logger(__name__)
DEFAULT_TIMEOUT = 15

def set_driver(driver: WebDriver):
    global _driver
    _driver = driver

def go_to_url(url):
    _driver.get(url)

def save_screenshot(screenshot_path):
    _driver.save_screenshot(screenshot_path)

def wait_and_click(locator, timeout=DEFAULT_TIMEOUT):
    logger.info(f"Attempting to click element: {locator}")
    if _driver is None:
        raise RuntimeError("Driver not set. Please call utils.set_driver(driver) before using.")
    try:
        element = WebDriverWait(_driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        return element
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"Failed to click element {locator}: {e}")
        raise

def wait_for_presence(locator, timeout=DEFAULT_TIMEOUT):
    if _driver is None:
        raise RuntimeError("Driver not set. Please call utils.set_driver(driver) before using.")
    return WebDriverWait(_driver, timeout).until(EC.presence_of_element_located(locator))

def scroll_down(times=1, delay=1):
    if _driver is None:
        raise RuntimeError("Driver not set. Please call utils.set_driver(driver) before using.")
    for _ in range(times + 1):
        _driver.execute_script("window.scrollBy({top: 100, behavior: 'smooth'});")
        time.sleep(delay)
