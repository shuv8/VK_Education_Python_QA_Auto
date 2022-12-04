"""Module of parser of nginx logs"""

import re
from collections import Counter


class NginxParser:
    """Nginx parser class

    Has sum functions that provides info from transferred log file"""

    def __init__(self, log_file):
        self.log_file = log_file

    def requests_number(self):
        """Provide total number of requests in logs file"""

        return len(self.log_file.readlines())

    def requests_number_by_type(self):
        """Provides info about number of requests by each type

        :return: Sorted list of requests type
        """
        req_by_type = [request.split()[5][1:] for request in
                       self.log_file.readlines() if
                       len(request.split()[5][1:]) < 100]
        req_by_type = Counter(req_by_type).most_common()
        return req_by_type

    def top_requests(self, num_of_requests: int = 10):
        """Provides info about top requests by its number

        :return: Sorted list of requests
        """
        req_by_url = [re.sub(r'^.*://[^/]*', '', request.split()[6]) for request in
                      self.log_file.readlines()]
        req_by_url = Counter(req_by_url).most_common(num_of_requests)
        return req_by_url

    def top_largest_requests_w_4xx(self, num_of_requests: int = 5):
        """Provides info about largest 4xx requests

        :return: Sorted list of requests
        """

        req_w_4xx = [(re.sub(r'^.*://[^/]*', '', request.split()[6]), int(request.split()[8]),
                      int(request.split()[9]), request.split()[0])
                     for request in self.log_file.readlines() if
                     re.match(r'4\d{2}', request.split()[8])]
        req_w_4xx.sort(key=lambda request: request[2], reverse=True)
        return req_w_4xx[:num_of_requests]

    def top_users_with_5xx_requests(self, num_of_users: int = 5):
        """Provides info about top users with 5xx requests

        :return: Sorted list of users
        """
        ip_5xx = [request.split()[0] for request in self.log_file.readlines() if
                    re.match(r'5\d{2}', request.split()[8])]
        freq_ip = Counter(ip_5xx).most_common(num_of_users)
        return freq_ip
