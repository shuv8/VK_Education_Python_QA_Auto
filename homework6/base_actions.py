"""Module with base test case"""

import pytest

from db.client import MySQLClient
from db.builder import MySQLBuilder

class BaseCase:
    """Class of basic actions"""

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, parser):
        """Setup basic test case"""
        self.client: MySQLClient = mysql_client
        self.builder: MySQLBuilder = MySQLBuilder(self.client)
        self.parser = parser
