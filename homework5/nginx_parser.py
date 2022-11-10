import json
import os
import re
import time
from argparse import ArgumentParser
from collections import Counter

LOG_FILE = os.path.join(os.path.abspath(os.path.join(__file__, os.path.pardir)), 'access.log')
RES_FILE = os.path.join(os.path.abspath(os.path.join(__file__, os.path.pardir)), 'res_py.txt')
RES_JSON = os.path.join(os.path.abspath(os.path.join(__file__, os.path.pardir)), 'res_py.json')


class NginxParser:

    def __init__(self, log_file, res_file=None, json_file=None):
        self.log_file = open(log_file, 'r')
        self.arg_parser = ArgumentParser()
        self.arg_parser.add_argument('--json', action='store_true',
                                     default=False)
        self.json = self.arg_parser.parse_args().json
        if self.json:
            self.json_info = {}
            self.json_file = open(json_file, 'w')
        else:
            self.res_file = open(res_file, 'w')

    def __del__(self):
        self.log_file.close()
        if self.json:
            json.dump(self.json_info, self.json_file, indent=3)
            self.json_file.close()
        else:
            self.res_file.close()

    def requests_number_by_type(self):
        req_by_type = [request.split()[5][1:] for request in
                       self.log_file.readlines() if
                       len(request.split()[5][1:]) < 100]
        req_by_type = Counter(req_by_type).most_common()
        self.log_file.seek(0)

        if self.json:
            self.json_info["Number of requests by type"] = {
                req_type[0]: req_type[1] for req_type in req_by_type}
        else:
            self.res_file.write('Total number of requests by type:\n')
            self.res_file.writelines(
                [f'{req_type[0]} - {req_type[1]}\n' for req_type in req_by_type])

    def top10_requests(self):
        req_by_url = [re.sub(r'^.*://[^/]*', '', request.split()[6]) for request in
                      self.log_file.readlines()]
        req_by_url = Counter(req_by_url).most_common(10)
        self.log_file.seek(0)

        if self.json:
            self.json_info["Top 10 most frequent requests"] = [
                {"PATH": request[0], "Number of requests": request[1]} for
                request in req_by_url]
        else:
            self.res_file.write('\nTop 10 most frequent requests:')
            self.res_file.writelines(
                [f'\nPATH: {request[0]}\nNumber of requests: {request[1]}\n-' for
                 request in req_by_url])

    def top5_users_with_5xx_requests(self):
        ip_5xx = [request.split()[0] for request in self.log_file.readlines() if
                    re.match(r'5\d{2}', request.split()[8])]
        freq_ip = Counter(ip_5xx).most_common(5)
        self.log_file.seek(0)

        if self.json:
            self.json_info["Top 5 users by number of requests with (5XX) error"] = [
                {"IP": ip[0], "Number of requests": ip[1]} for
                ip in freq_ip]
        else:
            self.res_file.write(
                '\n\nTop 5 users by number of requests with (5XX) error:')
            self.res_file.writelines(
                [f'\nIP: {ip[0]}\nNumber of requests: {ip[1]}\n-' for ip in
                 freq_ip])


if __name__ == "__main__":
    start_time = time.time()
    parser = NginxParser(LOG_FILE, RES_FILE, RES_JSON)
    parser.requests_number_by_type()
    parser.top10_requests()
    parser.top5_users_with_5xx_requests()
    print("It took %s seconds" % (time.time() - start_time))
