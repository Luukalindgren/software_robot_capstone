from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def create_browser():
    """Create and return a browser instance."""

    driver_path = os.path.join("drivers", "chromedriver.exe")

    options = Options()
    options.add_argument("--headless")  # Headless mode (no UI)
    options.add_argument("--disable-gpu")  # For better performance
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Initialize the browser
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver
