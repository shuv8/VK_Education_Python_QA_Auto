"""Module of query builder"""


class MySQLBuilder:
    """Query builder class"""

    def __init__(self, client):
        self.client = client

    def insert_requests_number(self, number_of_requests: int = None):
        """Insert requests number into table"""

        self.client.execute_query(
            f'insert into `total_number_of_requests` (`number_of_requests`)'
            f' values ({number_of_requests})'
        )

    def insert_request_type(self, req_type: str = None, num_of_requests: int = None):
        """Insert requests number by tyoe into table"""

        self.client.execute_query(
            f'insert into `number_of_requests_by_type` (`type`, `number_of_requests`)'
            f' values ("{req_type}", {num_of_requests})'
        )

    def insert_top_request(self, req_path: str = None, num_of_requests: int = None):
        """Insert top requests into table"""

        self.client.execute_query(
            f'insert into `top_requests` (`path`, `number_of_requests`)'
            f' values ("{req_path}", {num_of_requests})'
        )

    def insert_4xx_request(self, req_path: str = None, response_code: int = None,
                           size: int = None, ip: str = None):
        """Insert requests with 4xx into table"""

        self.client.execute_query(
            f'insert into `top_4xx_requests` (`path`, `response_code`, `size`, `ip`)'
            f' values ("{req_path}", {response_code}, {size}, "{ip}")'
        )

    def insert_5xx_user(self, ip: str = None, num_of_requests: int = None):
        """Insert requests with 5xx into table"""

        self.client.execute_query(
            f'insert into `top_5xx_users` (`ip`, `number_of_requests`)'
            f' values ("{ip}", {num_of_requests})'
        )
