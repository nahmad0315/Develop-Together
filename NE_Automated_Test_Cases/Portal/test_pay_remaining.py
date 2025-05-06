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
        # Step 1: Login using the helper method
        self.login(browser)

        # Step 2: Navigate to Place Order
        print("Step 2: Navigating to 'Place Order' section...")
        try:
            place_order_button = WebDriverWait(browser, 20).until(  # Increased timeout
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.placeorder.headerplaceOrder"))
            )
            print("Found Place Order button")
            place_order_button.click()
            print("Clicked Place Order button")
        except Exception as e:
            print("Error finding Place Order button:", str(e))
        print("Current URL:", browser.current_url)
        print("Looking for Place Order button...")
        place_order_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.placeorder.headerplaceOrder"))
        )
        print("Found Place Order button")
        place_order_button.click()

        # Step 3: Fill order details
        print("Step 3: Filling out order title and subject...")
        browser.find_element(By.ID, "title").send_keys(self.TEST_TITLE)

        dropdown = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-1xc3v61-indicatorContainer"))
        )
        dropdown.click()

        subject_select = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), '{self.TEST_SUBJECT}')]"))
        )
        subject_select.click()

        print("Step 4: Clicking 'Next' after subject selection...")
        next_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Next')]]"))
        )
        next_button.click()

        print("Step 5: Adding instructions...")
        instructions_field = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "instruction"))
        )
        instructions_field.clear()
        instructions_field.send_keys(self.TEST_INSTRUCTIONS)

        next_button_2 = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Next')]]"))
        )
        next_button_2.click()

        print("Step 6: Selecting deadline options...")
        deadline_field = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "pkg_deadline_options"))
        )
        deadline_field.click()

        select = Select(deadline_field)
        select.select_by_visible_text("Between 12-24hrs")

        dropdown_2 = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.ID, "deadline_hours"))
        )
        select = Select(dropdown_2)
        select.select_by_visible_text("14hrs")

        print("Step 7: Setting number of pages...")
        pages_field = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.ID, "no_of_pages"))
        )
        pages_field.send_keys(self.TEST_PAGES)

        next_button_3 = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[contains(text(), 'Next')]]"))
        )
        next_button_3.click()

        print("Step 8: Selecting partial payment (25%)...")
        pay_25 = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='partial']"))
        )
        pay_25.click()
        time.sleep(2)

        print("Step 9: Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Complete Your Payment')]"))
        )
        complete_payment_button.click()

        print("Step 11: Selecting wallet payment method...")
        wallet_label = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//label[contains(@class, 'walletSelect')][.//input[@value='yes']]") )
        )
        wallet_label.click()

        print("Step 12: Confirming payment...")
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

    # Test Case: Pay remaining balance after partial payment (wallet)
    def test_pay_remaining_after_partial_payment_wallet(self, browser):
        """
        Test Case: test_pay_remaining_after_partial_payment_wallet
        Description:
        This test verifies the functionality of paying the remaining balance after placing an order with partial payment.
        It first places an order with 25% partial payment via wallet, then completes the remaining 75% payment.

        Steps:
        1. Place order with 25% partial payment (using existing test case logic)
        2. Extract order ID from the order complete page
        3. Click on "Check Your Order Details" button
        4. Click on "Pay Remaining" button (using the most specific selector)
        5. Select wallet as payment method
        6. Confirm the remaining payment
        7. Verify that the 'Place Order' button is displayed (test passes if visible)

        Assertions:
        - Ensures the 'Place Order' button is visible after completing the remaining payment.

        Notes:
        - This test uses Selenium WebDriver for browser automation.
        - WebDriverWait is used to handle dynamic elements and ensure proper synchronization.
        - The test assumes valid credentials and sufficient wallet balance for both partial and remaining payments.
        """
        # Step 1: First place order with partial payment
        self.test_place_order_12_24_hours_partial_payment_wallet(browser)
        
        # # Step 2: Extract order ID from the order complete page
        # print("Step 2: Extracting Order ID from order complete page...")
        # order_id_elem = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
        #     EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'orderdetailsuccessfull')]/span[2]"))
        # )
        # order_id = order_id_elem.text.strip()
        # print(f"Order ID: {order_id}")
        
        # Step 3: Click 'Check Your Order Details' button
        print("Step 3: Clicking 'Check Your Order Details' button...")
        check_details_btn = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a > button.checkout-button"))
        )
        check_details_btn.click()
        
        # Step 4: Click Pay Remaining button (using the most specific selector)
        print("Step 4: Clicking Pay Remaining button...")
        pay_remaining_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.checkout-button.mb-1"))
        )
        pay_remaining_button.click()
        time.sleep(3)
        
        # # Step 5: Select wallet payment method
        # print("Step 5: Selecting wallet payment method...")
        # wallet_option = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
        #     EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        # )
        # wallet_option.click()
        
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
        
        time.sleep(4)# To make sure the screenshot is taken
        # Step 7: Verify 'Place Order' button is displayed
        print("Step 7: Verifying 'Place Order' button is displayed...")
        place_order_btn = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button.placeorder.headerplaceOrder"))
        )
        assert place_order_btn.is_displayed(), "'Place Order' button not visible after payment."
        print("Test Completed: 'Place Order' button is visible. Payment flow successful.")
      