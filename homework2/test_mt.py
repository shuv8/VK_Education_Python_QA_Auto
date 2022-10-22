"""Module with MyTarget tests"""

import allure
import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

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
        locator = (By.XPATH, f'//a[contains(@href, "{campaign_id}")]')
        try:
            with allure.step('Campaign name assertion...'):
                self.logger.info('Asserting created campaign name')
                assert self.campaigns_page.find(locator).text == random_name
        finally:
            self.campaigns_page.delete(campaign_id)
            self.logger.debug('Driver refresh')
            self.driver.refresh()
            with allure.step('Campaign delete assertion...'):
                self.logger.info('Asserting campaign is deleted')
                try:
                    assert self.campaigns_page.find(locator, 3).text == random_name
                except TimeoutException:
                    pass


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
        locator = (By.XPATH, f'//a[contains(@href, "{segment_id}")]')
        try:
            with allure.step('Segment name assertion...'):
                self.logger.info('Asserting created segment name')
                assert self.segments_page.find(locator).text == random_name
        finally:
            self.segments_page.delete(segment_id=segment_id)
            self.logger.debug('Driver refresh')
            self.driver.refresh()
            with allure.step('Segment delete assertion...'):
                self.logger.info('Asserting segment is deleted')
                try:
                    assert self.segments_page.find(locator, 3).text == random_name
                except TimeoutException:
                    pass

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
        locator = (By.XPATH, f'//a[contains(@href, "{segment_id}")]')
        try:
            with allure.step('Segment name assertion...'):
                self.logger.info('Asserting created segment name')
                assert self.segments_page.find(locator).text == random_name
            self.segments_page.click_btn(locator)
            with allure.step('Group name in source assertion...'):
                self.logger.info('Asserting created segment source')
                assert group_name in self.segments_page.find(
                    self.segments_page.locators.SEGMENT_SOURCE).text
        finally:
            self.main_page.open_page(self.main_page.locators.SEGMENTS_BUTTON)
            self.segments_page.delete(segment_id)
            self.logger.debug('Driver refresh')
            self.driver.refresh()
            with allure.step('Segment delete assertion...'):
                self.logger.info('Asserting segment is deleted')
                try:
                    assert self.segments_page.find(locator,
                                                   3).text == random_name
                except TimeoutException:
                    pass
            self.segments_page.click_btn(
                self.segments_page.locators.GROUPS_BUTTON)
            self.segments_page.delete_group(group_name)
            self.logger.debug('Driver refresh')
            self.driver.refresh()
            with allure.step('Group source delete assertion...'):
                self.logger.info('Asserting source group is deleted')
                try:
                    assert self.segments_page.find(
                        self.segments_page.locators.GROUP_IN_LIST, 3).text == group_name
                except TimeoutException:
                    pass
