from selenium.webdriver.common.by import By


class TwitchLocators:
    SEARCH_BUTTON = (By.XPATH, "//div[@class='Layout-sc-1xcs6mc-0 iwaIid']//div[text()='瀏覽']")
    SEARCH_INPUT = (By.XPATH, "//input[@type='search']")
    SEARCH_RESULT = (By.XPATH, "//p[@title='StarCraft II']")
    CHANNEL_TAB = (By.XPATH, "//div[@class='ScTitle-sc-iekec1-3 gesXMd'][text()='頻道']")
    FIRST_SEARCH_RESULT_LINK = (By.XPATH, "(//a[@data-a-target='search-result-link'])[1]")
    STREAMER_CARD = (By.XPATH, "(//div[@class='Layout-sc-1xcs6mc-0 doaFqY'])[3]")
    VIDEO_PLAYER = (By.XPATH, "//div[@data-a-target='player-overlay-click-handler']")