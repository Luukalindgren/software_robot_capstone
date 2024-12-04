from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def login_to_spåt(driver):
    """Login to Spåt with credentials from environment variables"""
    
    username = os.getenv("SPÅT_USERNAME")
    password = os.getenv("SPÅT_PASSWORD")
    url = os.getenv("SPÅT_URL")

    try:
        driver.get(url)
        print("Website title: ", driver.title)

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "root")))
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "email")))
        password_input = driver.find_element(By.NAME, "password")

        email_input.clear()
        email_input.send_keys(username)
        password_input.clear()
        password_input.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        login_button.click()

        WebDriverWait(driver, 20).until(EC.url_changes(url))

        sessions_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "button-sessions")))
        sessions_button.click()

    except Exception as e:
        print("An error occurred during login: ", e)
