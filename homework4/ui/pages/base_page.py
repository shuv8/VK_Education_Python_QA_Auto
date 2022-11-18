"""Module of basic page"""

from selenium.common.exceptions import StaleElementReferenceException, \
    TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction


class BasePage():
    """Basic page class"""

    CLICK_RETRY = 3
    BASE_TIMEOUT = 5

    def __init__(self, driver):
        """Init needed attributes"""
        self.driver = driver

    def find(self, locator, timeout=None):
        """Finds specified element on page

        :param locator:
        :param timeout:
        """

        return self.wait(timeout).until(
            EC.visibility_of_element_located(locator))

    def wait_for_text(self, locator, text: str, timeout=None):
        """Finds specified text in element

        :param locator:
        :param text:
        :param timeout:
        """

        return self.wait(timeout).until(
            EC.text_to_be_present_in_element(locator, text))

    def wait(self, timeout=None):
        """Waits until the timeout expires

        :param timeout:
        """

        if timeout is None:
            timeout = 10
        return WebDriverWait(self.driver, timeout=timeout)

    def click(self, locator, timeout=None):
        """Click on button with specified locator"""

        for i in range(self.CLICK_RETRY):
            try:
                self.find(locator, timeout=timeout)
                self.wait(timeout).until(
                    EC.element_to_be_clickable(locator)).click()
                return
            except StaleElementReferenceException:
                if i == self.CLICK_RETRY - 1:
                    raise
            except ElementClickInterceptedException:
                if i == self.CLICK_RETRY - 1:
                    raise

    def swipe_up(self, swipetime=200):
        """Swipe up action"""

        action = TouchAction(self.driver)
        dimension = self.driver.get_window_size()
        x = int(dimension['width'] / 2)
        start_y = int(dimension['height'] * 0.8)
        end_y = int(dimension['height'] * 0.2)
        action. \
            press(x=x, y=start_y). \
            wait(ms=swipetime). \
            move_to(x=x, y=end_y). \
            release(). \
            perform()

    def swipe_to_element(self, locator, max_swipes=None):
        """Swipe up to element

        :param locator: Locator of needed element
        :param max_swipes: Max number of swipes
        """
        if max_swipes is None:
            max_swipes = 5
        already_swiped = 0
        while len(self.driver.find_elements(*locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(
                    f"Error with {locator}, please check function")
            self.swipe_up()
            already_swiped += 1

    def swipe_element_lo_left(self, locator=None, web_element=None):
        """Swipes specified element to left

        :param web_element: Element to swipe
        :param locator: Locator of element
        """

        if web_element is None:
            web_element = self.find(locator, 10)
        left_x = web_element.location['x']
        right_x = left_x + web_element.rect['width']
        upper_y = web_element.location['y']
        lower_y = upper_y + web_element.rect['height']
        middle_y = (upper_y + lower_y) / 2
        action = TouchAction(self.driver)
        action. \
            press(x=right_x, y=middle_y). \
            wait(ms=300). \
            move_to(x=left_x, y=middle_y). \
            release(). \
            perform()

    def swipe_left_to_element(self, container_locator,
                              element_locator, max_swipes=None):
        """Swipe left to element

        :param container_locator: Locator of container with elements
        :param element_locator: Locator of needed element
        :param max_swipes: Max number of swipes
        """

        if max_swipes is None:
            max_swipes = 5
        already_swiped = 0
        while len(self.driver.find_elements(*element_locator)) == 0:
            if already_swiped > max_swipes:
                raise TimeoutException(
                    f"Error with {element_locator}, please check function")
            last_element = self.driver.find_elements(*container_locator)[1]
            self.swipe_element_lo_left(web_element=last_element)
            already_swiped += 1
