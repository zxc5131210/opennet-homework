from web_pages.base_page import BasePage
from utils.util import Locator # 引入 Locator 類來獲取定位器值

class TwitchHomePage(BasePage):

    def __init__(self, driver, locators: Locator):
        super().__init__(driver)
        self.locators = locators

    def click_search_button(self):
        self.click_element(self.locators.search_button)

    def enter_search_term(self, term: str):
        self.click_element(self.locators.search_input).send_keys(term)

    def click_search_result_starcraft_ii(self):
        self.click_element(self.locators.search_result)

    def navigate_to_home_page(self, url: str):
        self.go_to_url(url)