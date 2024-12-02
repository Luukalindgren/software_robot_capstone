from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def find_latest_session(driver):
    try:
        # Wait for table rows to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.MuiTableRow-root"))
        )

        # Locate all rows
        rows = driver.find_elements(By.CSS_SELECTOR, "tr.MuiTableRow-root")
        latest_session_row = None

        for row in rows:
            # Find the "Arena" cell
            arena_cell = row.find_elements(By.CSS_SELECTOR, "td.MuiTableCell-root")[-2]
            if "Lähitapiola Raisio" in arena_cell.text:
                # Save the first matching row (assuming the table is sorted by date)
                latest_session_row = row
                break

        if not latest_session_row:
            print("No sessions found for 'Lähitapiola Raisio'.")
            return False

        # Click the latest session row
        print("Clicking the latest session...")
        latest_session_row.click()

        print("Latest session found!")

        #return latest_session
    except Exception as e:
        print("Error finding latest session:", e)
        return None
    