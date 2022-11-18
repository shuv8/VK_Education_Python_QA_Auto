import pytest


class APIBaseActions:
    api_client = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        self.api_client.post_login()
        self.api_client.get_csrf_token()

    def campaign_create(self, name, campaign_url, image_path):
        url_id = self.api_client.get_campaign_url_id(campaign_url)['id']
        image_id = self.api_client.post_campaign_image(image_path)['id']
        return self.api_client.post_campaign_create(name=name, url_id=url_id, image_id=image_id)

    def segment_create(self, name, source_group_url=None):
        if source_group_url is not None:
            group_id, group_object_id = self.group_create(source_group_url)
            payload_params = self.api_client.builder.params_source_group(group_object_id)
            object_type = "remarketing_vk_group"
            return self.api_client.post_segment_create(name=name, object_type=object_type,
                                                       params=payload_params), group_id
        else:
            payload_params = self.api_client.builder.params_default()
            object_type = "remarketing_player"
            return self.api_client.post_segment_create(name=name, object_type=object_type,
                                                       params=payload_params)

    def group_create(self, group_url):
        group_object_id = self.api_client.get_group_id(group_url)['items'][0]['id']
        group_id = self.api_client.post_source_group(group_object_id)['items'][0]['id']
        return group_id, group_object_id

