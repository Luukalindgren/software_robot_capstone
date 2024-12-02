from utils.browser_setup import create_browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        # Use WebDriverWait to ensure elements are loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "root"))
        )
        print("Root element loaded!")

        # Wait for the login form to be ready
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        password_input = driver.find_element(By.NAME, "password")

        # Fill in the login form
        email_input.clear()
        email_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)

        # Wait for the login button to be enabled
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_button.click()
        print("Login button clicked!")

        # Wait for the page to load after login
        WebDriverWait(driver, 50).until(
            EC.url_changes(url)
        )
        print("Page loaded after login!")

        sessions_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "button-sessions"))
        )
        sessions_button.click()
        print("Sessions button clicked!")

    except Exception as e:
        print("An error occurred: ", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()