"""UI fixtures"""

import pytest
from appium import webdriver

from builder import Builder
from ui.pages.about_page import AboutPage
from ui.pages.base_page import BasePage
from ui.pages.commands_page import CommandsPage
from ui.pages.news_settings_page import NewsSettingsPage
from ui.pages.settings_page import SettingsPage


def get_driver(config, apk):
    """Return driver with specified config"""

    builder = Builder()
    desired_caps = builder.capability(apk)
    driver = webdriver.Remote(config['appium'], desired_capabilities=desired_caps)
    return driver


@pytest.fixture
def base_page(driver):
    """Return base page object"""

    return BasePage(driver=driver)


@pytest.fixture
def commands_page(driver):
    """Return commands page object"""

    return CommandsPage(driver=driver)


@pytest.fixture
def about_page(driver):
    """Return about page object"""

    return AboutPage(driver=driver)


@pytest.fixture
def settings_page(driver):
    """Return settings page object"""

    return SettingsPage(driver=driver)


@pytest.fixture
def news_settings_page(driver):
    """Return news settings page object"""

    return NewsSettingsPage(driver=driver)
