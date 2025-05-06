# Standard library imports
from datetime import datetime, timedelta
import time

# Third-party imports
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Local imports
from conftest import browser


class TestPlaceOrder:
    """
    Test suite for the NerdEssay order placement functionality.
    This class contains test cases for various order scenarios with different:
    - Deadlines (12-24 hours, less than 24 hours)
    - Payment types (partial, full)
    - Payment methods (wallet, Stripe)
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
    def login(self, browser, email=None, password=None, portal_url="https://portal.nerdessay.com/login"):
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
        email = email or self.TEST_EMAIL
        password = password or self.TEST_PASSWORD
        username_field = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        username_field.send_keys(email)
        password_field = browser.find_element(By.ID, "password")
        password_field.send_keys(password)
        submit_button = browser.find_element(By.ID, "buttonText")
        submit_button.click()
        # Wait for login to complete by waiting for the Place Order button
        WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.placeorder.headerplaceOrder"))
        )
        print("Login completed successfully")

    # Helper: Navigate to Place Order
    def navigate_to_place_order(self, browser):
        print("Navigating to 'Place Order' section...")
        place_order_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.placeorder.headerplaceOrder"))
        )
        place_order_button.click()

    # Helper: Fill order details (title, subject)
    def fill_order_details(self, browser, title=None, subject=None):
        print("Filling out order title and subject...")
        browser.find_element(By.ID, "title").send_keys(title or self.TEST_TITLE)
        dropdown = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-1xc3v61-indicatorContainer"))
        )
        dropdown.click()
        subject_select = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), '{subject or self.TEST_SUBJECT}')]"))
        )
        subject_select.click()
        next_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Next')]]"))
        )
        next_button.click()

    # Helper: Add instructions
    def add_instructions(self, browser, instructions=None):
        print("Adding instructions...")
        instructions_field = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "instruction"))
        )
        instructions_field.clear()
        instructions_field.send_keys(instructions or self.TEST_INSTRUCTIONS)
        next_button_2 = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Next')]]"))
        )
        next_button_2.click()

    # Helper: Select deadline
    def select_deadline(self, browser, deadline_type, deadline_value):
        print("Selecting deadline options...")
        deadline_field = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "pkg_deadline_options"))
        )
        deadline_field.click()
        select = Select(deadline_field)
        select.select_by_visible_text(deadline_type)
        if deadline_type == "More than 24hrs":
            self.insert_calendar_selection(browser, self.WAIT_TIMEOUT)
            time.sleep(1)  # Give time for overlays/animations to finish
            next_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Next')]]"))
            )
            browser.execute_script("arguments[0].scrollIntoView(true);", next_button)
            next_button.click()
        else:
            dropdown_2 = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "deadline_hours"))
            )
            select = Select(dropdown_2)
            select.select_by_visible_text(deadline_value)

    # Helper: Set number of pages
    def set_pages(self, browser, pages=None):
        print("Setting number of pages...")
        pages_field = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "no_of_pages"))
        )
        pages_field.send_keys(pages or self.TEST_PAGES)
        next_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Next')]]"))
        )
        next_button.click()

    # Helper: Select payment type
    def select_payment_type(self, browser, payment_type):
        print(f"Selecting payment type: {payment_type}...")
        print(f"Received payment_type: '{payment_type}'")
        if payment_type == "partial":
            option_click = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='partial']"))
            )
        else:
            option_click = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='full']"))
            )
        option_click.click()

    # Helper method to insert calendar selection for deadline greater than 24 hours
    def insert_calendar_selection(self, browser, wait_timeout=10):
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
            EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'react-datepicker__day') and text()='{day_after_tomorrow_day}']"))
        )
        browser.execute_script("arguments[0].scrollIntoView(true);", date_element)
        time.sleep(0.5)
        browser.execute_script("arguments[0].click();", date_element)
        time.sleep(1)  # Wait for time selection to appear

        # Step 4: Select first available time from the dropdown list
        time_option = WebDriverWait(browser, wait_timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//li[contains(@class,'react-datepicker__time-list-item') and not(contains(@class, 'disabled'))]"))
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

    # Test Case 01: 12-24 hours deadline, partial payment (25%), wallet payment
    def test_place_order_12_24_hours_partial_payment_wallet(self, browser):
        """
        Test Case: test_place_order_12_24_hours_partial_payment_wallet
        Description:
        This test verifies the functionality of placing an order with a deadline between 12-24 hours,
        selecting partial payment (25%), and using the wallet as the payment method. It ensures that the order
        process completes successfully and the "PAID" badge is displayed on the confirmation page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Between 12-24hrs and 14hrs).
        7. Set the number of pages for the order.
        8. Select the partial payment option (25%).
        9. Click "Complete Your Payment."
        10. Choose the wallet as the payment method.
        11. Confirm the payment.
        12. Verify that the "PAID" badge is displayed on the order confirmation page.

        Assertions:
        - Ensures the "PAID" badge is visible on the confirmation page, indicating a successful order placement.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for payment.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "Between 12-24hrs", "14hrs")
        self.set_pages(browser)
        self.select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 13: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']"))
        )
        time.sleep(self.SCREENSHOT_DELAY) # To make sure the screenshot is taken
        assert paid_badge.is_displayed(), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # Test Case 02: 12-24 hours deadline, partial payment (25%), Stripe payment
    def test_place_order_12_24_hours_partial_payment_stripe(self, browser):
        """
        Test Case: test_place_order_12_24_hours_partial_payment_stripe
        Description:
        This test verifies the functionality of placing an order with a deadline between 12-24 hours,
        selecting partial payment (25%), and using Stripe as the payment method. It ensures that the order
        process completes successfully and redirects to the Stripe payment page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Between 12-24hrs and 14hrs).
        7. Set the number of pages for the order.
        8. Select the partial payment option (25%).
        9. Click "Complete Your Payment."
        10. Choose "No" to proceed with Stripe payment.
        11. Confirm the payment.
        12. Verify that the Stripe payment page is loaded with the Pay button.

        Assertions:
        - Ensures the Stripe Pay button is visible and clickable.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test verifies the successful redirection to Stripe but does not complete the actual payment.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "Between 12-24hrs", "14hrs")
        self.set_pages(browser)
        self.select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'SubmitButton') and @type='submit']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # Test Case 03: 12-24 hours deadline, full payment (100%), wallet payment
    def test_place_order_12_24_hours_full_payment_wallet(self, browser):
        """
        Test Case: test_place_order_12_24_hours_full_payment_wallet
        Description:
        This test verifies the functionality of placing an order with a deadline between 12-24 hours,
        selecting full payment, and using the wallet as the payment method. It ensures that the order
        process completes successfully and the "PAID" badge is displayed on the confirmation page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Between 12-24hrs and 21hrs).
        7. Set the number of pages for the order.
        8. Select the full payment option.
        9. Click "Complete Your Payment."
        10. Choose the wallet as the payment method.
        11. Confirm the payment.
        12. Verify that the "PAID" badge is displayed on the order confirmation page.

        Assertions:
        - Ensures the "PAID" badge is visible on the confirmation page, indicating a successful order placement.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for payment.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "Between 12-24hrs", "21hrs")
        self.set_pages(browser)
        self.select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)  # To make sure the screenshot is taken
        
        assert paid_badge.is_displayed(), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # Test Case 04: 12-24 hours deadline, full payment (100%), Stripe payment
    def test_place_order_12_24_hours_full_payment_stripe(self, browser):
        """
        Test Case: test_place_order_12_24_hours_full_payment_stripe
        Description:
        This test verifies the functionality of placing an order with a deadline between 12-24 hours,
        selecting full payment, and using Stripe as the payment method. It ensures that the order
        process completes successfully and redirects to the Stripe payment page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Between 12-24hrs and 18hrs).
        7. Set the number of pages for the order.
        8. Select the full payment option.
        9. Click "Complete Your Payment."
        10. Choose "No" to proceed with Stripe payment.
        11. Confirm the payment.
        12. Verify that the Stripe payment page is loaded with the Pay button.

        Assertions:
        - Ensures the Stripe Pay button is visible and clickable.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test verifies the successful redirection to Stripe but does not complete the actual payment.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "Between 12-24hrs", "18hrs")
        self.set_pages(browser)
        self.select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'SubmitButton') and @type='submit']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # Test Case 05: Less than 24 hours deadline, partial payment (25%), wallet payment
    def test_place_order_less_than_24_hours_partial_payment_wallet(self, browser):
        """
        Test Case: test_place_order_less_than_24_hours_partial_payment_wallet
        Description:
        This test verifies the functionality of placing an order with a deadline of less than 24 hours (8hrs),
        selecting partial payment (25%), and using the wallet as the payment method. It ensures that the order
        process completes successfully and the "PAID" badge is displayed on the confirmation page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Within 12hrs and 8hrs).
        7. Set the number of pages for the order.
        8. Select the partial payment option (25%).
        9. Click "Complete Your Payment."
        10. Choose the wallet as the payment method.
        11. Confirm the payment.
        12. Verify that the "PAID" badge is displayed on the order confirmation page.

        Assertions:
        - Ensures the "PAID" badge is visible on the confirmation page, indicating a successful order placement.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for payment.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "Within 12hrs", "8hrs")
        self.set_pages(browser)
        self.select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)  # To make sure the screenshot is taken

        assert paid_badge.is_displayed(), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # Test Case 06: Less than 24 hours deadline, full payment (100%), wallet payment
    def test_place_order_less_than_24_hours_full_payment_wallet(self, browser):
        """
        Test Case: test_place_order_less_than_24_hours_full_payment_wallet
        Description:
        This test verifies the functionality of placing an order with a deadline of less than 24 hours (11hrs),
        selecting full payment, and using the wallet as the payment method. It ensures that the order
        process completes successfully and the "PAID" badge is displayed on the confirmation page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Within 12hrs and 11hrs).
        7. Set the number of pages for the order.
        8. Select the full payment option.
        9. Click "Complete Your Payment."
        10. Choose the wallet as the payment method.
        11. Confirm the payment.
        12. Verify that the "PAID" badge is displayed on the order confirmation page.

        Assertions:
        - Ensures the "PAID" badge is visible on the confirmation page, indicating a successful order placement.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for payment.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "Within 12hrs", "11hrs")
        self.set_pages(browser)
        self.select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)  # To make sure the screenshot is taken

        assert paid_badge.is_displayed(), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # Test Case 07: Less than 24 hours deadline, full payment (100%), Stripe payment
    def test_place_order_less_than_24_hours_full_payment_stripe(self, browser):
        """
        Test Case: test_place_order_less_than_24_hours_full_payment_stripe
        Description:
        This test verifies the functionality of placing an order with a deadline of less than 24 hours (3hrs),
        selecting full payment, and using Stripe as the payment method. It ensures that the order
        process completes successfully and redirects to the Stripe payment page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Within 12hrs and 3hrs).
        7. Set the number of pages for the order.
        8. Select the full payment option.
        9. Click "Complete Your Payment."
        10. Choose "No" to proceed with Stripe payment.
        11. Confirm the payment.
        12. Verify that the Stripe payment page is loaded with the Pay button.

        Assertions:
        - Ensures the Stripe Pay button is visible and clickable.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test verifies the successful redirection to Stripe but does not complete the actual payment.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "Within 12hrs", "3hrs")
        self.set_pages(browser)
        self.select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'SubmitButton') and @type='submit']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # Test Case 08: Less than 24 hours deadline, partial payment (25%), Stripe payment
    def test_place_order_less_than_24_hours_partial_payment_stripe(self, browser):
        """
        Test Case: test_place_order_less_than_24_hours_partial_payment_stripe
        Description:
        This test verifies the functionality of placing an order with a deadline of less than 24 hours (3hrs),
        selecting partial payment (25%), and using Stripe as the payment method. It ensures that the order
        process completes successfully and redirects to the Stripe payment page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Within 12hrs and 3hrs).
        7. Set the number of pages for the order.
        8. Select the partial payment option (25%).
        9. Click "Complete Your Payment."
        10. Choose "No" to proceed with Stripe payment.
        11. Confirm the payment.
        12. Verify that the Stripe payment page is loaded with the Pay button.

        Assertions:
        - Ensures the Stripe Pay button is visible and clickable.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test verifies the successful redirection to Stripe but does not complete the actual payment.
        - The test verifies partial payment (25%) functionality with Stripe integration.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "Within 12hrs", "3hrs")
        self.set_pages(browser)
        self.select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'SubmitButton') and @type='submit']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # Test Case 09: More than 24 hrs deadline, partial payment (25%), stripe payment
    def test_place_order_more_than_24_hours_deadline_partial_payment_stripe(self, browser):
        """
        Test Case: test_place_order_more_than_24_hours_deadline_partial_payment_stripe
        Description:
        This test verifies the functionality of placing an order with a deadline of more than 24 hours,
        selecting partial payment (25%), and using Stripe as the payment method. It ensures that the order
        process completes successfully and redirects to the Stripe payment page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options ("More than 24hrs") and use the calendar to pick the date and time.
        7. Set the number of pages for the order.
        8. Select the partial payment option (25%).
        9. Click "Complete Your Payment."
        10. Choose "No" to proceed with Stripe payment.
        11. Confirm the payment.
        12. Verify that the Stripe payment page is loaded with the Pay button.

        Assertions:
        - Ensures the Stripe Pay button is visible and clickable, indicating successful redirection to Stripe.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test verifies the successful redirection to Stripe but does not complete the actual payment.
        - The test verifies partial payment (25%) functionality with Stripe integration for deadlines greater than 24 hours.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "More than 24hrs", "")
        self.set_pages(browser)
        self.select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'SubmitButton') and @type='submit']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # Test Case 10: More than 24 hrs deadline, partial payment (25%), wallet payment
    def test_place_order_more_than_24_hours_deadline_partial_payment_wallet(self, browser):
        """
        Test Case: test_place_order_more_than_24_hours_deadline_partial_payment_wallet
        Description:
        This test verifies the functionality of placing an order with a deadline of more than 24 hours,
        selecting partial payment (25%), and using the wallet as the payment method. It ensures that the order
        process completes successfully and the "PAID" badge is displayed on the confirmation page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options ("More than 24hrs") and use the calendar to pick the date and time.
        7. Set the number of pages for the order.
        8. Select the partial payment option (25%).
        9. Click "Complete Your Payment."
        10. Choose "Yes" to use the wallet for payment.
        11. Confirm the payment.
        12. Verify that the "PAID" badge is displayed on the order confirmation page.

        Assertions:
        - Ensures the "PAID" badge is visible on the confirmation page, indicating a successful order placement.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for payment.
        - The test verifies partial payment (25%) functionality with wallet integration for deadlines greater than 24 hours.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "More than 24hrs", "")
        self.set_pages(browser)
        self.select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert paid_badge.is_displayed(), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # Test Case 11: More than 24 hrs deadline, full payment, stripe payment
    def test_place_order_more_than_24_hours_deadline_full_payment_stripe(self, browser):
        """
        Test Case: test_place_order_more_than_24_hours_deadline_full_payment_stripe
        Description:
        This test verifies the functionality of placing an order with a deadline of more than 24 hours,
        selecting full payment, and using Stripe as the payment method. It ensures that the order
        process completes successfully and redirects to the Stripe payment page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options ("More than 24hrs") and use the calendar to pick the date and time.
        7. Set the number of pages for the order.
        8. Select the full payment option.
        9. Click "Complete Your Payment."
        10. Choose "No" to proceed with Stripe payment.
        11. Confirm the payment.
        12. Verify that the Stripe payment page is loaded with the Pay button.

        Assertions:
        - Ensures the Stripe Pay button is visible and clickable, indicating successful redirection to Stripe.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test verifies the successful redirection to Stripe but does not complete the actual payment.
        - The test verifies full payment functionality with Stripe integration for deadlines greater than 24 hours.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "More than 24hrs", "")
        self.set_pages(browser)
        self.select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'SubmitButton') and @type='submit']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # Test Case 12: More than 24 hrs deadline, full payment, wallet payment
    def test_place_order_more_than_24_hours_deadline_full_payment_wallet(self, browser):
        """
        Test Case: test_place_order_more_than_24_hours_deadline_full_payment_wallet
        Description:
        This test verifies the functionality of placing an order with a deadline of more than 24 hours,
        selecting full payment, and using the wallet as the payment method. It ensures that the order
        process completes successfully and the "PAID" badge is displayed on the confirmation page.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options ("More than 24hrs") and use the calendar to pick the date and time.
        7. Set the number of pages for the order.
        8. Select the full payment option.
        9. Click "Complete Your Payment."
        10. Choose "Yes" to use the wallet for payment.
        11. Confirm the payment.
        12. Verify that the "PAID" badge is displayed on the order confirmation page.

        Assertions:
        - Ensures the "PAID" badge is visible on the confirmation page, indicating a successful order placement.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for payment.
        - The test verifies full payment functionality with wallet integration for deadlines greater than 24 hours.
        """
        self.login(browser)
        self.navigate_to_place_order(browser)
        self.fill_order_details(browser)
        self.add_instructions(browser)
        self.select_deadline(browser, "More than 24hrs", "")
        self.set_pages(browser)
        self.select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert paid_badge.is_displayed(), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # Test Case 13: Less than 24 hours deadline, partial payment (25%), wallet payment & pay remaining wallet 
    def test_pay_remaining_wallet_after_partial_payment_wallet_less_than_24hrs(self, browser):
        """
        Test Case: test_pay_remaining_wallet_after_partial_payment_wallet_less_than_24hrs
        Description:
        This test verifies the functionality of paying the remaining balance through wallet after placing an order with partial payment through wallet.
        It first places an order with 25% partial payment via wallet, then completes the remaining 75% payment via wallet.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Within 12hrs).
        7. Place order with 25% partial payment.
        8. Extract order ID from the order complete page
        9. Click on "Check Your Order Details" button
        10. Click on "Pay Remaining" button (using the most specific selector)
        11. Select wallet as payment method
        12. Confirm the remaining payment
        13. Verify that the 'Place Order' button is displayed (test passes if visible)

        Assertions:
        - Ensures the 'Place Order' button is visible after completing the remaining payment.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for both partial and remaining payments.
        """
        # Step 1: First place order with partial payment
        self.test_place_order_less_than_24_hours_partial_payment_wallet(browser)
        
        # Step 3: Click 'Check Your Order Details' button
        print("Step 3: Clicking 'Check Your Order Details' button...")
        check_details_btn = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a > button.checkout-button"))
        )
        check_details_btn.click()
        time.sleep(6)
        
        # Step 4: Click Pay Remaining button
        print("Step 4: Clicking Pay Remaining button...")
        pay_remaining_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.checkout-button.mb-1"))
        )
        pay_remaining_button.click()
        time.sleep(3)
        
        # Step 5: Select wallet payment method
        # print("Step 5: Selecting wallet payment method...")        
        wallet_option = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='yes']"))
        )
        browser.execute_script("arguments[0].click();", wallet_option)
        time.sleep(3)

        # Step 6: Confirm remaining payment
        print("Step 6: Confirming remaining payment...")
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()
        time.sleep(4)   # To make sure the screenshot is taken
        
        # Step 7: Verify 'Place Order' button is displayed
        print("Step 7: Verifying 'Place Order' button is displayed...")
        place_order_btn = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.placeorder.headerplaceOrder"))
        )
        assert place_order_btn.is_displayed(), "'Place Order' button not visible after payment."
        print("Test Completed: 'Place Order' button is visible. Payment flow successful.")
       
        # Test Case 14: Less than 24 hours deadline, partial payment (25%) wallet & pay remaining via stripe
    def test_pay_remaining_stripe_after_partial_payment_wallet_less_than_24hrs(self, browser):
        """
        Test Case: test_pay_remaining_stripe_after_partial_payment_wallet_less_than_24hrs
        Description:
        This test verifies the functionality of paying the remaining balance through Stripe after placing an order with partial payment through wallet.
        It first places an order with 25% partial payment via wallet, then completes the remaining 75% payment via Stripe.

        Steps:
        1. Log in to the portal using valid credentials.
        2. Navigate to the "Place Order" section.
        3. Fill out the order title and select the subject.
        4. Click "Next" after selecting the subject.
        5. Add instructions for the order.
        6. Select deadline options (Within 12hrs).
        7. Place order with 25% partial payment.
        8. Click on "Check Your Order Details" button
        9. Click on "Pay Remaining" button
        10. Select "No" for Stripe as payment method
        11. Click Confirm
        12. Verify that the 'Pay' button is displayed (test passes if visible)

        Assertions:
        - Ensures the 'Pay' button is visible after completing the remaining payment.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for both partial and remaining payments.
        """
        # Step 1: First place order with partial payment
        self.test_place_order_less_than_24_hours_partial_payment_wallet(browser)
        
        # Step 13: Click 'Check Your Order Details' button
        print("Step 3: Clicking 'Check Your Order Details' button...")
        check_details_btn = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a > button.checkout-button"))
        )
        check_details_btn.click()
        time.sleep(6)
        
        # Step 14: Click Pay Remaining button
        print("Step 4: Clicking Pay Remaining button...")
        pay_remaining_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.checkout-button.mb-1"))
        )
        pay_remaining_button.click()
        time.sleep(3)

        # Step 15: Select Stripe payment method
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Confirm')]"))
        )
        confirm_button.click()

        # Step 16: Verify 'Pay' button is displayed
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'SubmitButton') and @type='submit']"))
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    
