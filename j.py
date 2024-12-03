import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException

# region ***CONSTANT
TIMER = 2  # seconds

# Load environment variables
INSTANCE_URL = os.getenv("INSTANCE_URL")
J_USERNAME = os.getenv("J_USERNAME")
J_PASSWORD = os.getenv("J_PASSWORD")

# Check for missing environment variables
if not INSTANCE_URL or not J_USERNAME or not J_PASSWORD:
    missing_vars = [var for var, val in {"INSTANCE_URL": INSTANCE_URL, "J_USERNAME": J_USERNAME, "J_PASSWORD": J_PASSWORD}.items() if not val]
    print(f">>> Missing required environment variables: {', '.join(missing_vars)}")
    sys.exit(1)

# region ***INIT
# Chrome WebDriver options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")  # Headless mode for GitHub Actions
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")  # Ensure proper rendering

try:
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 60)
except WebDriverException as e:
    print(f"WebDriver initialization failed: {e}")
    sys.exit(1)
# endregion

# region ****FUNCs
def log(msg):
    """Print log messages."""
    print(f">>> {msg}")

def login():
    """Login to ServiceNow instance."""
    try:
        log("Starting login process...")
        driver.get(INSTANCE_URL)
        time.sleep(TIMER)

        # Find login elements
        username_field = driver.find_element(By.ID, "user_name")
        password_field = driver.find_element(By.ID, "user_password")
        submit_btn = driver.find_element(By.ID, "sysverb_login")

        # Enter credentials and submit
        username_field.send_keys(J_USERNAME)
        password_field.send_keys(J_PASSWORD)
        submit_btn.click()

        # Wait for navigation
        wait.until(EC.url_contains(f"{INSTANCE_URL}/now/nav/ui/classic/params/target/ui_page.do"))
        log("Login successful.")
        return True
    except TimeoutException:
        log("Login failed: Page load timeout.")
    except WebDriverException as e:
        log(f"Login failed: WebDriver exception: {e}")
    except Exception as e:
        log(f"Login failed: Unexpected exception: {e}")
    return False
# endregion

# region ****MAIN
def main():
    """Main function to handle login."""
    try:
        if not login():
            log("Login process failed.")
            sys.exit(1)
    finally:
        driver.quit()
        log("Browser session closed.")
# endregion

if __name__ == "__main__":
    main()
