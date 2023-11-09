from selenium.webdriver.common.by import By

from page_objects.product_page_pack.product_page import ProductPage
from utilities.ui_utilities.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    __input_search = (By.CSS_SELECTOR, 'input#search[name="q"][placeholder="Пошук по сайту"]')
    __search_result_locator = (By.XPATH,
                               "//li[contains(@class, 'mst-searchautocomplete__item') and .//a[contains(@href, 'https://aquapolis.ua/ua/komplekt-vintov-aquant-dlja-prozhektora-08020101-0006-malenkie.html') and contains(., 'Шуруп Aquant для прожектора 15 мм 08020101-0006')]]")

    def set_search_text(self, text):
        self.send_keys(self.__input_search, text)
        return self

    def click_search_result(self):
        self.click(self.__search_result_locator)
        return ProductPage(self._driver)
