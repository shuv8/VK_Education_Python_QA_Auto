"""Module of app locators"""

from appium.webdriver.common.mobileby import MobileBy


class CommandsPageLocators:
    """Locators of commands page"""

    COMMAND_INPUT = (MobileBy.ID, "ru.mail.search.electroscope:id/input_text")
    KEYBOARD_BUTTON = (MobileBy.ID, 'ru.mail.search.electroscope:id/keyboard')
    COMMAND_ENTER = (MobileBy.ID,
                     'ru.mail.search.electroscope:id/text_input_send')
    CARD_TITLE = (MobileBy.ID,
                  'ru.mail.search.electroscope:id/item_dialog_fact_card_title')
    SUGGESTS = (MobileBy.XPATH,
                '//*[@resource-id="ru.mail.search.electroscope:id/item_suggest_text"]')
    DIALOG_ANSWER = (MobileBy.XPATH,
                     '//*[@resource-id="ru.mail.search.electroscope:id/dialog_item"]')
    BURGER_MENU = (MobileBy.ID,
                   'ru.mail.search.electroscope:id/assistant_menu_bottom')
    PLAYER_TRACK_TITLE = (MobileBy.ID,
                          'ru.mail.search.electroscope:id/player_track_name')


class SettingsPageLocators:
    """Locators of settings page"""

    NEWS_SOURCE = (MobileBy.ID,
                   'ru.mail.search.electroscope:id/user_settings_field_news_sources')
    ABOUT_INFO = (MobileBy.ID,
                  'ru.mail.search.electroscope:id/user_settings_about')


class NewsSettingsPageLocators:
    """Locators of news source select page"""

    SOURCE_IS_SELECTED = (MobileBy.XPATH,
                          '//*[@resource-id="ru.mail.search.electroscope:id/news_sources_item_selected"]/' +
                          'preceding-sibling::' +
                          '*[@resource-id="ru.mail.search.electroscope:id/news_sources_item_title"]')


class AboutPageLocators:
    """Locators of about info page"""

    VERSION = (MobileBy.ID,
               'ru.mail.search.electroscope:id/about_version')
    COPYRIGHT = (MobileBy.ID,
                 'ru.mail.search.electroscope:id/about_copyright')
