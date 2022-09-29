import pytest
import locators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException

CLICK_RETRY = 5


class BaseActions:
    driver = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver):
        self.driver = driver

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator, timeout=None):
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def click_btn(self, locator, timeout=None):
        for i in range(CLICK_RETRY):
            try:
                btn = self.find(locator, timeout)
                self.wait(timeout).until(EC.element_to_be_clickable(btn)).click()
                return
            except StaleElementReferenceException:
                if i == CLICK_RETRY - 1:
                    raise
            except ElementClickInterceptedException:
                if i == CLICK_RETRY - 1:
                    raise

    def login(self, login, password, assertion=True):
        try:
            self.click_btn(locators.LOGIN_BUTTON, timeout=10)
        except TimeoutException:
            self.click_btn(locators.LOGIN_BURGER, timeout=1)
            self.click_btn(locators.LOGIN_BUTTON, timeout=1)
        self.find(locators.LOGIN_INPUT).send_keys(login)
        self.find(locators.PASSWORD_INPUT).send_keys(password)
        self.click_btn(locators.SIGN_IN_BUTTON)
        if assertion:
            assert f'data-ga-username="' + login + f'"' in self.driver.page_source

    def logout(self):
        self.click_btn(locators.RIGHT_UPPER_BUTTON)
        try:
            self.click_btn(locators.LOGOUT_BUTTON, timeout=1)
        except TimeoutException:
            self.click_btn(locators.RIGHT_UPPER_BUTTON, timeout=1)
            self.click_btn(locators.LOGOUT_BUTTON, timeout=1)

    def open_page(self, page_loc):
        try:
            self.click_btn(page_loc, timeout=10)
        except TimeoutException:
            self.click_btn(locators.MORE_BUTTON)
            self.click_btn(page_loc)

    def set_info(self, data):
        name_input = self.find(locators.NAME_INPUT)
        name_input.clear()
        name_input.send_keys(data["name"])
        phone_input = self.find(locators.PHONE_INPUT)
        phone_input.clear()
        phone_input.send_keys(data["phone"])
        self.click_btn(locators.SUBMIT_INFO_BUTTON)
