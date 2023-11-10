# -*- coding: utf-8 -*-

import allure
from flaky import flaky
from page_objects.main_page_pack.main_page import MainPage


@allure.feature('Product Cart Feature')
# @pytest.mark.headless
# сделал тест флаки потому что пришлось добавить time.sleep-ы из-за трудноотслеживаемого лоадинга
# который без time.sleep-ов вызывает ElementClickInterceptedException
@flaky(max_runs=3, min_passes=1)
def test_adding_product_to_cart_valid_data(create_driver_product_cart, env):
    """
    Test case to validate the process of adding a product to the cart with valid data.

    This test performs the following steps:
    1. Searches for a product using the specified keyword.
    2. Clicks on the search result.
    3. Verifies that the product is ready to dispatch.
    4. Sets the quantity of the product and adds it to the cart.
    5. Verifies that the minicart window is open and the quantity and price matches the entered value.
    6. Calculates the total price and verifies it in the minicart.
    7. Clicks on the "Make Order" button, navigating to the checkout page.
    8. Verifies that the checkout page is opened and the new user tab is active.
    9. Provides valid user credentials, selects the town, delivery method, issuing office, and payment method.
    10. Adds a comment to the order.

    Parameters:
    - create_driver_product_cart: Pytest fixture to create a WebDriver for the test.
    - env: Pytest fixture providing environment configuration data.

    Expected result:
    - Product added to the cart.
    """
    driver = create_driver_product_cart

    # Step 1: Search for a product
    search_keyword = "шуруп"
    product_case = MainPage(driver).set_search_text(search_keyword).click_search_result()

    # Step 2: Verify product status
    assert product_case.verify_product_status_is_ready_to_dispatch(), "Product is not ready to dispatch or element not found!"

    # Step 3: Set quantity and add to cart
    quantity_of_the_product = '5'
    product_case.set_quantity(quantity_of_the_product).click_buy_product()

    # Step 4: Verify minicart
    assert product_case.verify_minicart_window_is_open(), "Minicart window is not open or element not found!"
    assert product_case.verify_minicart_quantity_value() == quantity_of_the_product, \
        "Product quantity does not match the entered value"

    # Step 5: Verify total price in minicart
    total_price = int(env["product_17717_price"]) * int(quantity_of_the_product)
    assert product_case.get_product_price_on_minicart() == str(total_price), "Total price of the product is wrong"

    # Step 6: Click on "Make Order" and navigate to the checkout page
    checkout_page = product_case.click_make_order()

    # Step 7: Verify checkout page
    assert checkout_page.verify_checkout_page_opened(), "Checkout page isn't shown"
    assert checkout_page.verify_new_user_tab_active(), "New user tab isn't active"

    # Step 8: Provide user details and select options
    town_name = 'Київ'
    issuing_office_name = 'Відділення №180 (до 30 кг): просп. Степана Бандери, 8'
    comment = 'Test order'
    checkout_page.set_valid_user_creds(env["valid_name"], env["valid_surname"], env["valid_phone_number"],
                                       env["valid_email"])
    checkout_page.set_town(town_name).select_town_option().set_delivery_method() \
        .set_issuing_office(issuing_office_name).check_payment_method()

    # Step 9: Add comment to the order
    checkout_page.click_add_comment().set_comment(comment)
