import json
import os
from contextlib import suppress
from pathlib import Path

import allure
import pytest
from selenium.webdriver.chrome.options import Options

from utilities.driver_factory import create_driver_factory

_screenshot_path = Path.home().joinpath("Downloads")


@pytest.fixture(scope="session", autouse=True)
def env():
    """
        Fixture to load environment configuration from a JSON file.

        This fixture is designed to be used at the session level and is automatically
        invoked before any tests in the session. It loads configuration data from a
        specified JSON file and returns it as a dictionary.

        The JSON file should contain valid JSON-formatted data representing the
        configuration for your test environment.

        Usage:
            In your test module, you can use this fixture as follows:

        Returns:
            dict: A dictionary containing the configuration data loaded from the JSON file.

        """
    config_file = "configurations/env_1.json"
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
    with open(config_path, 'r', encoding='utf-8') as file:
        file_data = file.read()
    json_data = json.loads(file_data)
    return json_data


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
        This hook is called to create a test report object for each test item.

        Parameters:
        - item: The test item.
        - call: The call information.

        Returns:
        - The test report object.

        Note:
        - This hookwrapper allows you to perform actions before and after the actual test run.

        Caution:
        - Modifying the test report can affect the test result and behavior.
        """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def create_driver_for_page(request, env, page_url):
    """
       Fixture for creating a WebDriver instance, navigating to a page, and maximizing the window.

       Parameters:
       - request: The pytest request object.
       - env: The environment configuration.
       - page_url: The URL of the page to navigate to.

       Yields:
       - WebDriver instance.

       Note:
       - The fixture is designed to be used with pytest.
       - It supports an optional marker 'headless' to run the browser in headless mode.
       - The WebDriver instance is yielded to the test function.
       - The fixture ensures that the browser window is maximized.
       - If the associated test fails, a screenshot is attached to the Allure report.

       Usage:
       - Include 'create_driver_for_page' as a fixture in your test function parameters or you can implement it with
       other create_driver fixtures/
       - Use the yielded 'driver' instance to interact with the web page.
       """
    driver_options = Options()
    is_headless = request.node.get_closest_marker("headless")
    if is_headless:
        driver_options.add_argument("--headless")

    env = dict(env)
    driver = create_driver_factory(env["browser_id"], options=driver_options)
    driver.get(page_url)
    driver.maximize_window()
    yield driver
    if request.node.rep_call.failed:
        with suppress(Exception):
            allure.attach(driver.get_screenshot_as_png(),
                          name=request.function.__name__,
                          attachment_type=allure.attachment_type.PNG)
    driver.quit()


@pytest.fixture
def create_driver_product_cart(request, env):
    """
        Fixture for creating a WebDriver instance for a product cart page.

        Parameters:
        - request: The pytest request object.
        - env: The environment configuration.

        Yields:
        - WebDriver instance for the product cart page(main_page).

        Note:
        - This fixture utilizes the 'create_driver_for_page' fixture.
        - The 'app_url' from the 'env' configuration is used as the page URL.
        - Yields the WebDriver instance for interacting with the product cart page.

        Usage:
        - Include 'create_driver_product_cart' as a fixture in your test function parameters.
        - Utilize the yielded 'driver' instance for interactions on the product cart page.

        Example:
        def test_product_cart(create_driver_product_cart):
            # Test logic using the 'driver' instance for the product cart page.
        """
    yield from create_driver_for_page(request, env, env["app_url"])
