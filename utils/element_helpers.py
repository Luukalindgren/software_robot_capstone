from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

def wait_for_element(driver: WebDriver, locator: tuple, timeout: int = 10):
    """Wait for an element to be present."""
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(locator)
    )
