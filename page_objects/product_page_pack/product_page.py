from selenium.webdriver.common.by import By
from page_objects.checkout_page_pack.checkout_page import CheckoutPage
from utilities.ui_utilities.base_page import BasePage


class ProductPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    __ready_to_dispatch_span = (
    By.XPATH, "//div[@class='stock available' and @title='Наявність']/span[text()=' Готовий до відправлення']")
    __quantity_input = (By.XPATH, "//input[@id='qty' and @name='qty']")
    __buy_product_button = (By.XPATH, "//button[@id='product-addtocart-button' and @title='Купити']")
    __minicart_window = (By.CSS_SELECTOR, "div.block-minicart.ui-dialog-content")
    __quantity_in_minicart = (By.XPATH, "//input[@data-cart-item-id='17717']")
    __product_price_on_minicart = (By.XPATH, "//span[@class='price-wrapper']/span[@class='price']")
    __minicart_make_an_order_button = (By.XPATH, "//button[@id='top-cart-btn-checkout']")
    __checkout_page_title = (By.XPATH, "//span[text()='Оформлення замовлення']")
    __name_of_the_product = (By.XPATH, "(//span[text()[contains(.,'Шуруп')]]) [2]")

    def is_product_ready_to_dispatch(self):
        return self.is_displayed(self.__ready_to_dispatch_span)

    def set_quantity(self, text):
        self.send_keys(self.__quantity_input, text)
        return self

    def click_buy_product(self):
        self.click(self.__buy_product_button)
        return self

    def is_minicart_window_open(self):
        return self.is_displayed(self.__minicart_window)

    def check_minicart_quantity_value(self):
        return self.get_element_data_item_qty(self.__quantity_in_minicart)

    def get_product_price_on_minicart(self):
        return self.get_numeric_price_value(self.__product_price_on_minicart)

    def click_make_order(self):
        self.click(self.__minicart_make_an_order_button)
        return CheckoutPage(self._driver)




