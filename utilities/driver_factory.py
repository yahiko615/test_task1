from selenium import webdriver

CHROME = 1
FIREFOX = 2


def create_driver_factory(driver_id, options=None):
    driver_mapping = {
        CHROME: webdriver.Chrome,
        FIREFOX: webdriver.Firefox
    }
    driver_class = driver_mapping.get(int(driver_id), webdriver.Chrome)
    driver = driver_class(options=options)
    return driver
