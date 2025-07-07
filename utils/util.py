import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from pathlib import Path
import logging
import allure

from tests.conftest import driver

VALID_SCREENSHOT_EXTENSION = ['.png', '.jpg']
DEFAULT_TIMEOUT = 15
DEFAULT_SCREENSHOT_DIR = Path('screenshots')
DEFAULT_FAIL_SCREENSHOT_DIR = Path('fail_case_screenshot')


def _save_failure_screenshot(driver: driver, description: str):
    try:
        if not DEFAULT_FAIL_SCREENSHOT_DIR.exists():
            DEFAULT_FAIL_SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_name = Path(f"{description}_{time.time_ns()}.png")
        screenshot_path = DEFAULT_FAIL_SCREENSHOT_DIR / screenshot_name
        driver.save_screenshot(str(screenshot_path))
        logging.error(f"Failure screenshot saved to: {screenshot_path}")
        allure.attach.file(str(screenshot_path), name=description, attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        logging.error(f"Failed to save or attach screenshot: {e}")


def go_to_url(driver: driver, url: str):
    try:
        driver.get(url)
        logging.info(f'Successfully navigated to URL: {url}')
    except Exception as e:
        logging.error(f'Unexpected error while navigating to {url}: {e}')
        _save_failure_screenshot(driver,
                                 f"navigation_error_{url.replace('https://', '')
                                 .replace('http://', '').replace('/', '_')}")
        raise


def save_screenshot(driver: driver, screenshot_name: Path):
    try:
        if not DEFAULT_SCREENSHOT_DIR.exists():
            DEFAULT_SCREENSHOT_DIR.mkdir()
        screenshot_path = DEFAULT_SCREENSHOT_DIR / screenshot_name
        success = driver.save_screenshot(str(screenshot_path))
        if success:
            logging.info(f'Screenshot saved to: {str(screenshot_path)}')
        else:
            logging.warning(
                f'Screenshot attempt failed (unknown reason) at: {str(screenshot_path)}')
    except Exception as e:
        logging.error(f'Unexpected error during save_screenshot: {e}')
        _save_failure_screenshot(driver, f"save_screenshot_error_{screenshot_name.stem}")
        raise


def wait_and_click(driver, locator: str, timeout: int = DEFAULT_TIMEOUT):
    logging.info(f'Attempting to click element: {locator}')
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, locator)))
        element.click()
        return element
    except (TimeoutException, NoSuchElementException):
        message = f'Failed to click element {locator}'
        logging.error(message)
        _save_failure_screenshot(driver, f"click_failure_{locator.replace('//', '')
                                 .replace('/', '_')}")
        raise


def wait_for_presence(driver: driver, locator: str, timeout: int = DEFAULT_TIMEOUT):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )
        logging.info(f'Element found: {locator}')
        return element
    except Exception as e:
        logging.error(f'Unexpected error in wait_for_presence: {e}')
        _save_failure_screenshot(driver, f"presence_failure_{locator.replace('//', '')
                                 .replace('/', '_')}")
        raise


def scroll_down(driver: driver, times: int, delay: int = 1, scroll_px: float = 100):
    try:
        for i in range(times):
            driver.execute_script(
                f"window.scrollBy({{top: {scroll_px}, behavior: 'smooth'}});")
            logging.info(
                f'Scrolled down {scroll_px}px (iteration {i + 1}/{times})')
            time.sleep(delay)
    except Exception as e:
        logging.error(f'Unexpected error in scroll_down: {e}')
        _save_failure_screenshot(driver, f"scroll_down_error")
        raise


def is_element_exist_and_click(driver: driver, locator: str, timeout: int = 3):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )
        element.is_displayed()
        element.click()
        logging.info(f'element exist: {element.is_displayed()}')
    except TimeoutException:
        logging.info(f'element not exist')
        _save_failure_screenshot(driver,
                                 f"element_not_exist_and_click_timeout_{locator.replace('//', '')
                                 .replace('/', '_')}")
