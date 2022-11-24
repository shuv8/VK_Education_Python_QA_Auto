"""Pytest conftest module"""

import os
import pytest

from nginx_parser import NginxParser
from db.client import MySQLClient


def pytest_configure(config):
    """Configuration before tests"""

    mysql_client = MySQLClient(user='root', password='pass', db_name='TEST_SQL')
    if not hasattr(config, 'workerinput'):
        mysql_client.create_db()
    mysql_client.connect(db_created=True)
    if not hasattr(config, 'workerinput'):
        mysql_client.create_table_total_num()
        mysql_client.create_table_types()
        mysql_client.create_table_top_requests()
        mysql_client.create_table_top_4xx_requests()
        mysql_client.create_table_top_5xx_users()

    config.mysql_client = mysql_client


def pytest_addoption(parser):
    """Add options that could be used"""

    parser.addoption('--top_number', default=10)
    parser.addoption('--4xx_number', default=10)
    parser.addoption('--5xx_number', default=10)


@pytest.fixture(scope='session')
def config(request):
    """Makes config from entered options"""

    return {
        'top_number': int(request.config.getoption("--top_number")),
        '4xx_number': int(request.config.getoption("--4xx_number")),
        '5xx_number': int(request.config.getoption("--5xx_number"))
    }


@pytest.fixture(scope='session')
def repo_root():
    """Return path from the root"""

    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture(scope='function')
def open_logs(repo_root):
    """Return logs file stream"""

    logs_file = open(os.path.join(repo_root, 'access.logs'), 'r')
    yield logs_file
    logs_file.close()


@pytest.fixture(scope='function')
def parser(open_logs):
    """Return an object of nginx logs parser"""

    parser = NginxParser(open_logs)
    return parser


@pytest.fixture(scope='session')
def mysql_client(request) -> MySQLClient:
    """Return mysql client"""

    client = request.config.mysql_client
    yield client
    client.connection.close()
