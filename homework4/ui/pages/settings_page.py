"""Module of settings page"""

from ui.locators import SettingsPageLocators
from ui.pages.base_page import BasePage


class SettingsPage(BasePage):
    """Settings page class"""

    locators = SettingsPageLocators()

    def open_news_source(self):
        """Opens settings of news source"""

        self.swipe_to_element(self.locators.NEWS_SOURCE)
        self.click(self.locators.NEWS_SOURCE)

    def open_about(self):
        """Opens info about app"""

        self.swipe_to_element(self.locators.ABOUT_INFO)
        self.click(self.locators.ABOUT_INFO)
