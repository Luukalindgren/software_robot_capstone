from utils.browser_setup import create_browser
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv

def main():
    driver = create_browser()

    # Access secrets from .env (local) or GitHub Secrets (production)
    if not os.getenv("GITHUB_ACTIONS"):
        load_dotenv()

    username = os.getenv("SPÅT_USERNAME")
    password = os.getenv("SPÅT_PASSWORD")
    url = os.getenv("SPÅT_URL")

    try:
        # Open a website
        driver.get(url)
        print("Website title: ", driver.title)

        # Interact with the page
        driver.find_element(By.NAME, "email").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("Login button clicked!")

        # Wait for some time to ensure actions complete
        time.sleep(5)

        print("Login Successful!")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()