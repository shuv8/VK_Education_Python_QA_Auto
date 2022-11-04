"""Module of commands page"""
from appium.webdriver.common.mobileby import MobileBy

from ui.pages.base_page import BasePage
from ui.locators import CommandsPageLocators


class CommandsPage(BasePage):
    """Commands page class"""

    locators = CommandsPageLocators()

    def enter_command(self, command: str):
        """Enter command and send it

        :param command: Command that we want to send
        """

        self.click(self.locators.KEYBOARD_BUTTON)
        self.find(self.locators.COMMAND_INPUT).send_keys(command)
        self.click(self.locators.COMMAND_ENTER)
        self.driver.hide_keyboard()

    def scroll_to_suggested_command(self, command: str):
        """Scroll to specified command and choose it

        :param command: Command that we want to scroll to
        """

        loc = (MobileBy.XPATH,
               '//*[@resource-id="ru.mail.search.electroscope:id/item_suggest_text" ' +
               f'and contains(@text, "{command}")]')
        self.swipe_left_to_element(self.locators.SUGGESTS,
                                   loc, 20)
        self.click(loc)
