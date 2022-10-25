"""Module with MyTarget tests"""

import allure
import pytest

from base_actions import BaseCase


@allure.feature('Campaigns tests')
class TestCampaigns(BaseCase):
    """Tests of MyTarget campaigns"""

    @allure.story('Campaign creation')
    @pytest.mark.UI
    def test_campaign_create(self, auto_auth, random_name, img_path):
        """Test of campaign creating

        Create campaign with specified name, then asserts that it was
        successfully created and delete it
        """

        self.main_page.open_page(self.main_page.locators.CAMPAIGNS_BUTTON)
        campaign_id = self.campaigns_page.create(random_name, img_path)
        self.campaigns_page.check(random_name, campaign_id)
        self.campaigns_page.delete(campaign_id)
        self.logger.debug('Driver refresh')
        self.driver.refresh()
        self.campaigns_page.delete_check(campaign_id)


@allure.feature('Segments tests')
class TestSegments(BaseCase):
    """Tests of MyTarget segments"""

    @allure.story('Segment creation')
    @pytest.mark.UI
    def test_segment_create(self, auto_auth, random_name):
        """Test of simple segment creating

        Create segment with specified name, then asserts that it was
        successfully created and delete it
        """

        self.main_page.open_page(self.main_page.locators.SEGMENTS_BUTTON)
        segment_id = self.segments_page.create(random_name)
        self.segments_page.check(random_name, segment_id)
        self.segments_page.delete(segment_id=segment_id)
        self.logger.debug('Driver refresh')
        self.driver.refresh()
        self.segments_page.delete_check(segment_id)

    @allure.story('Segment creation with group source')
    @pytest.mark.UI
    def test_group_segment_create(self, auto_auth, random_name):
        """Test of creating segment with Vk group as source

        Create source group, create segment, based on this group, asserts
        that it was created successfully and that source of the segment is
        specified group, then delete group and segment
        """

        self.main_page.open_page(self.main_page.locators.SEGMENTS_BUTTON)
        group_name = self.segments_page.create_group('https://vk.com/vkedu')
        self.main_page.open_page(self.main_page.locators.SEGMENTS_BUTTON)
        segment_id = self.segments_page.create(random_name, 'group')
        self.segments_page.check_with_group(random_name, segment_id, group_name)
        self.main_page.open_page(self.main_page.locators.SEGMENTS_BUTTON)
        self.segments_page.delete(segment_id)
        self.logger.debug('Driver refresh')
        self.driver.refresh()
        self.segments_page.delete_check(segment_id)
        self.segments_page.click_btn(
            self.segments_page.locators.GROUPS_BUTTON)
        self.segments_page.delete_group(group_name)
        self.logger.debug('Driver refresh')
        self.driver.refresh()
        self.segments_page.delete_group_check(group_name)
