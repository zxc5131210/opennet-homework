import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

SCREENSHOT_DIR = "../screenshots"

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()

    mobile_emulation = {
        "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 "
                     "(HTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    }
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    _driver = webdriver.Chrome(options=chrome_options)

    yield _driver
    _driver.quit()

@pytest.fixture(scope="session", autouse=True)
def create_screenshot_dir():
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
        print(f"Created screenshot directory: {SCREENSHOT_DIR}")
