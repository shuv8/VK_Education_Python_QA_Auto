import datetime
from urllib.parse import urljoin

import requests


class APIClient:

    def __init__(self, log_file: str):
        self.base_url = None
        self.log_file = open(log_file, 'w')

    def __del__(self):
        self.log_file.close()
        
    def set_base_url(self, base_url: str):
        self.base_url = base_url

    def _request(self, method, location, headers=None,
                 data=None, files=None, json=None):
        url = urljoin(self.base_url, location)
        response = requests.request(method=method, url=url, headers=headers,
                                    data=data, files=files, json=json)
        self.log_file.write(
            f'{datetime.datetime.now()}\n'
            f'[REQUEST]:\n\t'
            f'Method - {response.request.method}\n\t'
            f'URL - {response.request.url}\n\t'
            f'Body - {response.request.body}\n'
            f'[RESPONSE]:\n\tResponse code - {response.status_code}\n\t'
            f'Headers - {response.headers}\n\t'
            f'Body - {response.text}\n\n\n'
        )
        return response
