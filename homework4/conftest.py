"""Pytest conftest module"""
import os

from ui.fixtures import *


def pytest_addoption(parser):
    """Add options that could be used"""

    parser.addoption('--os', default='android')
    parser.addoption("--appium", default='http://127.0.0.1:4723/wd/hub')


@pytest.fixture(scope='session')
def config(request):
    """Makes config from entered options"""

    return {
        'os': request.config.getoption("--os"),
        'appium': request.config.getoption("--appium")
    }


@pytest.fixture()
def driver(config, apk_path):
    """Return driver with specified options"""

    driver = get_driver(config, apk_path)
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def repo_root():
    """Return path from the root"""

    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def apk_path(repo_root):
    """Return path to the apk file

    :param repo_root:
    :return: image path
    """

    return os.path.join(repo_root, 'stuff', 'marussia_1.70.0.apk')
