import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Configure logger for this utility file
from utils.logger import setup_logger
logger = setup_logger(__name__)

DEFAULT_TIMEOUT = 15

def wait_and_click(driver, locator, timeout=DEFAULT_TIMEOUT):
    """
    Waits for an element to be clickable, clicks it, and logs the action.
    """
    logger.info(f"Attempting to click element: {locator}")
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        logger.info(f"Successfully clicked element: {locator}")
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for element to be clickable: {locator} did not appear or become clickable"
                     f" within {timeout} seconds.")
        raise
    except NoSuchElementException:
        logger.error(f"Element not found: {locator} could not be located in the DOM.")
        raise

def wait_for_presence(driver, locator, timeout=DEFAULT_TIMEOUT):
    """
    Waits for an element to be present in the DOM and logs the action.
    """
    logger.info(f"Waiting for element presence: {locator}")
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )
        logger.info(f"Successfully waited for element presence: {locator}")
        return element
    except TimeoutException:
        logger.error(f"Timeout waiting for element presence: {locator} did not appear within {timeout} seconds.")
        raise
    except NoSuchElementException:
        logger.error(f"Element not found: {locator} could not be located in the DOM.")
        raise

def scroll_down(driver, times=1, delay=1):
    """
    Scrolls down the page and logs the action.
    """
    for _ in range(times + 1):
        driver.execute_script("""
            window.scrollBy({
                top: 100,
                behavior: 'smooth'
            });
        """)
        time.sleep(delay)
    logger.info(f"scroll down {times+1}")