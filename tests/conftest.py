import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from utils import util
import yaml

DEFAULT_CONFIG_PATH = Path('config/twitch_startcraft_config.yaml')
LOCATORS_DIR = Path('locators')


def pytest_addoption(parser):
    parser.addoption(
        '--config', action='store', help='config path'
    )


@pytest.fixture
def config_path(request):
    config_path = request.config.getoption('--config')
    yield Path(config_path) if config_path else DEFAULT_CONFIG_PATH


@pytest.fixture
def test_config(config_path):
    with open(config_path, 'r') as file:
        yaml_data = yaml.safe_load(file)

    config = util.TestConfig.from_dict(yaml_data)
    for file_name_stem, locator_dataclass in util.LOCATOR_MAPPING.items():
        locator_file_path = LOCATORS_DIR / f'{file_name_stem}.yaml'
        if locator_file_path.exists():
            with open(locator_file_path, 'r') as file:
                locators_data = yaml.safe_load(file)
            setattr(config, file_name_stem, locator_dataclass.from_dict(locators_data))
        else:
            print(f"Warning: Locator file not found: {locator_file_path}")

    yield config


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
