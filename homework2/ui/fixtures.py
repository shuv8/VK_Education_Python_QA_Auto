"""UI fixtures"""

import logging
import os

import pytest
import rstr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from ui.pages.auth_page import AuthPage
from ui.pages.base_page import BasePage
from ui.pages.campaigns_page import CampaignsPage
from ui.pages.main_page import MainPage
from ui.pages.segments_page import SegmentsPage


def get_driver(config):
    """Return driver with specified config"""

    options = Options()
    options.headless = config['headless']
    if config['selenoid']:
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "105.0",
        }
        if config['vnc']:
            capabilities["selenoid:options"] = {"enableVNC": True}
        driver = webdriver.Remote(
            command_executor=config['selenoid'],
            options=options,
            desired_capabilities=capabilities)
    else:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(
            version='105.0.5195.19'
        ).install()),
                                  options=options)
    return driver


@pytest.fixture(scope='session')
def cookies(credentials, config, logger):
    """Return all cookies from authorized session

    :param credentials:
    :param config:
    :param logger:
    :return: session cookies
    """

    driver = get_driver(config)
    driver.get(config['url'])
    auth_page = AuthPage(driver, logger)
    auth_page.login(*credentials)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope='function')
def auto_auth(auth_page, cookies):
    """Return authorized auth page object"""

    for cookie in cookies:
        auth_page.driver.add_cookie(cookie)
    auth_page.driver.refresh()
    return auth_page


@pytest.fixture
def base_page(driver, logger):
    """Return base page object"""

    return BasePage(driver=driver, logger=logger)


@pytest.fixture
def auth_page(driver):
    """Return auth page object"""

    return AuthPage(driver=driver, logger=logger)


@pytest.fixture
def main_page(driver, logger):
    """Return main page object"""

    return MainPage(driver=driver, logger=logger)


@pytest.fixture
def campaigns_page(driver, logger):
    """Return campaigns page object"""

    return CampaignsPage(driver=driver, logger=logger)


@pytest.fixture
def segments_page(driver, logger):
    """Return segments page object"""

    return SegmentsPage(driver=driver, logger=logger)


@pytest.fixture()
def random_name():
    """Makes random string from regular expression

    :return: random name
    """

    return rstr.xeger(r'[a-zA-Zа-яА-Я0-9]{5,20}')


@pytest.fixture(scope='session')
def logger(request, config):
    """Writing logs to specified files

    :param request:
    :param config:
    :return:
    """

    log_formatter = logging.Formatter(
        '%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    log_file = os.path.join(request.config.base_temp_dir, 'test.log')
    log_level = logging.DEBUG if config['debug'] else logging.INFO

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
