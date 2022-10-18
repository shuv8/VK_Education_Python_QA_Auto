import pytest
from base_actions import APIBaseActions


class TestCampaigns(APIBaseActions):

    @pytest.mark.API
    def test_campaign_create(self, random_name, img_path):
        campaign_id = self.campaign_create(name=random_name,
                                           campaign_url='https://github.com/shuv8',
                                           image_path=img_path)['id']
        assert self.api_client.get_campaign(campaign_id)['name'] == random_name
        self.api_client.post_campaign_delete(campaign_id)


class TestSegments(APIBaseActions):

    @pytest.mark.API
    def test_segment_create(self, random_name):
        response = self.segment_create(name=random_name)
        assert response['name'] == random_name
        self.api_client.delete_segment(response['id'])

    @pytest.mark.API
    def test_group_segment_create(self, random_name):
        response, group_id = self.segment_create(name=random_name, source_group_url='https://vk.com/vkedu')
        assert response['name'] == random_name
        assert response['relations'][0]['object_type'] == 'remarketing_vk_group'
        self.api_client.delete_segment(response['id'])
        self.api_client.delete_source_group(group_id)
