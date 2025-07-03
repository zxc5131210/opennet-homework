import os
from typing import Optional
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import yaml

from tests.conftest import driver
from utils.logger import setup_logger

# init
_driver: Optional[WebDriver] = None
logger = setup_logger(__name__)
DEFAULT_TIMEOUT = 15


def load_config(file):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, '..', 'config', f'{file}')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


class Utils:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_url(self, url):
        try:
            self.driver.get(url)
            logger.info(f"Successfully navigated to URL: {url}")
        except Exception as e:
            logger.error(f"Unexpected error while navigating to {url}: {e}")
            raise

    def save_screenshot(self, screenshot_path):
        try:
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            success = self.driver.save_screenshot(screenshot_path)
            if success:
                logger.info(f"Screenshot saved to: {screenshot_path}")
            else:
                logger.warning(f"Screenshot attempt failed (unknown reason) at: {screenshot_path}")
        except Exception as e:
            logger.error(f"Unexpected error during save_screenshot: {e}")
            raise

    def wait_and_click(self, locator, timeout=DEFAULT_TIMEOUT):
        logger.info(f"Attempting to click element: {locator}")
        try:
            element = WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))
            element.click()
            return element
        except (TimeoutException, NoSuchElementException) as e:
            logger.error(f"Failed to click element {locator}: {e}")
            raise

    def wait_for_presence(self, locator, timeout=DEFAULT_TIMEOUT):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            logger.info(f"Element found: {locator}")
            return element
        except Exception as e:
            logger.error(f"Unexpected error in wait_for_presence: {e}")
            raise

    def scroll_down(self, times, delay=1, scroll_px = 100):
        try:
            for i in range(times + 1):
                self.driver.execute_script(f"window.scrollBy({{top: {scroll_px}, behavior: 'smooth'}});")
                logger.info(f"Scrolled down {scroll_px}px (iteration {i + 1}/{times + 1})")
                time.sleep(delay)
        except Exception as e:
            logger.error(f"Unexpected error in scroll_down: {e}")
            raise
