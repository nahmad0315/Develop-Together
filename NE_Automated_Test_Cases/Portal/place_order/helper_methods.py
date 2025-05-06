# Standard library imports
from datetime import datetime, timedelta
import time

# Third-party imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Local imports
from conftest import browser

"""
Helper methods for the Place Order page of the NerdEssay portal.
These methods include login, navigating to the Place Order section,
filling out order details, adding instructions, selecting deadlines,
setting the number of pages, selecting payment types, and inserting calendar selections.
These methods are designed to be reusable and modular, allowing for easy integration into test cases.
"""

# Test data constants
TEST_EMAIL = "nahmad0313@gmail.com"
TEST_PASSWORD = "1234567890"
TEST_TITLE = "SQA"
TEST_SUBJECT = "Science"
TEST_INSTRUCTIONS = "SQA"
TEST_PAGES = "1"

# Timeouts
WAIT_TIMEOUT = 10
WAIT_TIMEOUT_LONG = 15
SCREENSHOT_DELAY = 4


# Helper method to handle login functionality
def login(
    browser,
    email=None,
    password=None,
    portal_url="https://portal.nerdessay.com/login",
):
    """
    Helper method to handle login functionality.
    Args:
    browser: Selenium WebDriver instance
    email (str, optional): Email to use for login. Defaults to TEST_EMAIL
    password (str, optional): Password to use for login. Defaults to TEST_PASSWORD
    portal_url (str, optional): URL of the portal. Defaults to NerdEssay portal
    Returns:
    None
    """
    print("Step 1: Logging in...")
    browser.get(portal_url)
    # Use default values if not provided
    email = email or TEST_EMAIL
    password = password or TEST_PASSWORD
    username_field = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "email"))
    )
    username_field.send_keys(email)
    password_field = browser.find_element(By.ID, "password")
    password_field.send_keys(password)
    submit_button = browser.find_element(By.ID, "buttonText")
    submit_button.click()
    # Wait for login to complete by waiting for the Place Order button
    WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "button.placeorder.headerplaceOrder")
        )
    )
    print("Login completed successfully")


# Helper: Navigate to Place Order
def navigate_to_place_order(browser):
    print("Navigating to 'Place Order' section...")
    place_order_button = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, "button.placeorder.headerplaceOrder")
        )
    )
    place_order_button.click()


# Helper: Fill order details (title, subject)
def fill_order_details(browser, title=None, subject=None):
    print("Filling out order title and subject...")
    browser.find_element(By.ID, "title").send_keys(title or TEST_TITLE)
    dropdown = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "css-1xc3v61-indicatorContainer"))
    )
    dropdown.click()
    subject_select = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located(
            (By.XPATH, f"//div[contains(text(), '{subject or TEST_SUBJECT}')]")
        )
    )
    subject_select.click()
    next_button = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[span[contains(text(), 'Next')]]")
        )
    )
    next_button.click()


# Helper: Add instructions
def add_instructions(browser, instructions=None):
    print("Adding instructions...")
    instructions_field = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "instruction"))
    )
    instructions_field.clear()
    instructions_field.send_keys(instructions or TEST_INSTRUCTIONS)
    next_button_2 = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[span[contains(text(), 'Next')]]")
        )
    )
    next_button_2.click()


# Helper: Select deadline
def select_deadline(browser, deadline_type, deadline_value):
    print("Selecting deadline options...")
    deadline_field = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable((By.ID, "pkg_deadline_options"))
    )
    deadline_field.click()
    select = Select(deadline_field)
    select.select_by_visible_text(deadline_type)
    if deadline_type == "More than 24hrs":
        insert_calendar_selection(browser, WAIT_TIMEOUT)
        time.sleep(1)  # Give time for overlays/animations to finish
        next_button = WebDriverWait(browser, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[span[contains(text(), 'Next')]]")
            )
        )
        browser.execute_script("arguments[0].scrollIntoView(true);", next_button)
        next_button.click()
    else:
        dropdown_2 = WebDriverWait(browser, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "deadline_hours"))
        )
        select = Select(dropdown_2)
        select.select_by_visible_text(deadline_value)


# Helper: Set number of pages
def set_pages(browser, pages=None):
    print("Setting number of pages...")
    pages_field = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.visibility_of_element_located((By.ID, "no_of_pages"))
    )
    pages_field.send_keys(pages or TEST_PAGES)
    next_button = WebDriverWait(browser, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[span[contains(text(), 'Next')]]")
        )
    )
    next_button.click()


# Helper: Select payment type
def select_payment_type(browser, payment_type):
    print(f"Selecting payment type: {payment_type}...")
    print(f"Received payment_type: '{payment_type}'")
    if payment_type == "partial":
        option_click = WebDriverWait(browser, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='partial']"))
        )
    else:
        option_click = WebDriverWait(browser, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='full']"))
        )
    option_click.click()


# Helper method to insert calendar selection for deadline greater than 24 hours
def insert_calendar_selection(browser, wait_timeout=10):
    """
    Handles selecting a deadline using the calendar UI.
    Selects tomorrow's date and the first available time slot.
    """
    print("Step 7: Selecting deadline using calendar UI...")

    # Remove chat widget iframe completely
    # browser.execute_script('''
    #     var chat = document.querySelector('iframe[title="chat widget"]');
    #     if (chat) { chat.remove(); }
    # ''')

    # Step 1: Open the calendar input field
    date_picker_input = WebDriverWait(browser, wait_timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input.date_picker"))
    )
    date_picker_input.click()
    time.sleep(1)  # Wait for calendar to open

    # Step 2: Calculate the day after tomorrow's date
    day_after_tomorrow = datetime.now() + timedelta(days=2)
    day_after_tomorrow_day = day_after_tomorrow.day
    print(f" Selecting date: {day_after_tomorrow_day}")

    # Step 3: Select the day after tomorrow's date
    date_element = WebDriverWait(browser, wait_timeout).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//div[contains(@class, 'react-datepicker__day') and text()='{day_after_tomorrow_day}']",
            )
        )
    )
    browser.execute_script("arguments[0].scrollIntoView(true);", date_element)
    time.sleep(0.5)
    browser.execute_script("arguments[0].click();", date_element)
    time.sleep(1)  # Wait for time selection to appear

    # Step 4: Select first available time from the dropdown list
    time_option = WebDriverWait(browser, wait_timeout).until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                "//li[contains(@class,'react-datepicker__time-list-item') and not(contains(@class, 'disabled'))]",
            )
        )
    )
    browser.execute_script("arguments[0].click();", time_option)
    time.sleep(1)  # Wait for selection to complete

    # Step 5: Close calendar and verify selection
    browser.execute_script("document.body.click();")
    time.sleep(0.5)
    browser.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    time.sleep(0.5)

    # Verify the final selected value
    selected_value = date_picker_input.get_attribute("value")
    print(f"Final selected value: {selected_value}")
    print("Calendar deadline successfully selected.")
