from selenium import webdriver

CHROME = 1
FIREFOX = 2


def create_driver_factory(driver_id, options=None):
    """
     Create a WebDriver instance for the specified browser.

     Args:
         driver_id (int): An identifier for the desired browser (e.g., CHROME or FIREFOX).
         options (dict): Optional browser configuration options.

    Returns:
        WebDriver: An instance of the Selenium WebDriver for the specified browser.

    """
    driver_mapping = {
        CHROME: webdriver.Chrome,
        FIREFOX: webdriver.Firefox
    }
    driver_class = driver_mapping.get(int(driver_id), webdriver.Chrome)
    driver = driver_class(options=options)
    return driver
