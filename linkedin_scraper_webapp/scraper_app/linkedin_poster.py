from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from .scraper import login_to_linkedin
import time

def post_content_to_linkedin(username, password, post_content):
    print("Happening 2")
    """Posts the generated content to LinkedIn using Selenium."""
    driver = webdriver.Chrome()  # Ensure chromedriver is installed
    try:
        # Login
        login_to_linkedin(driver, username, password)
        print("✅ Successfully logged into LinkedIn for posting")

        # Open Post Box
        # Locate and click the "Start a post" button
        start_post = driver.find_element(By.XPATH, '//*[@id="ember37"]/span')
        driver.execute_script("arguments[0].click();", start_post)
        print("Start Post Button Clicked")

        time.sleep(3)

        # Enter Post Content
        wait = WebDriverWait(driver, 5)  # Wait up to 10 seconds
        post_box = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "ql-editor")))
        print("Open Box")
        post_box.send_keys(post_content)
        print("Send Content")

        time.sleep(2)

        # Click Post Button
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        post_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'share-actions__primary-action')]")))
        # Scroll into view if necessary
        driver.execute_script("arguments[0].scrollIntoView(true);", post_button)
        driver.execute_script("arguments[0].click();", post_button)
        print("✅ Successfully clicked the 'Post' button!")

        time.sleep(5)
        driver.quit()
        return True, "Successfully posted!"

    except Exception as e:
        driver.quit()
        return False, str(e)
