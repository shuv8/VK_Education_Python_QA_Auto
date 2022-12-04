"""Module with tests"""

import pytest

from base_actions import BaseCase


class TestDB(BaseCase):
    """DB tests class"""

    @pytest.mark.DB
    def test_total_number_of_requests(self):
        """Test of total request number"""

        number_of_requests = self.parser.requests_number()
        self.builder.insert_requests_number(number_of_requests)
        query = self.client.execute_query(
            'select * from total_number_of_requests', True
        )
        assert len(query) == 1
        assert query[0].number_of_requests == 225133

    @pytest.mark.DB
    def test_requests_type(self):
        """Test of request number by type"""

        req_by_type = self.parser.requests_number_by_type()
        for request in req_by_type:
            self.builder.insert_request_type(request[0], request[1])
        query = self.client.execute_query(
            'select * from number_of_requests_by_type order by number_of_requests desc', True
        )
        assert len(query) == 4
        assert query[1].type == 'POST'
        assert query[1].number_of_requests == 102503

    @pytest.mark.DB
    def test_top_requests(self, config):
        """Test of top requests"""

        top_requests = self.parser.top_requests(config['top_number'])
        for request in top_requests:
            self.builder.insert_top_request(request[0].replace('%', '%%'), request[1])
        query = self.client.execute_query(
            'select * from top_requests order by number_of_requests desc',
            True
        )
        assert len(query) == config['top_number']
        if config['top_number'] >= 4:
            assert query[3].path == '/templates/_system/css/general.css'
            assert query[3].number_of_requests == 4980

    @pytest.mark.DB
    def test_top_4xx_requests(self, config):
        """Test of top requests with 4xx by size"""

        top_4xx_requests = self.parser.top_largest_requests_w_4xx(config['4xx_number'])
        for request in top_4xx_requests:
            self.builder.insert_4xx_request(request[0].replace('%', '%%'), request[1],
                                            request[2], request[3])
        query = self.client.execute_query(
            'select * from top_4xx_requests order by size desc',
            True
        )
        assert len(query) == config['4xx_number']

    @pytest.mark.DB
    def test_top_5xx_users(self, config):
        """Test of top users with 5xx"""

        top_5xx_users = self.parser.top_users_with_5xx_requests(
            config['5xx_number'])
        for request in top_5xx_users:
            self.builder.insert_5xx_user(request[0].replace('%', '%%'), request[1])
        query = self.client.execute_query(
            'select * from top_5xx_users order by number_of_requests desc',
            True
        )
        assert len(query) == config['5xx_number']
