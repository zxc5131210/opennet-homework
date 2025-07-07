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
    search_term: str # 這裡的 search_term 需要保留，因為你的 config.yaml 裡有它
    screenshot_filename: Path

    def __post_init__(self):
        # 確保 screenshot_filename 是 Path 物件
        self.screenshot_filename = Path(self.screenshot_filename)
        if self.screenshot_filename.suffix not in VALID_SCREENSHOT_EXTENSION:
            raise RuntimeError('Invalid screenshot file extension')

# 定位器映射，也放在這裡，因為它直接與 dataclass 相關聯
LOCATOR_MAPPING = {
    "twitch_home_page_locators": TwitchHomePageLocators,
    "twitch_starcraft_page_locators": TwitchStarcraftPageLocators,
}