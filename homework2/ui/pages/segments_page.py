"""Module of segment page and its methods"""

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from ui.locators import SegmentsPageLocators
from ui.pages.base_page import BasePage


class SegmentsPage(BasePage):
    """Segment page object class"""

    locators = SegmentsPageLocators()

    @allure.step('Creating segment named {name}')
    def create(self, name, source=None):
        """Creates segment with specified name and source

        Fills all needed fields and creates segment. If source isn't specified
        it will be default, otherwise it could be VK group
        """
        self.logger.info(f'Creating segment {name}')
        try:
            self.click_btn(self.locators.CREATE_BUTTON, timeout=10)
        except TimeoutException:
            self.logger.warning(
                "Segments list isn't empty, trying to create new segment")
            self.click_btn(self.locators.CREATE_NOTEMPTY_BUTTON)
        if source is not None:
            if source == 'group':
                self.logger.debug(f'Segment source is {source}')
                self.click_btn(self.locators.GROUP_SEGMENT_BUTTON)
        self.click_btn(self.locators.SEGMENT_CHECKBOX)
        self.click_btn(self.locators.ADD_SEGMENT_BUTTON)
        name_input = self.find(self.locators.NAME_INPUT)
        name_input.clear()
        self.logger.debug(f'Input segment name={name}')
        name_input.send_keys(name)
        self.click_btn(self.locators.SUBMIT_BUTTON)
        locator = (By.XPATH, f'//*[@title="{name}"]')
        elem = self.find(locator)
        id_elem = elem.get_attribute("href").split('/')[-1]
        self.logger.info(f'Segment with id={id_elem} created successfully')
        return id_elem

    @allure.step('Deleting a segment with id {segment_id}')
    def delete(self, segment_id):
        """Delete segment with specified id"""

        self.logger.info(f'Deleting segment with id={segment_id}')
        locator = (By.XPATH,
                   f'//*[contains(@data-test, "id-{segment_id}")]//input[@type="checkbox"]')
        self.click_btn(locator)
        self.click_btn(self.locators.ACTIONS_BUTTON)
        self.click_btn(self.locators.DELETE_BUTTON)
        self.logger.info(f'Segment with id={segment_id} deleted successfully')

    @allure.step('Creating source group {url}')
    def create_group(self, url):
        """Create source group with specified URL"""

        self.logger.info(f'Creating source group with url={url}')
        self.click_btn(self.locators.GROUPS_BUTTON)
        group_url_input = self.find(self.locators.GROUP_URL_INPUT)
        group_url_input.clear()
        self.logger.debug(f'Input group url={url}')
        group_url_input.send_keys(url)
        self.click_btn(self.locators.SHOW_GROUPS_BUTTON)
        group_name = self.find(self.locators.GROUP_TITLE_TEXT).text
        self.click_btn(self.locators.GROUP_TITLE_BUTTON)
        self.click_btn(self.locators.ADD_SELECTED_GROUPS_BUTTON)
        self.logger.info('Asserting created source group name')
        assert self.find(self.locators.GROUP_IN_LIST).text == group_name
        self.logger.info(
            f'Source group with url={url} and name={group_name} created successfully')
        return group_name

    @allure.step('Deleting a source group named {name}')
    def delete_group(self, name):
        """Delete group with specified name"""

        self.logger.info(f'Deleting source group {name}')
        locator = (By.XPATH,
                   f'//*[@data-id="name"]/span[text()="{name}"]' +
                   '/following::td[@data-id="remove"]/div')
        try:
            self.click_btn(locator)
        except TimeoutException:
            self.logger.warning(
                "Delete button not found, trying to scroll table and retry")
            slider = self.find(self.locators.SLIDER)
            ActionChains(self.driver).click_and_hold(slider). \
                move_by_offset(200, 0).release().perform()
            self.click_btn(locator, timeout=15)
        self.click_btn(self.locators.DELETE_CONFIRM_BUTTON)
        self.logger.info(f'Source group {name} deleted successfully')

    @allure.step('Segment name assertion...')
    def check(self, name, segment_id):
        """Check if specified segment is created successfully

        :param name:
        :param segment_id:
        :return:
        """

        locator = (By.XPATH, f'//a[contains(@href, "{segment_id}")]')
        try:
            self.logger.info('Asserting created segment name')
            assert self.find(locator).text == name
        finally:
            pass

    @allure.step('Segment delete assertion...')
    def delete_check(self, segment_id):
        """Check if specified segment is deleted

        :param segment_id:
        :return:
        """

        locator = (By.XPATH, f'//a[contains(@href, "{segment_id}")]')
        self.logger.info('Asserting segment is deleted')
        try:
            assert self.find(locator, 3)
        except TimeoutException:
            pass

    @allure.step('Segment name assertion...')
    def check_with_group(self, name, segment_id, group_name):
        """Check if specified segment with group source is created successfully

        :param name:
        :param segment_id:
        :param group_name:
        :return:
        """

        locator = (By.XPATH, f'//a[contains(@href, "{segment_id}")]')
        try:
            self.logger.info('Asserting created segment name')
            assert self.find(locator).text == name
            self.click_btn(locator)
            with allure.step('Group name in source assertion...'):
                self.logger.info('Asserting created segment source')
                assert group_name in self.find(
                    self.locators.SEGMENT_SOURCE).text
        finally:
            pass

    @allure.step('Group source delete assertion...')
    def delete_group_check(self, group_name):
        """Check if specified group is deleted

        :param group_name:
        :return:
        """

        self.logger.info('Asserting source group is deleted')
        try:
            assert self.find(
                self.locators.GROUP_IN_LIST, 3).text == group_name
        except TimeoutException:
            pass
