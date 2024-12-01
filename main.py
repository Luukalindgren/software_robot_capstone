from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Chrome setup with headless mode
options = Options()
options.add_argument("--headless")  # Run without a UI
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Path to ChromeDriver
service = Service("/usr/local/bin/chromedriver")  # Update path if needed

driver = webdriver.Chrome(service=service, options=options)

try:
    # Open a website
    driver.get("https://example.com/login")

    # Interact with the page
    driver.find_element(By.ID, "username").send_keys("your_username")
    driver.find_element(By.ID, "password").send_keys("your_password")
    driver.find_element(By.ID, "loginButton").click()

    # Wait for some time to ensure actions complete
    time.sleep(5)

    print("Login Successful!")
finally:
    driver.quit()
