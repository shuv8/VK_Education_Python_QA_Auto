import logging
import os
import shutil
import sys
import allure
import pytest
import rstr
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from ui.pages.auth_page import AuthPage
from ui.pages.base_page import BasePage
from ui.pages.campaigns_page import CampaignsPage
from ui.pages.main_page import MainPage
from ui.pages.segments_page import SegmentsPage


def pytest_addoption(parser):
    parser.addoption('--url', default='https://target-sandbox.my.com/')
    parser.addoption("--headless", action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--debug_log', action='store_true')


def pytest_configure(config):
    if sys.platform.startswith('win'):
        base_dir = 'C:\\tests'
    else:
        base_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        os.makedirs(base_dir)
    config.base_temp_dir = base_dir


@pytest.fixture(scope='session')
def config(request):
    if request.config.getoption('--selenoid'):
        if request.config.getoption('--vnc'):
            vnc = True
        else:
            vnc = False
        selenoid = 'http://127.0.0.1:4444/wd/hub'
    else:
        selenoid = None
        vnc = False
    return {
        'url': request.config.getoption("--url"),
        'headless': request.config.getoption("--headless"),
        'selenoid': selenoid,
        'vnc': vnc,
        'debug': request.config.getoption("--debug_log")
    }


@pytest.fixture()
def driver(config):
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
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='105.0.5195.19').install()),
                                  options=options)
    driver.set_page_load_timeout(15)
    driver.get(config['url'])
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def credentials(repo_root):
    with open(os.path.join(repo_root, 'data', 'credentials.txt'), 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    return user, password


@pytest.fixture(scope='session')
def cookies(credentials, config, logger):
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
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(version='105.0.5195.19').install()),
                                  options=options)
    driver.get(config['url'])
    auth_page = AuthPage(driver, logger)
    auth_page.login(*credentials)

    cookies = driver.get_cookies()
    driver.quit()
    return cookies


@pytest.fixture(scope='function')
def auto_auth(auth_page, cookies):
    for cookie in cookies:
        auth_page.driver.add_cookie(cookie)
    auth_page.driver.refresh()
    return auth_page


@pytest.fixture
def base_page(driver, logger):
    return BasePage(driver=driver, logger=logger)


@pytest.fixture
def auth_page(driver):
    return AuthPage(driver=driver, logger=logger)


@pytest.fixture
def main_page(driver, logger):
    return MainPage(driver=driver, logger=logger)


@pytest.fixture
def campaigns_page(driver, logger):
    return CampaignsPage(driver=driver, logger=logger)


@pytest.fixture
def segments_page(driver, logger):
    return SegmentsPage(driver=driver, logger=logger)


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def random_name():
    return rstr.xeger(r'[a-zA-Zа-яА-Я0-9]{5,20}')


@pytest.fixture()
def img_path(repo_root):
    return os.path.join(repo_root, 'data', 'cat.jpeg')


@pytest.fixture(scope='function')
def temp_dir(request):
    test_dir = os.path.join(request.config.base_temp_dir, request._pyfuncitem.nodeid.replace(':', '-'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, temp_dir):
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(temp_dir, 'fail.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'fail.png',
                           attachment_type=allure.attachment_type.PNG)
        browser_logs = os.path.join(temp_dir, 'browser.log')
        with open(browser_logs, 'w') as f:
            for i in driver.get_log('browser'):
                f.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
        with open(browser_logs, 'r') as f:
            allure.attach(f.read(), 'browser.log', allure.attachment_type.TEXT)
        test_logs = os.path.join(request.config.base_temp_dir, 'test.log')
        with open(test_logs, 'r') as f:
            allure.attach(f.read(), 'test.log', allure.attachment_type.TEXT)


@pytest.fixture(scope='session')
def logger(request, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
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
