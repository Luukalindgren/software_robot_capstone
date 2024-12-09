from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Define locators as constants
TABLE_LOCATOR = "[data-testid='virtuoso-item-list']"
ROW_LOCATOR = "tr.MuiTableRow-root"
ARENA_SELECTOR_LOCATOR = "div.MuiSelect-multiple"
ARENA_INPUT_LOCATOR_TEMPLATE = "li[data-value='{}']"
FILTER_BUTTON_LOCATOR = "button.css-3ihcqq"
BACKDROP_LOCATOR = "MuiBackdrop-root"
APPLY_BUTTON_LOCATOR_XPATH = "/html/body/div/div/div[1]/main/div[2]/div[2]/div/div[4]/div/button[2]"

def get_table_rows(driver):
    """Helper function to get all rows from the session table."""
    table = driver.find_element(By.CSS_SELECTOR, TABLE_LOCATOR)
    return table.find_elements(By.CSS_SELECTOR, ROW_LOCATOR)

def get_session_ids(driver):
    """Extract session IDs from the current page."""
    session_ids = []

    rows = get_table_rows(driver)

    for row in rows:
        session_id = row.text
        session_ids.append(session_id)
        print(f"Session ID: {session_id}")
    
    return session_ids

def apply_arena_filter(driver, arena):
    """Apply the arena filter to the sessions page"""
    try:
        filter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, FILTER_BUTTON_LOCATOR)))
        filter_button.click()

        arena_selector = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ARENA_SELECTOR_LOCATOR)))
        arena_selector.click()

        arena_input_locator = ARENA_INPUT_LOCATOR_TEMPLATE.format(arena)
        arena_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, arena_input_locator)))
        arena_input.click()

        backdrop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, BACKDROP_LOCATOR)))
        backdrop.click()

        apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, APPLY_BUTTON_LOCATOR_XPATH)))
        apply_button.click()
        print("Filter applied!")

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ROW_LOCATOR)))

    except Exception as e:
        print("An error occurred applying the filter: ", e)

def loop_through_sessions(driver, arena, session_ids, download_folder):
    """Loop through sessions and process each"""
    try:
        for session_name in session_ids:
            print(f"Processing session: {session_name}")

            rows = get_table_rows(driver)
            session_row = next(row for row in rows if session_name in row.text)

            session_row.click()
            print(f"Session {session_name} opened!")

            print("Current URL: ", driver.current_url)

            download_session_data(driver, download_folder)

            driver.back()

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ROW_LOCATOR)))
            apply_arena_filter(driver, arena)

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ROW_LOCATOR)))
            rows = get_table_rows(driver)
    except Exception as e:
        print("An error occurred during looping: ", e)

def download_session_data(driver, download_folder):
    """Click the 'Export to Excel' button and download the file."""
    
    if check_if_already_downloaded(driver, download_folder):
        print("Session data already downloaded, skipping...")
        return

    try:
        # Find and wait both 'Export' and 'Delete' buttons
        buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "css-1xoy143")))
        
        # Filter to find the Export to Excel button by its visible text
        export_button = None
        for button in buttons:
            if "Export to Excel" in button.text:
                export_button = button
                break

        # If Export to Excel button is found, click it
        if export_button:
            print("Found 'Export to Excel' button, attempting to click it.")
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(export_button)).click()
            print("Export to Excel button clicked!")
        else:
            print("Error: Export to Excel button not found!")
            return

        downloaded_file = wait_for_download(download_folder)
        if downloaded_file:
            print("Downloaded file: ", downloaded_file)
        else:
            print("Download failed!")
                
    except Exception as e:
        print("Error downloading session data: ", e)

def wait_for_download(download_folder, timeout=30):
    """Wait for the download to finish by checking the download folder."""
    print("Waiting for download to complete...")
    start_time = time.time()

    # Record the initial files in the download folder
    existing_files = set(os.listdir(download_folder))
    
    while time.time() - start_time < timeout:
        # Check for new files in the folder
        files_in_directory = set(os.listdir(download_folder))
        
        # Check if any new files are added to the folder
        new_files = files_in_directory - existing_files
        if new_files:
            print(f"New files detected: {new_files}")
            return new_files  # Return the new files (i.e., the downloaded files)

        time.sleep(1)

    print("Download timed out!")
    return None

def check_if_already_downloaded(driver, download_folder):
    """Check if the session data has already been downloaded"""

    session_id = driver.current_url.split("/")[-1]
    print("Checking if session data already downloaded for session ID:", session_id)

    return f"session_{session_id}_statistics.xlsx" in os.listdir(download_folder)