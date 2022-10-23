"""Module of news settings page"""
from appium.webdriver.common.mobileby import MobileBy

from ui.locators import NewsSettingsPageLocators
from ui.pages.base_page import BasePage


class NewsSettingsPage(BasePage):
    """News settings page class"""

    locators = NewsSettingsPageLocators()

    def select_source(self, source: str = 'Mail.Ru'):
        """Select news source"""

        loc = (MobileBy.XPATH,
               '//*[@resource-id="ru.mail.search.electroscope:id/news_sources_item_title"' +
               f' and @text="{source}"]')
        self.swipe_to_element(loc)
        self.click(loc)
        assert self.find(self.locators.SOURCE_IS_SELECTED).text == source
