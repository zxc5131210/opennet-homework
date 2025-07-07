from web_pages.base_page import BasePage
from utils.util import Locator

class TwitchStarcraftPage(BasePage):
    def __init__(self, driver, locators: Locator):
        super().__init__(driver)
        self.locators = locators

    def click_channel_tab(self):
        self.click_element(self.locators.channel_tab)

    def wait_for_streamer_cards(self):
        self.find_element(self.locators.streamer_card)

    def click_streamer_card(self):
        self.click_element(self.locators.streamer_card)

    def skip_content_classification_popup(self):
        return self.is_element_present_and_click(self.locators.skip_popup)

    def wait_for_video_player(self, timeout: int = 15):
        self.find_element(self.locators.video_player, timeout=timeout)