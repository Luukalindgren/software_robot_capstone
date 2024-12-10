from utils.browser_setup import create_browser
from utils.login_actions import login_to_spåt
from utils.spåt_actions import apply_arena_filter, loop_through_sessions, get_session_ids
from utils.config import load_environment_variables
from utils.db_actions import connect_to_db, upload_sessions_to_db

from selenium.webdriver.common.by import By

# TODO:
# - Containerize with Docker
# - Test the GitHub Actions, daily schedule


def main():
    # Selenium bot actions
    arena = "Lähitapiola Raisio"
    download_folder = "temp"

    driver = create_browser()

    # Debugging
    driver.save_screenshot("/home/runner/work/my_project/my_project/screenshot1.png")
    print("Browser created!", driver.page_source)

    load_environment_variables()

    login_to_spåt(driver)

    # Debugging
    driver.save_screenshot("/home/runner/work/my_project/my_project/screenshot2.png")
    print("Logged in!", driver.page_source)

    apply_arena_filter(driver, arena)

    # Debugging
    driver.save_screenshot("/home/runner/work/my_project/my_project/screenshot3.png")
    print("Arena filter applied!", driver.page_source)

    session_ids = get_session_ids(driver)

    loop_through_sessions(driver, arena, session_ids, download_folder)

    # Debugging
    driver.save_screenshot("/home/runner/work/my_project/my_project/screenshot4.png")
    print("Sessions processed!", driver.page_source)

    # Database actions
    client = connect_to_db()
    upload_sessions_to_db(client)

    client.close()
    driver.quit()

if __name__ == "__main__":
    main()