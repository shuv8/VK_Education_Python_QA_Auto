"""Module of auth page and its methods"""

import allure

from ui.locators import AuthPageLocators
from ui.pages.base_page import BasePage


class AuthPage(BasePage):
    """Auth page object class"""

    locators = AuthPageLocators()

    @allure.step('Log in with credentials {login} {password}')
    def login(self, login, password):
        """Performs authorization on the portal

        Enters credentials to relevant fields and performs authorization

        :param login:
        :param password:
        :return:
        """
        self.logger.info(f'Authorization to {login}')
        self.click_btn(self.locators.LOGIN_BUTTON, timeout=15)
        self.logger.debug(f'Input login={login}')
        self.find(self.locators.LOGIN_INPUT).send_keys(login)
        self.logger.debug(f'Input password={password}')
        self.find(self.locators.PASSWORD_INPUT).send_keys(password)
        self.click_btn(self.locators.SIGN_IN_BUTTON)
