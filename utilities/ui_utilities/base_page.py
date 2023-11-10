import time

from selenium.common import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re


class BasePage:
    """
    BasePage class providing common functionality for interacting with web pages.

    Attributes:
    - _driver: The WebDriver instance for interacting with the web page.
    - _wait: WebDriverWait instance for explicit waits.

    """
    def __init__(self, driver):
        """
        Initializes the BasePage instance.

        Parameters:
        - driver: The WebDriver instance for interacting with the web page.
        """
        self._driver = driver
        self._wait = WebDriverWait(self._driver, 60)

    def __wait_until_element_visible(self, locator: tuple):
        """
        Waits until an element identified by the given locator becomes visible.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
        - WebElement: The WebElement once it becomes visible.
        """
        return self._wait.until(EC.visibility_of_element_located(locator))

    def __wait_until_element_invisible(self, locator: tuple):
        """
        Waits until an element identified by the given locator becomes invisible.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
        - bool: True if the element becomes invisible, False otherwise.
        """
        return self._wait.until(EC.invisibility_of_element_located(locator))

    def __wait_until_element_present(self, locator: tuple):
        """
         Waits until at least one element identified by the given locator is present in the DOM.

        Parameters:
         - locator: A tuple representing the locator strategy and value.

        Returns:
        - List[WebElement]: A list of WebElements once they are present.
         """
        return self._wait.until(EC.presence_of_all_elements_located(locator))

    def __wait_until_element_clickable(self, locator: tuple):
        """
        Waits until an element identified by the given locator is clickable.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
        - WebElement: The WebElement once it becomes clickable.
        """
        return self._wait.until(EC.element_to_be_clickable(locator))

    def send_keys(self, locator, value, is_clear=True):
        """
        Enters text into an input field identified by the given locator.

        Parameters:
        - locator: A tuple representing the locator strategy and value.
        - value: The text to be entered.
        - is_clear: Whether to clear the existing text in the input field before entering new text (default is True).

        Returns:
        - None
        """
        element = self.__wait_until_element_visible(locator)
        if is_clear:
            element.clear()
            element.send_keys(Keys.CONTROL + 'a')
        element.send_keys(value)

    def press_enter(self):
        """
        Presses the 'Enter' key on the active element.

        Returns:
        - self
        """
        self._driver.switch_to.active_element.send_keys(Keys.ENTER)
        return self

    def press_backspace(self):
        """
        Presses the 'Backspace' key on the active element.

        Returns:
        - self
        """
        self._driver.switch_to.active_element.send_keys(Keys.BACK_SPACE)
        return self

    def click(self, locator):
        """
        Clicks on the element identified by the given locator.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
        - None
        """
        self.__wait_until_element_clickable(locator).click()

    def is_displayed(self, locator):
        """
        Checks if an element identified by the given locator is displayed.

        Parameters:
         - locator: A tuple representing the locator strategy and value.

         Returns:
        - bool: True if the element is displayed, False otherwise.
         """
        label_element = self.__wait_until_element_visible(locator)
        return label_element.is_displayed()

    def is_not_displayed(self, locator, timeout=10):
        """
        Checks if an element identified by the given locator is not displayed.

        Parameters:
        - locator: A tuple representing the locator strategy and value.
        - timeout: Maximum time to wait for the element to become invisible (default is 10 seconds).

        Returns:
        - bool: True if the element is not displayed within the specified timeout, False otherwise.
        """
        try:
            WebDriverWait(self._driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def get_text(self, locator):
        """
         Retrieves the text content of an element identified by the given locator.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
         - str: The text content of the element.
        """
        element = self.__wait_until_element_visible(locator)
        return element.text

    def get_numeric_price_value(self, locator):
        """
        Retrieves the numeric value of a price element identified by the given locator.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
        - str: The numeric value of the price element.
        """
        element = self.__wait_until_element_visible(locator)
        text = element.text.replace("₴", "").strip()
        return text

    def get_placeholder(self, locator):
        """
         Retrieves the placeholder value of an element identified by the given locator.

         Parameters:
         - locator: A tuple representing the locator strategy and value.

         Returns:
         - str: The placeholder value of the element.
         """
        element = self.__wait_until_element_visible(locator)
        return element.placeholder

    def get_element(self, by, value):
        """
        Retrieves an element identified by the specified method (By) and value.

        Parameters:
        - by: The locator strategy (e.g., By.ID, By.XPATH, By.CSS_SELECTOR).
        - value: The value of the locator.

        Returns:
        - WebElement: The WebElement matching the specified locator.
         """
        element = self.__wait_until_element_visible((by, value))
        return element

    def get_element_by_locator(self, locator):
        """
        Retrieves an element identified by the given locator.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
        - WebElement: The WebElement matching the specified locator.
        """
        element = self.__wait_until_element_visible(locator)
        return element

    def get_element_data_item_qty(self, locator):
        """
         Retrieves the 'data-item-qty' attribute value of an element identified by the given locator.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
        - str: The value of the 'data-item-qty' attribute.
        """
        element = self.__wait_until_element_visible(locator)
        quantity = element.get_attribute("data-item-qty")
        return quantity

    def get_element_style(self, locator):
        """
        Retrieves the 'style' attribute value of an element identified by the given locator.

        Parameters:
        - locator: A tuple representing the locator strategy and value.

        Returns:
        - str: The value of the 'style' attribute.
        """
        element = self.__wait_until_element_visible(locator)
        style = element.get_attribute("style")
        return style

    def click_via_js(self, locator, timeout=10):
        """
        Clicks on an element using JavaScript to ensure it is visible and clickable.

        Parameters:
        - locator: A tuple representing the locator strategy and value.
        - timeout: Maximum time to wait for the element to become clickable (in seconds).

        Returns:
        - None

        """
        try:
            element = self.__wait_until_element_clickable(locator)
            self._driver.execute_script("arguments[0].scrollIntoView(true);", element)
            element.click()
        except NoSuchElementException:
            raise NoSuchElementException(f"Element located by {locator} is not visible or not found.")
        except TimeoutException:
            raise TimeoutException(f"Element located by {locator} was not clickable within {timeout} seconds.")

    def scroll_via_js(self):
        """
        Scrolls the page down by 500 pixels using JavaScript.

        Returns:
        - None
        """
        self._driver.execute_script("window.scrollBy(0, 500);")

    def move_cursor_to_element(self, locator):
        """
        Moves the mouse cursor to the specified web element identified by the given locator.

        This method uses the ActionChains class from Selenium to perform the cursor movement.

        Parameters:
        - locator: A tuple representing the locator strategy and value (e.g., (By.XPATH, "//div[@id='example']")).

        Returns:
        - None

        """
        element = self.__wait_until_element_visible(locator)
        actions = ActionChains(self._driver)
        actions.move_to_element(element).perform()

    def wait_for_element_clickable_and_click(self, locator):
        """
           Waits for an element to be clickable and then clicks it.

           Parameters:
           - locator: A tuple representing the locator strategy and value.

           Raises:
           - ElementClickInterceptedException: If the element is not clickable after the maximum number of retries.

           Returns:
           - None
           """
        max_retries = 15
        retries = 0

        while retries < max_retries:
            try:
                element = self.__wait_until_element_clickable(locator)
                element.click()
                break
            except ElementClickInterceptedException:
                retries += 1
                time.sleep(2)

        if retries == max_retries:
            raise ElementClickInterceptedException("Exceeded maximum retry attempts for ElementClickInterceptedException")
