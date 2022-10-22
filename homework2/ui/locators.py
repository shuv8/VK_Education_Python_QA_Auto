"""Module of element's locators"""

from selenium.webdriver.common.by import By


class AuthPageLocators:
    """Locators of auth page"""

    LOGIN_BUTTON = (By.XPATH,
                    '//*[contains(@class, "responseHead-module-button")]')
    LOGIN_INPUT = (By.NAME, 'email')
    PASSWORD_INPUT = (By.NAME, 'password')
    SIGN_IN_BUTTON = (By.XPATH,
                      '//*[contains(@class, "authForm-module-button")]')


class MainPageLocators:
    """Locators of main page"""

    MORE_BUTTON = (By.XPATH, '//*[contains(@class, "center-module-more")]')
    CAMPAIGNS_BUTTON = (By.XPATH,
                        '//*[contains(@class, "center-module-campaigns")]')
    SEGMENTS_BUTTON = (By.XPATH,
                       '//*[contains(@class, "center-module-segments")]')


class CampaignsPageLocators:
    """Locators of campaigns page"""

    CREATE_INSTRUCTION_BUTTON = (By.XPATH,
        '//*[contains(@class, "instruction-module-item")]//*[contains(@href, "/campaign/new")]')
    CREATE_BUTTON = (By.XPATH,
                     '//*[contains(@class, "dashboard-module-createButton")]/div')
    TRAFFIC_BUTTON = (By.XPATH, '//*[contains(@class, "traffic")]')
    URL_INPUT = (By.XPATH,
                 '//*[contains(@class, "mainUrl-module-searchInput")]')
    NAME_INPUT = (By.XPATH, '//*[contains(@class, "campaign-name")]//input')
    BANNER_BUTTON = (By.ID, 'patterns_banner_4')
    IMAGE_INPUT = (By.XPATH,
                   "//input[@type='file' and @data-test='image_240x400']")
    IMAGE_UPLOADED_NOTIFICATION = (By.XPATH,
                                   '//*[contains(@class, "patternTabs-module-green")]')
    IMAGE_CROP_BUTTON = (By.XPATH,
                         '//*[contains(@class, "image-cropper__save")]')
    SUBMIT_BUTTON = (By.XPATH,
                     '//div[contains(@class, "js-save-button-wrap")]/button')
    DELETE_BUTTON = (By.XPATH,
                     '//li[contains(@class, "optionsList-module-option")][5]')
    CLOSE_BUBBLE_BUTTON = (By.XPATH,
                           '//span[contains(@class, "js-bubble-close")]')


class SegmentsPageLocators:
    """Locators of segments page"""

    CREATE_BUTTON = (By.XPATH, '//a[@href="/segments/segments_list/new/"]')
    CREATE_NOTEMPTY_BUTTON = (By.XPATH,
        '//div[contains(@class, "segments-list__btn-wrap js-create-button-wrap")]/button')
    SEGMENT_CHECKBOX = (By.XPATH,
                        '//*[contains(@class, "adding-segments-source__checkbox")]')
    ADD_SEGMENT_BUTTON = (By.XPATH,
                          '//div[contains(@class, "js-add-button")]/button')
    NAME_INPUT = (By.XPATH,
                  '//*[contains(@class, "input_create-segment-form")]//input')
    SUBMIT_BUTTON = (By.XPATH,'//*[contains(@class, "button_submit")]')
    DELETE_BUTTON = (By.XPATH,
                     '//*[contains(@class, "optionsList-module") and @data-id="remove"]')
    DELETE_CONFIRM_BUTTON = (By.XPATH,
                             '//*[contains(@class, "button_confirm-remove")]')
    ACTIONS_BUTTON = (By.XPATH,
                      '//*[contains(@class, "segmentsTable-module-selectItem")]')
    GROUPS_BUTTON = (By.XPATH, '//*[@href="/segments/groups_list"]')
    GROUP_URL_INPUT = (By.XPATH,
                       '//input[contains(@class, "multiSelectSuggester")]')
    SHOW_GROUPS_BUTTON = (By.XPATH, '//*[@data-test="show"]')
    GROUP_TITLE_BUTTON = (By.XPATH,
                          '//*[contains(@class, "optionsList-module-item")]')
    GROUP_TITLE_TEXT = (By.XPATH,
                        '//*[contains(@class, "optionsList-module-item")]//span')
    ADD_SELECTED_GROUPS_BUTTON = (By.XPATH,
                                  '//*[@data-test="add_selected_items_button"]')
    GROUP_IN_LIST = (By.XPATH,
                     '//*[contains(@class, "js-cell-name") and @data-id="name"]//span')
    GROUP_SEGMENT_BUTTON = (By.XPATH,
                            '//*[contains(@class, "adding-segments-item") ' +
                            'and contains(text(), "VK")]')
    SEGMENT_SOURCE = (By.XPATH, '//*[contains(@class, "js-source-name")]')
    SLIDER = (By.XPATH,
      '//*[contains(@class, "flexi-table")]//*[contains(@class, "horizontal custom-scroll")]/div')
