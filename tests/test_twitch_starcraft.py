import os
import time

import pytest
import yaml
from selenium.common.exceptions import TimeoutException

from locators.locators import TwitchLocators
import utils.util as util

config = util.load_config('config.yaml')
TWITCH_URL = config['twitch']['url']
SEARCH_TERM = config['twitch']['search_term']
SCREENSHOT_DIR = config['twitch']['screenshot_dir']
SCREENSHOT_FILENAME = config['twitch']['screenshot_filename']

def test_twitch_stream_screenshot(driver):
    utils = util.Utils(driver)
    utils.go_to_url(TWITCH_URL)

    utils.wait_and_click(TwitchLocators.SEARCH_BUTTON)
    utils.wait_and_click(TwitchLocators.SEARCH_INPUT).send_keys(SEARCH_TERM)
    utils.wait_and_click(TwitchLocators.SEARCH_RESULT)
    utils.wait_and_click(TwitchLocators.CHANNEL_TAB)
    utils.scroll_down(2)

    try:
        utils.wait_and_click(TwitchLocators.STREAMER_CARD).click()
        time.sleep(5)
    except TimeoutException:
        pytest.fail("STREAMER_CARD not found. Please check TwitchLocators.")

    try:
        utils.wait_for_presence(TwitchLocators.VIDEO_PLAYER, timeout=15)
    except TimeoutException:
        pytest.fail("Streamer page may not have fully loaded.")

    screenshot_path = os.path.join(SCREENSHOT_DIR, SCREENSHOT_FILENAME)
    utils.save_screenshot(screenshot_path)