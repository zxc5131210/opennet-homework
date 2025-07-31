from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from pathlib import Path

VALID_SCREENSHOT_EXTENSION = ['.png', '.jpg']

@dataclass
class TwitchHomePageLocators(DataClassJsonMixin):
    search_button: str
    search_input: str
    search_result: str

@dataclass
class TwitchStarcraftPageLocators(DataClassJsonMixin):
    channel_tab: str
    streamer_card: str
    video_player: str
    skip_popup: str

@dataclass
class TestConfig(DataClassJsonMixin):
    url: str
    search_term: str
    screenshot_filename: Path
    default_timeout: int
    default_screenshot_dir: str
    default_fail_screenshot_dir: str

    def __post_init__(self):
        self.screenshot_filename = Path(self.screenshot_filename)
        if self.screenshot_filename.suffix not in VALID_SCREENSHOT_EXTENSION:
            raise RuntimeError('Invalid screenshot file extension')

LOCATOR_MAPPING = {
    "twitch_home_page_locators": TwitchHomePageLocators,
    "twitch_starcraft_page_locators": TwitchStarcraftPageLocators,
}