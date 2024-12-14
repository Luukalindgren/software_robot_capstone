from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import os

def create_browser():
    """Create and return a browser instance with specified download settings."""
    
    chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

    download_folder = os.path.join(os.getcwd(), "temp")

    if not os.path.exists(download_folder):
        print("Creating download folder:", download_folder)
        os.makedirs(download_folder)

    options = Options()
    options.add_argument("--headless")  # Headless mode (no UI)
    options.add_argument("--window-size=1920x1080")
    options.add_argument("--disable-gpu")  # For better performance
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certifiate-errors")
    options.add_argument("--disable-dev-shm-usage")

    # options.add_argument("--enable-logging")
    # options.add_argument("--v=1")

    # Set download preferences
    prefs = {
        "download.default_directory": download_folder,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)

    print("Browser options set for download directory:", prefs["download.default_directory"])

    driver = webdriver.Chrome(service=chrome_service, options=options)

    return driver
