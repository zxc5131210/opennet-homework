import os
import time
import pytest
import yaml
from selenium.common.exceptions import TimeoutException

from locators.locators import TwitchLocators
from utils.logger import setup_logger
import utils.util as selenium_utils  

logger = setup_logger(__name__)

# Load configuration from YAML file
with open('../config/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

TWITCH_URL = config['twitch']['url']
SEARCH_TERM = config['twitch']['search_term']
SCREENSHOT_DIR = config['twitch']['screenshot_dir']
SCREENSHOT_FILENAME = config['twitch']['screenshot_filename']

def test_twitch_stream_screenshot(driver):
    logger.info("Navigating to Twitch homepage...")
    driver.get(TWITCH_URL)

    logger.info("Clicking on search icon...")
    selenium_utils.wait_and_clickable(driver, TwitchLocators.SEARCH_BUTTON).click()

    logger.info(f"Typing search term: {SEARCH_TERM}")
    selenium_utils.wait_and_clickable(driver, TwitchLocators.SEARCH_INPUT).send_keys(SEARCH_TERM)

    logger.info("Clicking search result...")
    selenium_utils.wait_and_clickable(driver, TwitchLocators.SEARCH_RESULT).click()

    logger.info("Clicking on 'Channels' tab...")
    selenium_utils.wait_and_clickable(driver, TwitchLocators.CHANNEL_TAB).click()

    logger.info("Scrolling down to load more channels...")
    selenium_utils.scroll_down(driver, 2)

    logger.info("Clicking on a streamer card...")
    try:
        selenium_utils.wait_and_clickable(driver, TwitchLocators.STREAMER_CARD).click()
        time.sleep(5)
    except TimeoutException:
        logger.error("Could not find a streamer card.")
        pytest.fail("STREAMER_CARD not found. Please check TwitchLocators.")

    logger.info("Waiting for streamer page to load...")
    try:
        selenium_utils.wait_for_presence(driver, TwitchLocators.VIDEO_PLAYER, timeout=15)
        logger.info("Streamer page loaded.")
    except TimeoutException:
        logger.warning("Streamer page may not have fully loaded.")
        pytest.fail("Streamer page may not have fully loaded.")

    screenshot_path = os.path.join(SCREENSHOT_DIR, SCREENSHOT_FILENAME)
    driver.save_screenshot(screenshot_path)
    logger.info(f"Screenshot saved to: {screenshot_path}")