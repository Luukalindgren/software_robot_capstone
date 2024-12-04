# EXAMPLE TEMPLATE FROM CHATGPT
# from utils.browser_setup import create_browser
# from selenium.webdriver.common.by import By

# def test_login():
#     driver = create_browser()
#     try:
#         driver.get("https://example.com/login")
#         driver.find_element(By.ID, "username").send_keys("test_user")
#         driver.find_element(By.ID, "password").send_keys("test_password")
#         driver.find_element(By.ID, "submit").click()

#         # Assert successful login (example condition)
#         assert "Dashboard" in driver.title
#         print("Login test passed!")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     test_login()
