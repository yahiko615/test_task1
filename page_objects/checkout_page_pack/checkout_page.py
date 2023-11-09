from utilities.ui_utilities.base_page import BasePage
from selenium.webdriver.common.by import By


class CheckoutPage(BasePage):
    __checkout_page_title = (By.XPATH, "//span[text()='Оформлення замовлення']")
    __name_of_the_product = (By.XPATH, "(//span[text()[contains(.,'Шуруп')]]) [2]")

    def __init__(self, driver):
        super().__init__(driver)

    def is_checkout_page_shown(self):
        return self.is_displayed(self.__checkout_page_title) and self.is_displayed(self.__name_of_the_product)
