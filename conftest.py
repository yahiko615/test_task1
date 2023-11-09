import json
from contextlib import suppress
import os
from pathlib import Path
import allure
import inspect
import pytest
from selenium.webdriver.chrome.options import Options


from utilities.driver_factory import create_driver_factory

_screenshot_path = Path.home().joinpath("Downloads")


def auto_step(cls):
    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if not name.startswith('_'):
            setattr(cls, name, allure.step(method))
    return cls


@pytest.fixture(scope="session", autouse=True)
def env():
    config_file = "configurations/env_1.json"
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), config_file)
    with open(config_path) as file:
        file_data = file.read()
    json_data = json.loads(file_data)
    return json_data


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


def create_driver_for_page(request, env, page_url):
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
    yield from create_driver_for_page(request, env, env["app_url"])




