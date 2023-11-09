import time

from selenium.common import ElementNotVisibleException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re


class BasePage:
    def __init__(self, driver):
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 25)

    def __wait_until_element_visible(self, locator: tuple):
        return self._wait.until(EC.visibility_of_element_located(locator))

    def __wait_until_element_invisible(self, locator: tuple):
        return self._wait.until(EC.invisibility_of_element_located(locator))

    def __wait_until_element_clickable(self, locator: tuple):
        return self._wait.until(EC.element_to_be_clickable(locator))

    def send_keys(self, locator, value, is_clear=True):
        element = self.__wait_until_element_visible(locator)
        if is_clear:
            element.clear()
            element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(value)

    def click(self, locator):
        self.__wait_until_element_clickable(locator).click()

    def is_displayed(self, locator):
        user_label_element = self.__wait_until_element_visible(locator)
        return user_label_element.is_displayed()

    def is_not_displayed(self, locator):
        user_label_element = self.__wait_until_element_invisible(locator)
        return user_label_element.is_displayed()

    def get_text(self, locator):
        element = self.__wait_until_element_visible(locator)
        return element.text

    def get_numeric_price_value(self, locator):
        element = self.__wait_until_element_visible(locator)
        text = element.text.replace("₴", "").strip()
        return text

    def get_placeholder(self, locator):
        element = self.__wait_until_element_visible(locator)
        return element.placeholder

    def get_element(self, by, value):
        element = self.__wait_until_element_visible((by, value))
        return element

    def get_element_by_locator(self, locator):
        element = self.__wait_until_element_visible(locator)
        return element

    def get_element_data_item_qty(self, locator):
        element = self.__wait_until_element_visible(locator)
        quantity = element.get_attribute("data-item-qty")
        return quantity

    def get_element_style(self, locator):
        element = self.__wait_until_element_visible(locator)
        style = element.get_attribute("style")
        return style

    def click_via_js(self, locator):
        element = self.__wait_until_element_clickable(locator)
        self._driver.execute_script('arguments[0].click()', element)

    def move_cursor_to_element(self, locator):
        element = self.__wait_until_element_visible(locator)
        actions = ActionChains(self._driver)
        actions.move_to_element(element).perform()

    def scroll_to_element(self, locator):
        retries = 15
        while retries:
            try:
                element = self.__wait_until_element_visible(locator)
                return element
            except ElementNotVisibleException:
                self._driver.execute_script('window.scrollTo(0, 100)')
                retries -= 1

    def check_if_others_tags_is_displayed(self, locator):
        try:
            elements = self._wait.until(EC.presence_of_all_elements_located(locator))
            return len(elements) == 0
        except TimeoutException:
            return True


