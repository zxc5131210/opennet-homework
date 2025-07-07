from selenium.webdriver.remote.webdriver import WebDriver
from pathlib import Path
from utils import util

class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_url(self, url: str):
        util.go_to_url(self.driver, url)

    def click_element(self, locator: str, timeout: int = util.DEFAULT_TIMEOUT):
        return util.wait_and_click(self.driver, locator, timeout)

    def find_element(self, locator: str, timeout: int = util.DEFAULT_TIMEOUT):
        return util.wait_for_presence(self.driver, locator, timeout)

    def scroll_down(self, times: int, delay: int = 1, scroll_px: float = 100):
        util.scroll_down(self.driver, times, delay, scroll_px)

    def is_element_present_and_click(self, locator: str, timeout: int = 3):
        return util.is_element_exist_and_click(self.driver, locator, timeout)

    def save_screenshot(self, filename: Path):
        util.save_screenshot(self.driver, filename)