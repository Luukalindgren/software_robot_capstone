from selenium import webdriver

from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import os
import chromedriver_autoinstaller

def create_browser():
    """Create and return a browser instance with specified download settings."""

    chromedriver_autoinstaller.install()

    download_folder = os.path.join(os.getcwd(), "temp")

    if not os.path.exists(download_folder):
        print("Creating download folder:", download_folder)
        os.makedirs(download_folder)

    options = Options()
    options.add_argument("--headless")  # Headless mode (no UI)
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-gpu")  # For better performance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", download_folder)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # options.add_argument("--enable-logging")
    # options.add_argument("--v=1")

    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

    return driver
