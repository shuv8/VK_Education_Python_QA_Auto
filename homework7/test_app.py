import settings

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'


class TestApp:

    def test_add_user(self, api_log_client):
        api_log_client.set_base_url(url)
        assert api_log_client._request('POST', url + '/add_user',
                                json={'name': 'Test', 'surname': 'Testov'}).status_code == 201
        assert api_log_client._request('GET', url+'/get_user').status_code == 400
        assert api_log_client._request('GET',
                                       url + '/get_user?name=Test&surname=Testov').status_code == 200
        age = api_log_client._request('GET',
                                       url + '/get_user?name=Test&surname=Testov').json()['age']
        assert age <= 100
        assert api_log_client._request('GET',
                                       url + '/get_user?name=Test&surname=Testov').json()['age'] == age
        api_log_client._request('POST', url + '/add_user',
                                json={'name': 'Petr', 'surname': 'Testov', 'age': 22})
        assert api_log_client._request('GET',
                                       url + '/get_user?name=Petr&surname=Testov').json()['age'] == 22

    def test_update_user(self, api_log_client):
        api_log_client.set_base_url(url)
        api_log_client._request('POST', url + '/add_user',
                                json={'name': 'Ivan', 'surname': 'Ivanov', 'age': 33})
        assert api_log_client._request('PUT', url+'/update_user?name=Ivan&surname=Ivanov',
                                       json={'age': 22}).status_code == 202
        assert api_log_client._request('GET',
                                       url + '/get_user?name=Ivan&surname=Ivanov').json()['age'] == 22

    def test_delete_user(self, api_log_client):
        api_log_client.set_base_url(url)
        api_log_client._request('POST', url + '/add_user',
                                json={'name': 'Delete', 'surname': 'Ivanov',
                                      'age': 33})
        assert api_log_client._request('DELETE', url + '/delete_user',
                                json={'name': 'Delete', 'surname': 'Ivanov'}).status_code == 204
        assert api_log_client._request('GET',
                                       url + '/get_user?name=Delete&surname=Ivanov').status_code == 404
