import os
import time

import pytest
from selenium.common.exceptions import TimeoutException
from utils import util


def test_twitch_stream_screenshot(test_config, driver):
    util.go_to_url(driver, test_config.url)
    util.wait_and_click(driver, test_config.locator.search_button)
    util.wait_and_click(
        driver, test_config.locator.search_input).send_keys(test_config.search_term)
    util.wait_and_click(driver, test_config.locator.search_result)
    util.wait_and_click(driver, test_config.locator.channel_tab)
    util.scroll_down(driver, 2)

    try:
        util.wait_and_click(driver, test_config.locator.streamer_card).click()
    except TimeoutException:
        pytest.fail('STREAMER_CARD not found. Please check TwitchLocators.')

    # popup skip handle
    util.handle_popup(driver, test_config.locator.skip_popup)

    try:
        util.wait_for_presence(
            driver, test_config.locator.video_player, timeout=15)
    except TimeoutException:
        pytest.fail('Streamer page may not have fully loaded.')

    util.save_screenshot(driver, test_config.screenshot_filename)
