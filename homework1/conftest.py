import os
import pytest
import rstr
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    parser.addoption("--headless", action='store_true')


@pytest.fixture()
def config(request):
    return {"headless": request.config.getoption("--headless")}


@pytest.fixture()
def driver(config):
    options = Options()
    options.headless = config["headless"]
    driver = webdriver.Chrome(executable_path=ChromeDriverManager(version="105.0.5195.19").install(), options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def credentials(repo_root):
    with open(os.path.join(repo_root, 'credentials.txt'), 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    return user, password


@pytest.fixture()
def data_test():
    data = {"name": rstr.xeger('[А-Я][а-я]{2,15}'),
            "phone": rstr.xeger('\\+79[0-9]{9}')}
    return data


@pytest.fixture()
def random_creds():
    data = {'valid_email': rstr.xeger(r'[a-z0-9]{1,10}@[a-z]{1,10}\.[a-z]{1,3}'),
            'invalid_email': rstr.xeger(r'[a-z]{1,20}'),
            'password': rstr.xeger(r'[a-z0-9]{5,20}')}
    return data
