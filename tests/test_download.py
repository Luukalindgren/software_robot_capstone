# EXAMPLE TEMPLATE FROM CHATGPT
# import os
# from utils.browser_setup import create_browser
# from selenium.webdriver.common.by import By

# def test_download():
#     driver = create_browser()
#     try:
#         driver.get("https://example.com/download")
#         download_button = driver.find_element(By.ID, "download")
#         download_button.click()

#         # Wait and verify file download
#         download_dir = os.path.join(os.getcwd(), "downloads")
#         file_path = os.path.join(download_dir, "example_file.zip")
        
#         # Allow time for the file to download
#         import time
#         time.sleep(5)

#         assert os.path.exists(file_path), "File download failed!"
#         print("File downloaded successfully!")
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     test_download()
