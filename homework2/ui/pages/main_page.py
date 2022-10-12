import allure
from selenium.common.exceptions import TimeoutException
from ui.pages.base_page import BasePage
from ui.locators import MainPageLocators


class MainPage(BasePage):
    locators = MainPageLocators()

    @allure.step('Opening page')
    def open_page(self, page_loc):
        self.logger.info('Opening necessary page')
        self.logger.debug(f'Opening page with locator {page_loc}')
        try:
            self.logger.debug('Click on page button')
            self.click_btn(page_loc)
        except TimeoutException:
            self.logger.warning('Page button not found, trying to open more')
            self.click_btn(self.locators.MORE_BUTTON)
            self.click_btn(page_loc)
