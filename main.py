from utils.browser_setup import create_browser
from utils.login_actions import login_to_spåt
from utils.spåt_actions import apply_arena_filter, loop_through_sessions, get_session_ids
from utils.config import load_environment_variables

from selenium.webdriver.common.by import By


def main():
    arena = "Lähitapiola Raisio"
    download_folder = "temp"

    driver = create_browser()

    load_environment_variables()

    login_to_spåt(driver)

    apply_arena_filter(driver, arena)

    session_ids = get_session_ids(driver)

    loop_through_sessions(driver, arena, session_ids, download_folder)

    print("Current url: ", driver.current_url)

    driver.quit()

if __name__ == "__main__":
    main()