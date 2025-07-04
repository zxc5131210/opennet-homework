import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from utils import util
import yaml

DEFAULT_SCREENSHOT_PATH = Path('screenshots/final_streamer_page.png')
DEFAULT_CONFIG_PATH = Path('config/twitch_startcraft_config.yaml')


def pytest_addoption(parser):
    parser.addoption(
        '--config', action='store', help='config path'
    )


@pytest.fixture
def config_path(request):
    config_path = request.config.getoption('--config')
    if not config_path:
        yield DEFAULT_CONFIG_PATH
    else:
        yield Path(config_path)


@pytest.fixture
def test_config(config_path):
    with open(config_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    yield util.TestConfig.from_dict(yaml_data)


@pytest.fixture(scope='function')
def driver():
    chrome_options = Options()

    mobile_emulation = {
        'deviceMetrics': {'width': 360, 'height': 640, 'pixelRatio': 3.0},
        'userAgent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 '
                     '(HTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'
    }
    chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)

    _driver = webdriver.Chrome(options=chrome_options)

    yield _driver
    _driver.quit()
