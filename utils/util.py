import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from pathlib import Path
import logging
import allure
import functools

_test_config = None

def set_test_config(config):
    global _test_config
    _test_config = config


def _save_failure_screenshot(driver, description: str):
    try:
        fail_screenshot_dir = Path(_test_config.default_fail_screenshot_dir)
        if not fail_screenshot_dir.exists():
            fail_screenshot_dir.mkdir(parents=True, exist_ok=True)
        screenshot_name = Path(f"{description}_{time.time_ns()}.png")
        screenshot_path = fail_screenshot_dir / screenshot_name
        driver.save_screenshot(str(screenshot_path))
        logging.error(f"Failure screenshot saved to: {screenshot_path}")
        allure.attach.file(str(screenshot_path), name=description, attachment_type=allure.attachment_type.PNG)
    except Exception as e:
        logging.error(f"Failed to save or attach screenshot: {e}")


def selenium_action(func):
    @functools.wraps(func)
    def wrapper(driver, *args, **kwargs):
        try:
            return func(driver, *args, **kwargs)
        except Exception as e:
            logging.error(f'Error in {func.__name__}: {e}')
            _save_failure_screenshot(driver, f'{func.__name__}_failure')
            raise
    return wrapper


@selenium_action
def go_to_url(driver, url: str):
    driver.get(url)
    logging.info(f'Successfully navigated to URL: {url}')


@selenium_action
def save_screenshot(driver, screenshot_name: Path):
    screenshot_dir = Path(_test_config.default_screenshot_dir)
    if not screenshot_dir.exists():
        screenshot_dir.mkdir()
    screenshot_path = screenshot_dir / screenshot_name
    success = driver.save_screenshot(str(screenshot_path))
    if success:
        logging.info(f'Screenshot saved to: {str(screenshot_path)}')
    else:
        logging.warning(
            f'Screenshot attempt failed (unknown reason) at: {str(screenshot_path)}')


@selenium_action
def wait_and_click(driver, locator: str, timeout: int = None):
    timeout = timeout if timeout is not None else _test_config.default_timeout
    logging.info(f'Attempting to click element: {locator}')
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, locator)))
    element.click()
    return element


@selenium_action
def wait_for_presence(driver, locator: str, timeout: int = None):
    timeout = timeout if timeout is not None else _test_config.default_timeout
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, locator))
    )
    logging.info(f'Element found: {locator}')
    return element


@selenium_action
def scroll_down(driver, times: int, delay: int = 1, scroll_px: float = 100):
    for i in range(times):
        driver.execute_script(
            f"window.scrollBy({{top: {scroll_px}, behavior: 'smooth'}});")
        logging.info(
            f'Scrolled down {scroll_px}px (iteration {i + 1}/{times})')
        time.sleep(delay)


def is_element_exist_and_click(driver, locator: str, timeout: int = 3):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )
        if element.is_displayed():
            element.click()
            logging.info(f'Element {locator} exists and was clicked.')
            return True
    except TimeoutException:
        logging.info(f'Element {locator} not found within {timeout} seconds.')
        return False
    except Exception as e:
        logging.error(f'An error occurred while trying to click {locator}: {e}')
        _save_failure_screenshot(driver, f"element_not_exist_and_click_timeout_{locator.replace('//', '').replace('/', '_')}")
        return False
