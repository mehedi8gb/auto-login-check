from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Variables for email, password, and URL
EMAIL = "20-43872-2@student.aiub.edu"  # Replace with the actual email
PASSWORD = "Vqmwtfa3rr##lmp2vrqls3##"        # Replace with the actual password
LOGIN_URL = "https://login.microsoftonline.com/"
CLOSE_BROWSER = False             # Set to True to close the browser after sign-in, False to keep it open

def wait_for_element(driver, by, value, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((by, value)))

def wait_for_element_to_be_clickable(driver, by, value, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.element_to_be_clickable((by, value)))

def find_element_by_value_or_type(driver, value, input_type, timeout=10):
    wait = WebDriverWait(driver, timeout)
    try:
        return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"input[type='{input_type}'][value='{value}']")))
    except TimeoutException:
        return wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"input[type='{input_type}']")))

# Set up the WebDriver (Chrome in this case)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # Open the Microsoft Online login page
    driver.get(LOGIN_URL)
    print("Navigated to Microsoft Online login page")

    # Wait for the email field to be present
    email_field = wait_for_element(driver, By.CSS_SELECTOR, "input[type='email']")
    print("Email field is present")

    # Enter the email
    email_field.send_keys(EMAIL)
    print("Entered email")

    # Click the next button
    next_button = wait_for_element_to_be_clickable(driver, By.CSS_SELECTOR, "input[type='submit']")
    next_button.click()
    print("Clicked next button")

    # Wait for the transition to the password input page
    try:
        password_field = wait_for_element(driver, By.CSS_SELECTOR, "input[type='password']", timeout=20)
        print("Password field is present")
    except TimeoutException:
        print("Timeout waiting for password field")
        driver.quit()
        exit()

    # Enter the password
    password_field.send_keys(PASSWORD)
    print("Entered password")

    # Wait for the sign-in button to be clickable using either value or type condition
    sign_in_button = find_element_by_value_or_type(driver, "Sign in", "submit")
    sign_in_button.click()
    print("Clicked sign-in button")

    # Wait for the login process to complete
    WebDriverWait(driver, 20).until(EC.url_contains("microsoftonline.com"))
    print("Login process completed")

    # Wait for the next page to fully load (optional, adjust as needed)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Next page loaded")

    # Verify login success (optional)
    # You can add additional checks here to ensure login was successful

finally:
    if CLOSE_BROWSER:
        driver.quit()
        print("Browser closed")
    else:
        print("Browser left open")
        # Prevent the script from exiting
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("Script interrupted by user")
            driver.quit()
            print("Browser closed")