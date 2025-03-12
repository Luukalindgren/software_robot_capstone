from utils.browser_setup import create_browser
from utils.login_actions import login_to_spat
from utils.spat_actions import apply_arena_filter, loop_through_sessions, get_session_ids
from utils.config import load_environment_variables
from utils.db_actions import connect_to_db, upload_sessions_to_db

from selenium.webdriver.common.by import By

# TODO:
# - Containerize with Docker
# - Test the GitHub Actions, daily schedule


def main():
    # Selenium bot actions
    arena_1 = "Lähitapiola Raisio"
    arena_2 = "Areena"
    download_folder = "temp"

    driver = create_browser()

    print("\nBrowser created!", driver.current_url)

    load_environment_variables()

    login_to_spat(driver)

    print("\nLogged in!", driver.current_url)

    # First arena
    apply_arena_filter(driver, arena_1)

    print(f"\nArena filter '{arena_1}' applied!", driver.current_url)

    session_ids = get_session_ids(driver)

    loop_through_sessions(driver, arena_1, session_ids, download_folder)

    print(f"\nSessions from arena '{arena_1}' processed!", driver.current_url)

    # Second arena
    apply_arena_filter(driver, arena_2)

    print(f"\nArena filter '{arena_2}' applied!", driver.current_url)

    session_ids = get_session_ids(driver)

    loop_through_sessions(driver, arena_2, session_ids, download_folder)

    print(f"\nSessions from arena '{arena_2}' processed!", driver.current_url)

    # Database actions
    client = connect_to_db()
    upload_sessions_to_db(client)

    client.close()
    driver.quit()

if __name__ == "__main__":
    main()