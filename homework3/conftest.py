import os
import rstr
import pytest
from api_client import APIClient


def pytest_addoption(parser):
    parser.addoption('--url', default="https://target-sandbox.my.com/")


@pytest.fixture(scope='session')
def config(request):
    return {
        'url': request.config.getoption('--url')
    }


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='session')
def credentials(repo_root):
    with open(os.path.join(repo_root, 'data', 'credentials.txt'), 'r') as f:
        user = f.readline().strip()
        password = f.readline().strip()
    return user, password


@pytest.fixture(scope='function')
def api_client(config, credentials):
    return APIClient(config['url'], *credentials)


@pytest.fixture(scope='function')
def random_name():
    return rstr.xeger(r'[a-zA-Zа-яА-Я0-9]{5,20}')


@pytest.fixture()
def img_path(repo_root):
    return os.path.join(repo_root, 'data', 'cat.jpeg')
