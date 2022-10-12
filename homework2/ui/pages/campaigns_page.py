import allure
from selenium.webdriver.common.by import By
from ui.locators import CampaignsPageLocators
from ui.pages.base_page import BasePage
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class CampaignsPage(BasePage):
    locators = CampaignsPageLocators()

    @allure.step('Creating campaign named {name}')
    def create(self, name, img_path):
        self.logger.info(f'Creating campaign {name}')
        try:
            self.click_btn(self.locators.CREATE_BUTTON)
        except TimeoutException:
            self.logger.warning('Creating button not found, trying to click button from instruction')
            self.click_btn(self.locators.CREATE_INSTRUCTION_BUTTON, timeout=5)
        self.click_btn(self.locators.TRAFFIC_BUTTON, timeout=15)
        url_input = self.find(self.locators.URL_INPUT)
        url_input.clear()
        self.logger.debug('Input campaign target url="https://github.com/shuv8"')
        url_input.send_keys('https://github.com/shuv8')
        name_input = self.find(self.locators.NAME_INPUT)
        name_input.clear()
        self.logger.debug(f'Input campaign name={name}')
        name_input.send_keys(name)
        try:
            self.click_btn(self.locators.BANNER_BUTTON, timeout=2)
        except ElementClickInterceptedException:
            self.logger.warning('Banner button not found, trying to close bubble and retry')
            self.click_btn(self.locators.CLOSE_BUBBLE_BUTTON)
            self.click_btn(self.locators.BANNER_BUTTON)
        try:
            img_input = self.find_file_input(self.locators.IMAGE_INPUT, timeout=5)
        except TimeoutException:
            self.logger.warning('Image input not found, trying to choose banner type and retry')
            self.click_btn(self.locators.BANNER_BUTTON)
            img_input = self.find_file_input(self.locators.IMAGE_INPUT)
        self.logger.debug(f'Uploading image from {img_path}')
        img_input.send_keys(img_path)
        try:
            self.find(self.locators.IMAGE_UPLOADED_NOTIFICATION, timeout=3)
        except TimeoutException:
            self.logger.debug(f'Cropping image')
            self.click_btn(self.locators.IMAGE_CROP_BUTTON)
        self.click_btn(self.locators.SUBMIT_BUTTON)
        campaign_elem = self.find((By.XPATH, f'//*[@title="{name}"]'), timeout=15)
        campaign_id = campaign_elem.get_attribute("href").split('/')[-1].replace('?', '')
        self.logger.info(f'Campaign with id={campaign_id} created successfully')
        return campaign_id

    @allure.step('Deleting a campaign with id {campaign_id}')
    def delete(self, campaign_id):
        self.logger.info(f'Deleting campaign with id={campaign_id}')
        locator = (By.XPATH, f'//*[contains(@data-test, "{campaign_id}")]//*[contains(@class, "settingsCell")]')
        self.click_btn(locator)
        self.click_btn(self.locators.DELETE_BUTTON)
        self.logger.info(f'Campaign with id={campaign_id} deleted successfully')
