import os
import time
from time import sleep

import pytest
import yaml
from selenium.common.exceptions import TimeoutException

from locators.locators import TwitchLocators

import utils.util as utils

# Load configuration from YAML file
with open('../config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

TWITCH_URL = config['twitch']['url']
SEARCH_TERM = config['twitch']['search_term']
SCREENSHOT_DIR = config['twitch']['screenshot_dir']
SCREENSHOT_FILENAME = config['twitch']['screenshot_filename']

def test_twitch_stream_screenshot(driver):
    driver.get(TWITCH_URL)

    utils.wait_and_click(driver, TwitchLocators.SEARCH_BUTTON)
    utils.wait_and_click(driver, TwitchLocators.SEARCH_INPUT).send_keys(SEARCH_TERM)
    utils.wait_and_click(driver, TwitchLocators.SEARCH_RESULT)
    utils.wait_and_click(driver, TwitchLocators.CHANNEL_TAB)
    utils.scroll_down(driver, 2)

    try:
        utils.wait_and_click(driver, TwitchLocators.STREAMER_CARD).click()
        time.sleep(5)
    except TimeoutException:
        pytest.fail("STREAMER_CARD not found. Please check TwitchLocators.")

    try:
        utils.wait_for_presence(driver, TwitchLocators.VIDEO_PLAYER, timeout=15)
    except TimeoutException:
        pytest.fail("Streamer page may not have fully loaded.")

    screenshot_path = os.path.join(SCREENSHOT_DIR, SCREENSHOT_FILENAME)
    driver.save_screenshot(screenshot_path)