"""Module with Marussia tests"""

import pytest

from base_actions import BaseCase


class TestCommands(BaseCase):
    """Tests of commands window"""

    @pytest.mark.AndroidUI
    def test_command(self):
        """Test of command execution and selecting suggested command"""

        self.commands_page.enter_command("Russia")
        assert self.commands_page.find(
            self.commands_page.locators.CARD_TITLE).text == 'Россия'
        self.commands_page.scroll_to_suggested_command('население россии')
        assert self.commands_page.wait_for_text(
            self.commands_page.locators.CARD_TITLE,
            '146 млн.')

    @pytest.mark.AndroidUI
    @pytest.mark.parametrize(
        "expression, expected_result",
        [
            pytest.param(
                '1+1', '2',
                id="sum"
            ),
            pytest.param(
                '10-9', '1',
                id="sub"
            ),
            pytest.param(
                '3*7', '21',
                id="mul"
            ),
            pytest.param(
                '35/7', '5',
                id="div"
            ),
        ],
    )
    def test_calculator(self, expression, expected_result):
        """Test of calculator in commands window

        :param expression: Math expression
        :param expected_result: Expected result of expression
        """

        self.commands_page.enter_command(expression)
        assert self.commands_page.driver.find_elements(
            *self.commands_page.locators.DIALOG_ANSWER)[-1].text == expected_result


class TestSettings(BaseCase):
    """Tests of app settings"""

    @pytest.mark.AndroidUI
    def test_news_settings(self):
        """Test of selecting news source"""

        self.commands_page.click(self.commands_page.locators.BURGER_MENU)
        self.settings_page.open_news_source()
        self.news_settings_page.select_source()
        self.driver.back()
        self.driver.back()
        self.commands_page.enter_command('News')
        assert self.commands_page.find(self.commands_page.locators.PLAYER_TRACK_TITLE)

    @pytest.mark.AndroidUI
    def test_about(self):
        """Test of info about app"""

        self.commands_page.click(self.commands_page.locators.BURGER_MENU)
        self.settings_page.open_about()
        self.about_page.check_version()
        assert 'Все права защищены' in self.about_page.find(self.about_page.locators.COPYRIGHT).text
