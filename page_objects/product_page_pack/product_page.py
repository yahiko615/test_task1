from selenium.webdriver.common.by import By

from conftest import auto_step
from page_objects.checkout_page_pack.checkout_page import CheckoutPage
from utilities.ui_utilities.base_page import BasePage


@auto_step
class ProductPage(BasePage):
    """
        Page Object class representing the product page of the application.

        This class extends the 'BasePage' class, providing common functionality for interacting with web pages.

        Attributes:
        - driver: The WebDriver instance for interacting with the web page.

        Locators:
        - __ready_to_dispatch_span: Locator for the span indicating that the product is ready to dispatch.
        - __quantity_input: Locator for the quantity input field on the product page.
        - __buy_product_button: Locator for the "Buy" button on the product page.
        - __minicart_window: Locator for the minicart window on the page.
        - __quantity_in_minicart: Locator for the quantity field in the minicart.
        - __product_price_on_minicart: Locator for the product price in the minicart.
        - __minicart_make_an_order_button: Locator for the "Make an Order" button in the minicart.
        - __checkout_page_title: Locator for the title of the checkout page.
        - __name_of_the_product: Locator for the name of the product on the checkout page.

        Methods:
        - __init__: Constructor method to initialize the ProductPage instance.
        - verify_product_status_is_ready_to_dispatch: Verifies if the product is ready to dispatch.
        - set_quantity: Sets the quantity of the product on the page.
        - click_buy_product: Clicks on the "Buy" button to add the product to the cart.
        - verify_minicart_window_is_open: Verifies if the minicart window is open.
        - verify_minicart_quantity_value: Verifies the quantity value in the minicart.
        - get_product_price_on_minicart: Gets the product price from the minicart.
        - click_make_order: Clicks on the "Make an Order" button in the minicart and navigates to the checkout page.

        Example:
        product_page = ProductPage(driver)
        product_page.set_quantity("5").click_buy_product()
        assert product_page.verify_minicart_window_is_open(), "Minicart window is not open or element not found!"
        assert product_page.verify_minicart_quantity_value() == "5", "Product quantity does not match the entered value"
        total_price = int(env["product_17717_price"]) * int(product_page.verify_minicart_quantity_value())
        assert product_page.get_product_price_on_minicart() == str(total_price), "Total price of the product is wrong"
        checkout_page = product_page.click_make_order()
        assert checkout_page.verify_checkout_page_opened(), "Checkout page isn't shown"
        ```
        """
    def __init__(self, driver):
        """
        Initializes the ProductPage instance.

        Parameters:
        - driver: The WebDriver instance for interacting with the web page.
        """
        super().__init__(driver)

    __ready_to_dispatch_span = (
        By.XPATH, "//div[@class='stock available' and @title='Наявність']/span[text()=' Готовий до відправлення']")
    __quantity_input = (By.XPATH, "//input[@id='qty' and @name='qty']")
    __buy_product_button = (By.XPATH, "//button[@id='product-addtocart-button' and @title='Купити']")
    __minicart_window = (
        By.XPATH, "//div[contains(@class, 'block-minicart') and contains(@class, 'ui-dialog-content')]")
    __quantity_in_minicart = (By.XPATH, "//input[@data-cart-item-id='17717']")
    __product_price_on_minicart = (By.XPATH, "//span[@class='price-wrapper']/span[@class='price']")
    __minicart_make_an_order_button = (By.XPATH, "//button[@id='top-cart-btn-checkout']")
    __checkout_page_title = (By.XPATH, "//span[text()='Оформлення замовлення']")
    __name_of_the_product = (By.XPATH, "(//span[text()[contains(.,'Шуруп')]]) [2]")

    def verify_product_status_is_ready_to_dispatch(self):
        """
        Verifies if the product is ready to dispatch.

        Returns:
        - bool: True if the product is ready to dispatch, False otherwise.
        """
        return self.is_displayed(self.__ready_to_dispatch_span)

    def set_quantity(self, text):
        """
        Sets the quantity of the product on the page.

        Parameters:
        - text: The quantity to be set.

        Returns:
        - self: The current instance for method chaining.
        """
        self.send_keys(self.__quantity_input, text)
        return self

    def click_buy_product(self):
        """
        Clicks on the "Buy" button to add the product to the cart.

        Returns:
        - self: The current instance for method chaining.
        """
        self.click(self.__buy_product_button)
        return self

    def verify_minicart_window_is_open(self):
        """
        Verifies if the minicart window is open.

        Returns:
        - bool: True if the minicart window is open, False otherwise.
        """
        return self.is_displayed(self.__minicart_window)

    def verify_minicart_quantity_value(self):
        """
        Verifies the quantity value in the minicart.

        Returns:
        - str: The quantity value in the minicart.
        """
        return self.get_element_data_item_qty(self.__quantity_in_minicart)

    def get_product_price_on_minicart(self):
        """
        Gets the product price from the minicart.

        Returns:
        - str: The product price in the minicart.
        """
        return self.get_numeric_price_value(self.__product_price_on_minicart)

    def click_make_order(self):
        """
        Clicks on the "Make an Order" button in the minicart and navigates to the checkout page.

         Returns:
        - CheckoutPage: An instance of the CheckoutPage class representing the checkout page.
        """
        self.click(self.__minicart_make_an_order_button)
        return CheckoutPage(self._driver)
