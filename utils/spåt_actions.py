from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import json
import time
import os

# Define locators as constants
TABLE_LOCATOR = "[data-testid='virtuoso-item-list']"
ROW_LOCATOR = "tr.MuiTableRow-root"
ARENA_SELECTOR_LOCATOR = "div.MuiSelect-multiple"
ARENA_INPUT_LOCATOR_TEMPLATE = "li[data-value='{}']"
FILTER_BUTTON_LOCATOR = "button.css-3ihcqq"
BACKDROP_LOCATOR = "div.css-esi9ax"
APPLY_BUTTON_LOCATOR_XPATH = "/html/body/div/div/div[1]/main/div[2]/div[2]/div/div[4]/div/button[2]"

# TODO:
# - Function that uploads the downloaded data to the MongoDB



def get_table_rows(driver):
    """Helper function to get all rows from the session table."""
    try:
        print("Getting table rows...")
        table = driver.find_element(By.CSS_SELECTOR, TABLE_LOCATOR)
        return table.find_elements(By.CSS_SELECTOR, ROW_LOCATOR)
    except Exception as e:
        print("An error occurred getting table rows: ", e)


def get_session_ids(driver):
    """Extract latest three session IDs from the current page."""
    try:
        session_ids = []

        rows = get_table_rows(driver)[:8]

        for row in rows:
            session_id = row.text
            session_ids.append(session_id)
            print(f"Session ID: {session_id}")
        
        return session_ids
    except Exception as e:
        print("An error occurred getting session IDs: ", e)

def apply_arena_filter(driver, arena):
    """Apply the arena filter to the sessions page"""
    try:
        print("Applying arena filter...")
        filter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, FILTER_BUTTON_LOCATOR)))
        filter_button.click()

        arena_selector = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ARENA_SELECTOR_LOCATOR)))
        arena_selector.click()

        arena_input_locator = ARENA_INPUT_LOCATOR_TEMPLATE.format(arena)
        arena_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, arena_input_locator)))
        arena_input.click()

        backdrop = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, BACKDROP_LOCATOR)))
        backdrop.click()
        print("Backdrop clicked!")
        time.sleep(1)

        apply_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, APPLY_BUTTON_LOCATOR_XPATH)))
        apply_button.click()
        print("Filter applied!")

        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ROW_LOCATOR)))

    except Exception as e:
        print("An error occurred applying the filter: ", e)

def loop_through_sessions(driver, arena, session_ids, download_folder):
    """Loop through sessions and process each"""

    try:
        print("Looping through sessions...")
        for session_name in session_ids:
            print(f"Processing session: {session_name}")

            rows = get_table_rows(driver)[:8]
            session_row = next(row for row in rows if session_name in row.text)

            driver.execute_script("arguments[0].click();", session_row)
            print(f"Session {session_name} opened!")

            print("Current URL: ", driver.current_url)

            get_team_id(driver)

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

    existing_files = set(os.listdir(download_folder))
    
    while time.time() - start_time < timeout:
        files_in_directory = set(os.listdir(download_folder))
        
        new_files = files_in_directory - existing_files
        if new_files:
            print(f"New files detected: {new_files}")
            return new_files
        
        time.sleep(1)

    print("Download timed out!")
    return None

def check_if_already_downloaded(driver, download_folder):
    """Check if the session data has already been downloaded"""

    session_id = driver.current_url.split("/")[-1]
    print("Checking if session data already downloaded for session ID:", session_id)

    return f"session_{session_id}_statistics.xlsx" in os.listdir(download_folder)

def get_team_id(driver):
    """
    Fetches authorization token and uses it to do GraphQL query to
    get the team_id of the players in the session.
    With this GraphQL we could also extract all the same data that
    the downloaded excel files contain... Not implemented.
    """

    graphql_url = "https://spat.interjektio.dev/v1/graphql"
    session_id = driver.current_url.split("/")[-1]
    auth_token = driver.get_cookie("Authorization")

    payload = {
        "operationName": "GetSessionPlayerData",
        "variables": {
            "session_id": session_id
        },
        "query": (
                "query GetSessionPlayerData($session_id: Int) {\n"
                "  tag(\n"
                "    where: {tag_assignments: {session_id: {_eq: $session_id}}}\n"
                "    order_by: {tag_id: asc}\n"
                "  ) {\n"
                "    tag_assignments(where: {session_id: {_eq: $session_id}}) {\n"
                "      player {\n"
                "        id\n"
                "        name\n"
                "        team_id\n"
                "        __typename\n"
                "      }\n"
                "    }\n"
                "  }\n"
                "}\n"
            )
        }

    headers = {
        "Authorization": "Bearer Zm9vOmJhcg==",
        "Content-Type": "application/json",
        "Referer": driver.current_url
    }

    cookies = {
        "Authorization": auth_token['value']
    }

    response = requests.post(graphql_url, json=payload, headers=headers, cookies=cookies)

    if response.ok:
        data = response.json()
        team_id = data['data']['tag'][0]['tag_assignments'][0]['player']['team_id']
        print("Team_id: ", team_id)
    else:
        print("Request failed: ", response.status_code, response.text)
