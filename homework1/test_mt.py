import pytest
import locators
from base_actions import BaseActions


class TestPositive(BaseActions):

    @pytest.mark.UI
    def test_authorize(self, credentials):
        self.open('https://target-sandbox.my.com/')
        self.login(*credentials)

    @pytest.mark.UI
    def test_logout(self, credentials):
        self.open('https://target-sandbox.my.com/')
        self.login(*credentials)
        self.logout()
        assert 'https://target-sandbox.my.com/' == self.driver.current_url

    @pytest.mark.UI
    def test_info_edit(self, credentials, data_test):
        self.open('https://target-sandbox.my.com/')
        self.login(*credentials)
        self.open_page(locators.PROFILE_BUTTON)
        self.set_info(data_test)
        assert self.find(locators.INFO_EDIT_RESULT)
        assert self.find(locators.NAME_INPUT).get_attribute('value') == data_test['name']
        assert self.find(locators.PHONE_INPUT).get_attribute('value') == data_test['phone']
        self.driver.refresh()
        assert self.find(locators.USER_NAME, timeout=15).get_attribute('title') == data_test['name']

    @pytest.mark.UI
    @pytest.mark.parametrize(
        "page, expected_locator",
        [
            pytest.param(
                locators.BILLING_BUTTON, locators.AUTODEPOSIT_BUTTON, id="billing"
            ),
            pytest.param(
                locators.STATISTICS_BUTTON, locators.REPORTS_BUTTON, id="statistics"
            ),
        ],
    )
    def test_change_page(self, page, expected_locator, credentials):
        self.open('https://target-sandbox.my.com/')
        self.login(*credentials)
        self.open_page(page)
        assert self.find(expected_locator, timeout=10)


class TestNegative(BaseActions):
    @pytest.mark.UI
    def test_wrong_creds(self, random_creds):
        self.open('https://target-sandbox.my.com/')
        self.login(login=random_creds['valid_email'],
                   password=random_creds['password'],
                   assertion=False)
        assert 'error_code=1' in self.driver.current_url

    @pytest.mark.UI
    def test_invalid_email(self, random_creds):
        self.open('https://target-sandbox.my.com/')
        self.login(login=random_creds['invalid_email'],
                   password=random_creds['password'],
                   assertion=False)
        assert self.find(locators.INVALID_EMAIL_NOTIFICATION)
