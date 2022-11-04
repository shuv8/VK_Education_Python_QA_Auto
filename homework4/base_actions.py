"""Module with base actions for tests"""

import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.commands_page import CommandsPage
from ui.pages.about_page import AboutPage
from ui.pages.settings_page import SettingsPage
from ui.pages.news_settings_page import NewsSettingsPage


class BaseCase:
    """Class with basic actions for tests"""

    driver = None
    config = None
    base_page = None
    commands_page = None
    about_page = None
    settings_page = None
    news_settings_page = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, request: FixtureRequest):
        """Setup all needed attributes of Base case"""

        self.driver = driver
        self.config = config

        self.base_page: BasePage = (request.getfixturevalue('base_page'))
        self.commands_page: CommandsPage = (request.getfixturevalue('commands_page'))
        self.about_page: AboutPage = (request.getfixturevalue('about_page'))
        self.settings_page: SettingsPage = (request.getfixturevalue('settings_page'))
        self.news_settings_page: NewsSettingsPage = (request.getfixturevalue('news_settings_page'))
