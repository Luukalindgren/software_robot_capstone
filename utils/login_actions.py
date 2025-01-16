from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def login_to_spåt(driver):
    """Login to Spåt with credentials from environment variables"""
    
    username = os.getenv("SPAT_USERNAME")
    password = os.getenv("SPAT_PASSWORD")
    url = os.getenv("SPAT_URL")

    print("Logging in to Spåt with username:", username)

    try:
        driver.get(url)
        print("Website title: ", driver.title)
        print("Current URL: ", driver.current_url)

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "root")))
        email_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")

        email_input.clear()
        email_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)

        print("Credentials entered")

        login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()
        print("Login button clicked")

        WebDriverWait(driver, 20).until(EC.url_changes(url))

        sessions_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-sessions")))
        sessions_button.click()
        
        print("Sessions button clicked")

    except Exception as e:
        print("An error occurred during login: ", e)
