# test_twitch_stream.py

import os
import time
import pytest
from selenium.common.exceptions import TimeoutException

from locators.locators import TwitchLocators
from utils.logger import setup_logger
import utils.util as selenium_utils  # ✅ 匯入整個模組

logger = setup_logger(__name__)

TWITCH_URL = "https://www.twitch.tv/"
SEARCH_TERM = "StarCraft II"
SCREENSHOT_DIR = "../screenshots"
SCREENSHOT_FILENAME = "final_streamer_page.png"

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
