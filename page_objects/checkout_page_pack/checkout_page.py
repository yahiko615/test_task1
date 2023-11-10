import time

from selenium.webdriver.common.by import By

from conftest import auto_step
from utilities.ui_utilities.base_page import BasePage


@auto_step
class CheckoutPage(BasePage):
    """
        Page Object class representing the checkout page of the application.

        This class extends the 'BasePage' class, providing common functionality for interacting with web pages.

        Attributes:
        - driver: The WebDriver instance for interacting with the web page.

        Locators:
        - __checkout_page_title: Locator for the title of the checkout page.
        - __name_of_the_product: Locator for the name of the product on the checkout page.
        - __new_user_tab_active: Locator for the active new user tab.
        - __name_input: Locator for the name input field.
        - __surname_input: Locator for the surname input field.
        - __telephone_input: Locator for the telephone input field.
        - __email_input: Locator for the email input field.
        - __town_select: Locator for the town selection element.
        - __select_input: Locator for the input field in the selection element.
        - __select_option: Locator for the town selection option.
        - __delivery_method_select: Locator for the delivery method selection element.
        - __delivery_method_option: Locator for the delivery method option.
        - __issuing_office_select: Locator for the issuing office selection element.
        - __select_issuing_office_option: Locator for the issuing office option.
        - __payment_method_select: Locator for the payment method selection element.
        - __add_comment: Locator for the add comment element.
        - __comment_textarea: Locator for the comment textarea.

        Methods:
        - __init__: Constructor method to initialize the CheckoutPage instance.
        - verify_checkout_page_opened: Verifies if the checkout page is opened.
        - verify_new_user_tab_active: Verifies if the new user tab is active.
        - set_valid_user_creds: Enters valid user credentials into the corresponding input fields.
        - set_town: Sets the town in the checkout form.
        - select_town_option: Selects the town option in the checkout form.
        - set_delivery_method: Sets the delivery method in the checkout form.
        - set_issuing_office: Sets the issuing office in the checkout form.
        - check_payment_method: Checks the payment method in the checkout form.
        - click_add_comment: Clicks on the add comment element.
        - set_comment: Enters the comment in the comment textarea.

        Example:
        checkout_page = CheckoutPage(driver)
        checkout_page.set_valid_user_creds("Джон", "Дон", "1234567890", "john.doe@example.com") \
                     .set_town("Київ ").select_town_option() \
                     .set_delivery_method().set_issuing_office("Відділення №180 (до 30 кг): просп. Степана Бандери, 8")\
                     .check_payment_method().click_add_comment() \
                     .set_comment("This is a test comment")
        """
    __checkout_page_title = (By.XPATH, "//span[text()='Оформлення замовлення']")
    __name_of_the_product = (By.XPATH, "(//span[text()[contains(.,'Шуруп')]]) [2]")
    __new_user_tab_active = (By.XPATH, "//*[@id='tab-new-client' and .//span[contains(text(), 'Я новий користувач')]]")
    __name_input = (By.XPATH, "//input[@name='firstname']")
    __surname_input = (By.XPATH, "//input[@name='lastname']")
    __telephone_input = (By.XPATH, "//input[@name='telephone']")
    __email_input = (By.XPATH, "//input[@name='username-custom']")
    __town_select = (By.XPATH, "(//span[@class='select2-selection select2-selection--single']) [1]")
    __select_input = (By.XPATH, "(//input[@class='select2-search__field'])")
    __select_option = (By.XPATH, '//li[text()="Київ"]')
    __delivery_method_select = (
        By.XPATH, "(//span[@class='select2-selection select2-selection--single']) [2]")
    __delivery_method_option = (By.XPATH, "//li[@class='s_method_novaposhta_novaposhta_to_warehouse']")
    __issuing_office_select = (By.XPATH, "(//span[@class='select2-selection select2-selection--single']) [3]")
    __select_issuing_office_option = (By.XPATH, '//li[text()="Відділення №180 (до 30 кг): просп. Степана Бандери, 8"]')
    __payment_method_select = (
        By.XPATH, "//span[@class='select2-selection__placeholder' and text()='Готівкою при отриманні']")
    __add_comment = (By.XPATH, "//span[@id='add-comment' and @class='toggle']")
    __comment_textarea = (By.XPATH, "//textarea[@id='order_note' and @name='order_note']")

    # __display_block = (By.XPATH, '//div[@style="display: block;"]')
    # __display_none = (By.XPATH, '//div[@style="display: none;"]')

    def __init__(self, driver):
        """
        Initializes the CheckoutPage instance.

        Parameters:
        - driver: The WebDriver instance for interacting with the web page.
        """
        super().__init__(driver)

    def verify_checkout_page_opened(self):
        """
        Verifies if the checkout page is opened.

        Returns:
        - bool: True if the checkout page is opened, False otherwise.
        """
        return self.is_displayed(self.__checkout_page_title) and self.is_displayed(self.__name_of_the_product)

    def verify_new_user_tab_active(self):
        """
        Verifies if the new user tab is active.

        Returns:
        - bool: True if the new user tab is active, False otherwise.
        """
        return self.is_displayed(self.__new_user_tab_active)

    def set_valid_user_creds(self, name, surname, phone_number, email):
        """
        Enters valid user credentials into the corresponding input fields.

        Parameters:
        - name: The user's first name.
        - surname: The user's last name.
        - phone_number: The user's phone number.
        - email: The user's email address.

        Returns:
        - self: The current instance for method chaining.
        """
        fields = [self.__name_input, self.__surname_input, self.__telephone_input, self.__email_input]
        values = [name, surname, phone_number, email]

        for field, value in zip(fields, values):
            self.send_keys(field, value)

        time.sleep(5)
        return self

    def set_town(self, text):
        """
        Sets the town in the checkout form.

        Parameters:
        - text: The name of the town to be set.

        Returns:
        - self: The current instance for method chaining.
        """
        # //div[@class='loader'] в DOM вечно висит лоадер, при этом расположение на стринце визуально отследить невозможно никаким локатором
        # при загрузке страницы или смене города пока подгружается инфа он появляется визуально
        # но при этом меняется только класс body, и стили display: block / absolute / none
        # пробовал подвязываться на все что угодно, но даже после того как классы в DOM дереве перестают меняться лоадер визуально висит еще
        # пару секунд, а привязка на body который имеет просто огромный изменяющийся class врятле разумная идея из-за огромного селектора
        # и при попытке кликнуть на элемент вылетает ElementClickInterceptedException потому что лоадер перекрывает все,
        # через click_via_JS тоже не работает, так что в итоге вот такие вот костыли в виде time.sleep()
        self.click_via_js(self.__town_select)
        self.send_keys(self.__select_input, text)
        return self

    def select_town_option(self):
        """
        Selects the town option in the checkout form.

        Returns:
         - self: The current instance for method chaining.
        """
        # self.wait_until_element_present(self.__display_block)
        # self.wait_until_element_present(self.__display_none)
        # self.wait_until_element_invisible(self.__display_block)
        time.sleep(8)
        self.click_via_js(self.__select_option)
        return self

    def set_delivery_method(self):
        """
        Sets the delivery method in the checkout form.

        Returns:
        - self: The current instance for method chaining.
        """
        time.sleep(5)
        self.click_via_js(self.__delivery_method_select)
        self.scroll_via_js()
        self.click_via_js(self.__delivery_method_option)
        return self

    def set_issuing_office(self, text):
        """
        Sets the issuing office in the checkout form.

        Parameters:
        - text: The name of the issuing office to be set.

        Returns:
        - self: The current instance for method chaining.
        """
        time.sleep(5)
        self.click_via_js(self.__issuing_office_select)
        self.send_keys(self.__select_input, text)
        time.sleep(5)
        self.press_backspace()
        self.click_via_js(self.__select_issuing_office_option)
        return self

    def check_payment_method(self):
        """
        Checks the payment method in the checkout form.

        Returns:
        - self: The current instance for method chaining.
        """
        self.is_displayed(self.__payment_method_select)
        return self

    def click_add_comment(self):
        """
        Clicks on the add comment element.

        Returns:
        - self: The current instance for method chaining.
        """
        self.click(self.__add_comment)
        return self

    def set_comment(self, name):
        """
        Enters the comment in the comment textarea.

        Parameters:
        - name: The comment to be entered.

        Returns:
        - self: The current instance for method chaining.
        """
        self.send_keys(self.__comment_textarea, name)
        return self
