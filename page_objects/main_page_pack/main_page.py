from selenium.webdriver.common.by import By

from utilities.auto_step.auto_step import autostep
from page_objects.product_page_pack.product_page import ProductPage
from utilities.ui_utilities.base_page import BasePage


@autostep
class MainPage(BasePage):
    """
       Page Object class representing the main page of the application.

       This class extends the 'BasePage' class, providing common functionality for interacting with web pages.

       Attributes:
       - driver: The WebDriver instance for interacting with the web page.

       Example:
       main_page = MainPage(driver)
       main_page.set_search_text("water pump").click_search_result()
       """
    def __init__(self, driver):
        """
        Initializes the MainPage instance.

        Parameters:
        - driver: The WebDriver instance for interacting with the web page.
        """
        super().__init__(driver)

    __input_search = (By.XPATH, "//input[@id='search' and @name='q' ]")
    __search_result_locator = (By.XPATH,
                               "//a[@rel='noreferrer' and @href='https://aquapolis.ua/ua/komplekt-vintov-aquant-dlja-prozhektora-08020101-0006-malenkie.html']")

    def set_search_text(self, text):
        """
        Enters the specified text into the search input field.

        Parameters:
        - text: The text to be entered into the search input field.

        Returns:
        - self: The current instance for method chaining.
        """
        self.send_keys(self.__input_search, text)
        return self

    def click_search_result(self):
        """
         Clicks on a specific search result link.

        Returns:
        - ProductPage: An instance of the 'ProductPage' class for further interaction.
        """
        self.click(self.__search_result_locator)
        return ProductPage(self._driver)
