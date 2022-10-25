"""Pytest conftest module"""

import shutil
import sys

import allure

from ui.fixtures import *


def pytest_addoption(parser):
    """Add options that could be used"""

    parser.addoption('--url', default='https://target-sandbox.my.com/')
    parser.addoption("--headless", action='store_true')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--vnc', action='store_true')
    parser.addoption('--debug_log', action='store_true')


def pytest_configure(config):
    """Configures base directory when starting tests"""

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
    """Makes config from entered options"""

    if request.config.getoption('--selenoid'):
        vnc = bool(request.config.getoption('--vnc'))
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
    """Return driver with specified options"""

    driver = get_driver(config)
    driver.set_page_load_timeout(15)
    driver.get(config['url'])
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def credentials(repo_root):
    """Read credentials from file"""

    with open(os.path.join(repo_root, 'data', 'credentials.txt'), 'r') as file:
        user = file.readline().strip()
        password = file.readline().strip()
    return user, password


@pytest.fixture(scope='session')
def repo_root():
    """Return path from the root"""

    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def img_path(repo_root):
    """Return path to the image

    :param repo_root:
    :return: image path
    """

    return os.path.join(repo_root, 'data', 'cat.jpeg')


@pytest.fixture(scope='function')
def temp_dir(request):
    """Making path to temporary directory

    :param request:
    :return:
    """

    test_dir = os.path.join(request.config.base_temp_dir,
                            request._pyfuncitem.nodeid.replace(':', '-'))
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def ui_report(driver, request, temp_dir):
    """Attach artifacts to report if test fails

    :param driver:
    :param request:
    :param temp_dir:
    :return:
    """
    failed_tests_count = request.session.testsfailed
    yield
    if request.session.testsfailed > failed_tests_count:
        screenshot_file = os.path.join(temp_dir, 'fail.png')
        driver.get_screenshot_as_file(screenshot_file)
        allure.attach.file(screenshot_file, 'fail.png',
                           attachment_type=allure.attachment_type.PNG)
        browser_logs = os.path.join(temp_dir, 'browser.log')
        with open(browser_logs, 'w') as file:
            for i in driver.get_log('browser'):
                file.write(f"{i['level']} - {i['source']}\n{i['message']}\n")
        with open(browser_logs, 'r') as file:
            allure.attach(file.read(), 'browser.log',
                          allure.attachment_type.TEXT)
        test_logs = os.path.join(request.config.base_temp_dir, 'test.log')
        with open(test_logs, 'r') as file:
            allure.attach(file.read(), 'test.log', allure.attachment_type.TEXT)
