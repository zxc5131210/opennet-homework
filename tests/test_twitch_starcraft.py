import logging
import pytest
import allure
from selenium.common.exceptions import TimeoutException
from web_pages.twitch_home_page import TwitchHomePage
from web_pages.twitch_starcraft_page import TwitchStarcraftPage
from utils import util


@allure.feature("Twitch Stream Test")
@allure.story("Search StarCraft II and Watch Stream")
@allure.severity(allure.severity_level.CRITICAL)
@allure.link("https://www.twitch.tv/", name="Twitch URL")
def test_twitch_stream_screenshot(test_config, driver):
    home_page = TwitchHomePage(driver, test_config.twitch_home_page_locators)
    starcraft_page = TwitchStarcraftPage(driver, test_config.twitch_starcraft_page_locators)

    with allure.step("Navigate to Twitch homepage"):
        home_page.navigate_to_home_page(test_config.url)
        allure.attach(driver.current_url, name="Current URL", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Click search button and enter search term"):
        home_page.click_search_button()
        home_page.enter_search_term(test_config.search_term)
        allure.attach(test_config.search_term, name="Search Term", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Click 'StarCraft II' search result"):
        home_page.click_search_result_starcraft_ii()

    with allure.step("Click 'Channels' tab and wait for streamer cards"):
        starcraft_page.click_channel_tab()
        starcraft_page.wait_for_streamer_cards()
        starcraft_page.scroll_down(2)

    with allure.step("Click streamer card"):
        try:
            starcraft_page.click_streamer_card()
        except TimeoutException:
            allure.attach(driver.page_source, name="Page Source", attachment_type=allure.attachment_type.HTML)
            util.save_screenshot(driver, util.Path("failed_streamer_card_click.png"))
            allure.attach.file(str(util.DEFAULT_SCREENSHOT_DIR / "failed_streamer_card_click.png"),
                               name="Screenshot on failed streamer card click",
                               attachment_type=allure.attachment_type.PNG)
            pytest.fail('STREAMER_CARD not found. Please check TwitchLocators.')

    with allure.step("Handle content classification popup (if present)"):
        if starcraft_page.skip_content_classification_popup():
            logging.info("Content classification popup was clicked.")
            allure.attach("Content classification popup clicked", name="Popup Handling",
                          attachment_type=allure.attachment_type.TEXT)
        else:
            logging.info("Content classification popup not found or already dismissed.")
            allure.attach("Content classification popup not found or already dismissed", name="Popup Handling",
                          attachment_type=allure.attachment_type.TEXT)

    with allure.step("Wait for video player to appear"):
        try:
            starcraft_page.wait_for_video_player(timeout=15)
            allure.attach("Video player loaded", name="Video Player Status",
                          attachment_type=allure.attachment_type.TEXT)
        except TimeoutException:
            allure.attach(driver.page_source, name="Page Source", attachment_type=allure.attachment_type.HTML)
            util.save_screenshot(driver, util.Path("failed_video_player_load.png"))
            allure.attach.file(str(util.DEFAULT_SCREENSHOT_DIR / "failed_video_player_load.png"),
                               name="Screenshot on failed video player load",
                               attachment_type=allure.attachment_type.PNG)
            pytest.fail('Streamer page may not have fully loaded or video player not found.')

    with allure.step("Save final page screenshot"):
        final_screenshot_path = str(util.DEFAULT_SCREENSHOT_DIR / test_config.screenshot_filename)
        starcraft_page.save_screenshot(test_config.screenshot_filename)
        allure.attach.file(final_screenshot_path,
                           name="Final Page Screenshot",
                           attachment_type=allure.attachment_type.PNG)
