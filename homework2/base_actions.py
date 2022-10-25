"""Module with base actions for tests"""

import pytest
from _pytest.fixtures import FixtureRequest

from ui.pages.base_page import BasePage
from ui.pages.auth_page import AuthPage
from ui.pages.campaigns_page import CampaignsPage
from ui.pages.main_page import MainPage
from ui.pages.segments_page import SegmentsPage


class BaseCase:
    """Class with basic actions for tests"""

    driver = None
    config = None
    logger = None
    base_page = None
    auth_page = None
    main_page = None
    campaigns_page = None
    segments_page = None

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, config, logger, request: FixtureRequest):
        """Setup all needed attributes of Base case"""

        self.driver = driver
        self.config = config
        self.logger = logger

        self.base_page: BasePage = (request.getfixturevalue('base_page'))
        self.auth_page: AuthPage = (request.getfixturevalue('auth_page'))
        self.main_page: MainPage = (request.getfixturevalue('main_page'))
        self.campaigns_page: CampaignsPage = (request.getfixturevalue('campaigns_page'))
        self.segments_page: SegmentsPage = (request.getfixturevalue('segments_page'))
