import logging
import allure
from web_pages.twitch_home_page import TwitchHomePage
from web_pages.twitch_starcraft_page import TwitchStarcraftPage
from pathlib import Path


@allure.feature("Twitch Stream Test")
@allure.story("Search StarCraft II and Watch Stream")
def test_twitch_stream_screenshot(test_config, driver):
    home_page = TwitchHomePage(driver, test_config.twitch_home_page_locators)
    starcraft_page = TwitchStarcraftPage(driver, test_config.twitch_starcraft_page_locators)

    with allure.step("Navigate to Twitch homepage"):
        home_page.navigate_to_home_page(test_config.url)

    with allure.step("Click search button and enter search term"):
        home_page.click_search_button()
        home_page.enter_search_term(test_config.search_term)

    with allure.step("Click 'StarCraft II' search result"):
        home_page.click_search_result_starcraft_ii()

    with allure.step("Click 'Channels' tab and wait for streamer cards"):
        starcraft_page.click_channel_tab()
        starcraft_page.wait_for_streamer_cards()

    with allure.step("scroll down two times"):
        starcraft_page.scroll_down(2)

    with allure.step("Click streamer card"):
        starcraft_page.click_streamer_card()

    with allure.step("Handle content classification popup (if present)"):
        if starcraft_page.skip_content_classification_popup():
            logging.info("Content classification popup was clicked.")
        else:
            logging.info("Content classification popup not found or already dismissed.")

    with allure.step("Wait for video player to appear"):
        starcraft_page.wait_for_video_player(timeout=15)

    with allure.step("Save final page screenshot"):
        screenshot_dir = Path(test_config.default_screenshot_dir)
        final_screenshot_path = screenshot_dir / test_config.screenshot_filename
        starcraft_page.save_screenshot(test_config.screenshot_filename)
        assert final_screenshot_path.exists()
        allure.attach.file(str(final_screenshot_path),
                           name="Final Page Screenshot",
                           attachment_type=allure.attachment_type.PNG)
