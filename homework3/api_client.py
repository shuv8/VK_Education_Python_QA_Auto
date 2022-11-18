import requests
from urllib.parse import urljoin, quote
from builder import Builder


class ResponseStatusCodeException(Exception):
    ...


class RespondErrorException(Exception):
    ...


class APIClient:
    def __init__(self, base_url: str, login: str, password: str):
        self.base_url = base_url
        self.login = login
        self.password = password
        self.session = requests.Session()
        self.builder = Builder()

    def _request(self, method, location, headers=None, data=None, files=None, json=None, expected_status=200, jsonify=True):
        url = urljoin(self.base_url, location)
        response = self.session.request(method=method, url=url, headers=headers, data=data, files=files, json=json)
        if response.status_code != expected_status:
            raise ResponseStatusCodeException(f'Expected {expected_status}, but got {response.status_code} for {url}')
        if jsonify:
            json_response: dict = response.json()
            if json_response.get('bStateError', False):
                error = json_response['sErrorMsg']
                raise RespondErrorException(f'Request {url} return error : "{error}"')
            return json_response
        return response

    def post_login(self):
        url = 'https://auth-ac.my.com/auth'
        headers = {'Referer': self.base_url}
        data = self.builder.auth(email=self.login, password=self.password)
        data['continue'] = "https://target-sandbox.my.com/auth/mycom?state=target_login%3D1%26ignore_opener%3D1#email"
        res = self._request('POST', location=url, headers=headers, data=data, jsonify=False)
        assert "error_code=1" not in res.url

    def get_csrf_token(self):
        self._request(method="GET", location='/csrf/', jsonify=False)

    def post_campaign_create(self, name: str, url_id: int, image_id: int):
        url = "/api/v2/campaigns.json"
        headers = {'X-CSRFToken': self.session.cookies['csrftoken']}
        data = self.builder.campaign(name)
        data["banners"][0]["urls"]["primary"]["id"] = url_id
        data["banners"][0]["content"]["image_240x400"]["id"] = image_id
        return self._request(method='POST', location=url, headers=headers, json=data)

    def get_campaign_url_id(self, campaign_url: str):
        url = f'/api/v1/urls/?url={quote(campaign_url, safe="")}'
        return self._request(method='GET', location=url)

    def post_campaign_image(self, image_path: str):
        url = '/api/v2/content/static.json'
        headers = {'X-CSRFToken': self.session.cookies['csrftoken']}
        files = {'file': (image_path, open(image_path, 'rb'))}
        return self._request(method='POST', location=url, headers=headers, files=files)

    def get_campaign(self, campaign_id: int):
        url = f'/api/v2/campaigns/{campaign_id}.json'
        headers = {'X-CSRFToken': self.session.cookies['csrftoken']}
        return self._request(method='GET', location=url, headers=headers)

    def post_campaign_delete(self, campaign_id: int):
        url = f'/api/v2/campaigns/{campaign_id}.json'
        headers = {'X-CSRFToken': self.session.cookies['csrftoken']}
        data = {'status': 'deleted'}
        self._request(method='POST', location=url, headers=headers, json=data, expected_status=204, jsonify=False)

    def get_group_id(self, group_url: str):
        url = f'/api/v2/vk_groups.json?_q={quote(group_url, safe="")}'
        return self._request(method='GET', location=url)

    def post_segment_create(self, name: str, object_type: str, params: dict):
        url = '/api/v2/remarketing/segments.json?fields=relations__object_type,name,id'
        headers = {'X-CSRFToken': self.session.cookies['csrftoken']}
        data = self.builder.segment(name)
        data['relations'][0]['object_type'] = object_type
        data['relations'][0]['params'] = params
        return self._request(method='POST', location=url, headers=headers, json=data)

    def post_source_group(self, group_object_id: int):
        url = '/api/v2/remarketing/vk_groups/bulk.json'
        headers = {'X-CSRFToken': self.session.cookies['csrftoken']}
        data = {"items": [{"object_id": group_object_id}]}
        return self._request(method='POST', location=url, headers=headers, json=data, expected_status=201)

    def delete_source_group(self, group_id: int):
        url = f'/api/v2/remarketing/vk_groups/{group_id}.json'
        headers = {'X-CSRFToken': self.session.cookies['csrftoken']}
        self._request(method='DELETE', location=url, headers=headers, expected_status=204, jsonify=False)

    def delete_segment(self, segment_id: int):
        url = f'/api/v2/remarketing/segments/{segment_id}.json'
        headers = {'X-CSRFToken': self.session.cookies['csrftoken']}
        self._request(method='DELETE', location=url, headers=headers, expected_status=204, jsonify=False)
