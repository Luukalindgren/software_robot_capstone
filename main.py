from utils.browser_setup import create_browser
from utils.find_latest_session import find_latest_session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv

def main():
    driver = create_browser()

    arena = "Lähitapiola Raisio"

    # Access secrets from .env (local) or GitHub Secrets (production)
    if not os.getenv("GITHUB_ACTIONS"):
        load_dotenv()

    login_to_spåt(driver)

    apply_arena_filter(driver, arena)

    session_ids = []

    table = driver.find_element(By.CSS_SELECTOR, "[data-testid='virtuoso-item-list']")
    rows = table.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")

    for row in rows:
        session_id = row.text
        session_ids.append(session_id)
        print(f"Session ID: {session_id}")

    loop_through_sessions(driver, arena, session_ids)

    print("Current url: ", driver.current_url)

    driver.quit()

def login_to_spåt(driver):
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
        WebDriverWait(driver, 20).until(
            EC.url_changes(url)
        )

        sessions_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "button-sessions"))
        )
        sessions_button.click()
        print("Sessions button clicked!")

    except Exception as e:
        print("An error occurred during login: ", e)

def loop_through_sessions(driver, arena, session_ids):
    try:
        for session_name in session_ids:
            print(f"Processing session: {session_name}")

            # Re-query for rows after navigating back
            table = driver.find_element(By.CSS_SELECTOR, "[data-testid='virtuoso-item-list']")
            rows = table.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")

            # Find the row with the corresponding session name
            session_row = next(row for row in rows if session_name in row.text)
            
            # Click on the session to open it
            session_row.click()
            print(f"Session {session_name} opened!")
            
            # IMPLEMENT DOWNLOADING HERE
            # download_session(driver, row)
            
            print("Current url: ", driver.current_url)

            # Go back to the sessions listing page
            driver.back()
            print("Back to session listing page.")

            # Wait for the sessions list to reload
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.MuiTableRow-root"))
            )

            # Reapply the filter (to ensure it's still active)
            apply_arena_filter(driver, arena)

            # Wait for the sessions list to reload
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.MuiTableRow-root"))
            )
            table = driver.find_element(By.CSS_SELECTOR, "[data-testid='virtuoso-item-list']")
            rows = table.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")
    except Exception as e:
        print("An error occurred during looping: ", e)

def apply_arena_filter(driver, arena):
    try:
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-3ihcqq"))
        )
        filter_button.click()

        arena_selector = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.MuiSelect-multiple"))
        )
        arena_selector.click()

        arena_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f"li[data-value='{arena}']"))
        )
        arena_input.click()

        backdrop = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "MuiBackdrop-root"))
        )
        backdrop.click()

        apply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/main/div[2]/div[2]/div/div[4]/div/button[2]"))
        )
        apply_button.click()
        print("Filter applied!")

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.MuiTableRow-root"))
        )
        print("Session rows found!")
    except Exception as e:
        print("An error occurred applying the filter: ", e)

if __name__ == "__main__":
    main()