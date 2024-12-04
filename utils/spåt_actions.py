from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define locators as constants
TABLE_LOCATOR = "[data-testid='virtuoso-item-list']"
ROW_LOCATOR = "tr.MuiTableRow-root"
ARENA_SELECTOR_LOCATOR = "div.MuiSelect-multiple"
ARENA_INPUT_LOCATOR_TEMPLATE = "li[data-value='{}']"
FILTER_BUTTON_LOCATOR = "button.css-3ihcqq"
BACKDROP_LOCATOR = "MuiBackdrop-root"
APPLY_BUTTON_LOCATOR_XPATH = "/html/body/div/div/div[1]/main/div[2]/div[2]/div/div[4]/div/button[2]"

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

def loop_through_sessions(driver, arena, session_ids):
    """Loop through sessions and process each"""
    try:
        for session_name in session_ids:
            print(f"Processing session: {session_name}")

            rows = get_table_rows(driver)
            session_row = next(row for row in rows if session_name in row.text)

            session_row.click()
            print(f"Session {session_name} opened!")

            print("Current URL: ", driver.current_url)
            driver.back()

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ROW_LOCATOR)))
            apply_arena_filter(driver, arena)

            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ROW_LOCATOR)))
            rows = get_table_rows(driver)
    except Exception as e:
        print("An error occurred during looping: ", e)

def get_table_rows(driver):
    """Helper function to get all rows from the session table."""
    table = driver.find_element(By.CSS_SELECTOR, TABLE_LOCATOR)
    return table.find_elements(By.CSS_SELECTOR, ROW_LOCATOR)
