import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from pathlib import Path
import logging

from tests.conftest import driver

VALID_SCREENSHOT_EXTENSION = ['.png', '.jpg']
DEFAULT_TIMEOUT = 15
DEFAULT_SCREENSHOT_DIR = Path('screenshots')


@dataclass
class TwitchHomePageLocators(DataClassJsonMixin):
    search_button: str
    search_input: str
    search_result: str

@dataclass
class TwitchStarcraftPageLocators(DataClassJsonMixin):
    channel_tab: str
    streamer_card: str
    video_player: str
    skip_popup: str


@dataclass
@dataclass
class TestConfig(DataClassJsonMixin):
    url: str
    search_term: str
    screenshot_filename: Path

    def __post_init__(self):
        self.screenshot_filename = Path(self.screenshot_filename)
        if self.screenshot_filename.suffix not in VALID_SCREENSHOT_EXTENSION:
            raise RuntimeError('Invalid screenshot file extension')

LOCATOR_MAPPING = {
    "twitch_home_page_locators": TwitchHomePageLocators,
    "twitch_starcraft_page_locators": TwitchStarcraftPageLocators,
}

def go_to_url(driver: driver, url: str):
    try:
        driver.get(url)
        logging.info(f'Successfully navigated to URL: {url}')
    except Exception as e:
        logging.error(f'Unexpected error while navigating to {url}: {e}')
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
