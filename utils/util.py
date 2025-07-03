import os
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
    try:
        _driver.get(url)
        logger.info(f"Successfully navigated to URL: {url}")
    except Exception as e:
        logger.error(f"Unexpected error while navigating to {url}: {e}")
        raise

def save_screenshot(screenshot_path):
    try:
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        success = _driver.save_screenshot(screenshot_path)
        if success:
            logger.info(f"Screenshot saved to: {screenshot_path}")
        else:
            logger.warning(f"Screenshot attempt failed (unknown reason) at: {screenshot_path}")
    except Exception as e:
        logger.error(f"Unexpected error during save_screenshot: {e}")
        raise

def wait_and_click(locator, timeout=DEFAULT_TIMEOUT):
    logger.info(f"Attempting to click element: {locator}")
    try:
        element = WebDriverWait(_driver, timeout).until(EC.element_to_be_clickable(locator))
        element.click()
        return element
    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"Failed to click element {locator}: {e}")
        raise

def wait_for_presence(locator, timeout=DEFAULT_TIMEOUT):
    try:
        element = WebDriverWait(_driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        logger.info(f"Element found: {locator}")
        return element
    except Exception as e:
        logger.error(f"Unexpected error in wait_for_presence: {e}")
        raise

def scroll_down(times, delay=1, scroll_px = 100):
    try:
        for i in range(times + 1):
            _driver.execute_script(f"window.scrollBy({{top: {scroll_px}, behavior: 'smooth'}});")
            logger.info(f"Scrolled down {scroll_px}px (iteration {i + 1}/{times + 1})")
            time.sleep(delay)
    except Exception as e:
        logger.error(f"Unexpected error in scroll_down: {e}")
        raise
