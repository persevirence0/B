import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
from plyer import notification
import random
import pyautogui
import psutil

# Initialize logging for terminal output
logging.basicConfig(level=logging.INFO)

# Initialize Faker for random data generation
fake = Faker()

# Configure the correct path to the Firefox geckodriver (updated path from the second script)
geckodriver_path = r"C:\Users\runneradmin\Desktop\geckodriver.exe"  # Updated path from second code

# Set up the Selenium WebDriver with FirefoxOptions
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")

# Ensure only one instance of FirefoxDriver is created
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=options)

# Function to generate a random email address
def generate_random_email():
    return fake.user_name() + str(random.randint(1000, 9999)) + "@outlook.com"

# Function to generate random name and surname
def generate_random_name():
    first_name = fake.first_name()
    last_name = fake.last_name()
    return first_name, last_name

# Function to scan for buttons and click the first clickable one
def scan_and_click(buttons, timeout=1):
    while True:
        for button_locator in buttons:
            try:
                button = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable(button_locator)
                )
                button.click()
                logging.info(f"Clicked button with locator: {button_locator}")
                return
            except Exception:
                pass  # Button not found or not clickable yet, keep scanning
        time.sleep(1)

# Function to check if Firefox is running
def is_firefox_open():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and 'firefox' in proc.info['name'].lower():
            return True
    return False

# Function to open CMD and run commands
def open_cmd_and_run():
    # Open CMD using the Win + R shortcut
    pyautogui.hotkey('win', 'r')
    time.sleep(1)  # Wait for Run window to open

    # Type 'cmd' and press Enter to open CMD
    pyautogui.write('cmd')
    pyautogui.press('enter')
    time.sleep(1)  # Wait for CMD to open

    # Type the command to start Firefox and press Enter
    pyautogui.write('start firefox')
    pyautogui.press('enter')
    
    time.sleep(3)
    
    # Minimize the CMD window using Win + Down
    pyautogui.hotkey('win', 'down')
    time.sleep(0.5)  # Small delay to ensure window is minimized
    
    time.sleep(2)
    
    # Select the Firefox tab by clicking it
    pyautogui.hotkey('alt', 'tab')  # Alt + Tab to switch to the next window (Firefox)
    time.sleep(1)  # Small delay to make sure Firefox is selected

    # Task: Ensure cursor is on the search bar
    pyautogui.click(500, 80)  # Adjusted coordinates to click on the search bar in Firefox

    # Continuously check if Firefox is open
    while not is_firefox_open():
        time.sleep(1)  # Check every 0.5 seconds

    # Once Firefox is detected, type the AliExpress URL and press Enter
    pyautogui.write('https://www.aliexpress.com/account/index.html')
    pyautogui.press('enter')

try:
    # Task 1-15: The main script flow
    logging.info("1. Opening the Outlook sign-up page.")
    driver.get("https://signup.live.com/signup?lic=1&mkt=fr-be")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "usernameInput"))
    )

    random_email = generate_random_email()
    logging.info(f"2. Generated random email: {random_email}")

    email_input = driver.find_element(By.ID, "usernameInput")
    email_input.send_keys(random_email)

    logging.info("4. Clicking the 'Suivant' button for the email input.")
    next_button = driver.find_element(By.ID, "nextButton")
    next_button.click()

    # (Continuing the existing flow...)

    # Run the second part of the script after Task 17
    logging.info("Starting to run the CMD script to open Firefox and navigate to AliExpress.")
    open_cmd_and_run()

    # Wait for the AliExpress registration page to fully load
    logging.info("Waiting for the AliExpress registration page to load.")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div[2]/div/div[2]/div/div/div[1]/div/div[3]/div[2]/div/span/span[1]/span[1]/input[1]"))
    )
    
    # New Task: Click on the email input field and paste the generated email
    logging.info("Clicking on the email input field and entering the random email.")
    email_input_field = driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div/div[2]/div/div/div[1]/div/div[3]/div[2]/div/span/span[1]/span[1]/input[1]")
    email_input_field.click()
    email_input_field.send_keys(random_email)
    email_input_field.send_keys(u'\ue007')  # Press Enter key
    logging.info("Random email pasted and submitted on AliExpress.")

    # Keeps the browser open until Enter is pressed
    input("Press Enter to close the browser...")

except Exception as e:
    logging.error(f"Failed during AliExpress registration: {e}")

finally:
    logging.info("Closing the browser.")
    driver.quit()
