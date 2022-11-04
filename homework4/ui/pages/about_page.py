"""Module of app about page"""

from ui.locators import AboutPageLocators
from ui.pages.base_page import BasePage


class AboutPage(BasePage):
    """About page class"""

    locators = AboutPageLocators()

    def check_version(self):
        """Check app version"""

        apk_version = self.driver.capabilities.get('app')\
            .rpartition('marussia_')[-1].replace('.apk', '')
        assert apk_version in self.find(self.locators.VERSION).text
