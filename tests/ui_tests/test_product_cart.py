import allure
from page_objects.main_page_pack.main_page import MainPage


@allure.feature('Product Cart Feature')
# @pytest.mark.headless
# @flaky(max_runs=3, min_passes=1)
def test_adding_product_to_cart_valid_data(create_driver_product_cart, env):
    env = dict(env)
    user_name, user_surename, phone, email, product_price = env["valid_name"], env["valid_surname"], env[
        "valid_phone_number"], env["valid_email"], env["product_17717_price"]
    driver = create_driver_product_cart

    search_keyword = "шуруп"
    product_case = MainPage(driver).set_search_text(search_keyword).click_search_result()
    assert product_case.is_product_ready_to_dispatch(), "Product is not ready to dispatch or element not found!"

    quantity_of_the_product = '5'
    product_case.set_quantity(quantity_of_the_product).click_buy_product()
    assert product_case.is_minicart_window_open(), "Minicart window is not open or element not found!"
    assert product_case.check_minicart_quantity_value() == quantity_of_the_product, \
        "Product quantity does not match the entered value"

    total_price = int(product_price) * int(quantity_of_the_product)
    assert product_case.get_product_price_on_minicart() == str(total_price), "Total price of the product is wrong"

    product_case.click_make_order()
    assert product_case.is_checkout_page_shown(), "Checkout page isn't shown"


