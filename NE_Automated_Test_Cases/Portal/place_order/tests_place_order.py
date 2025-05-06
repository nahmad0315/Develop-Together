# Standard library imports
import time

# Third-party imports
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# import helper_methods as hm
from helper_methods import (
    login,
    navigate_to_place_order,
    fill_order_details,
    add_instructions,
    select_deadline,
    set_pages,
    select_payment_type,
    insert_calendar_selection,
)


class TestPlaceOrder:
    """
    Test suite for the NerdEssay order placement functionality.
    This class contains test cases for various order scenarios with different:
    - Deadlines (12-24 hours, less than 24 hours)
    - Payment types (partial, full)
    - Payment methods (wallet, Stripe)
    """

    # Timeouts
    WAIT_TIMEOUT = 10
    WAIT_TIMEOUT_LONG = 15
    SCREENSHOT_DELAY = 4

    # TC_PO_01: Within 12 hours deadline, full payment (100%), wallet payment
    def test_place_order_within_12_hours_full_payment_wallet(self, browser):
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "Within 12hrs", "11hrs")
        set_pages(browser)
        select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']")
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)  # To make sure the screenshot is taken

        assert (
            paid_badge.is_displayed()
        ), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # TC_PO_06: Within 12 hours deadline, full payment, Stripe
    def test_place_order_within_12_hours_full_payment_stripe(self, browser):
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "Within 12hrs", "3hrs")
        set_pages(browser)
        select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'SubmitButton') and @type='submit']",
                )
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # TC_PO_03: 12-24 hours deadline, full payment, wallet
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "Between 12-24hrs", "21hrs")
        set_pages(browser)
        select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']")
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)  # To make sure the screenshot is taken

        assert (
            paid_badge.is_displayed()
        ), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # TC_PO_04: 12-24 hours deadline, full payment (100%), Stripe payment
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "Between 12-24hrs", "18hrs")
        set_pages(browser)
        select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'SubmitButton') and @type='submit']",
                )
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # TC_PO_05: More than 24 hrs deadline, full payment via wallet
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "More than 24hrs", "")
        set_pages(browser)
        select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']")
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert (
            paid_badge.is_displayed()
        ), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # TC_PO_06: More than 24 hrs deadline, full payment via stripe
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "More than 24hrs", "")
        set_pages(browser)
        select_payment_type(browser, "full")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'SubmitButton') and @type='submit']",
                )
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # TC_PO_07: Within 12 hours deadline, partial payment (25%), wallet payment & pay remaining wallet
    def test_pay_remaining_wallet_after_partial_payment_wallet_within_12hrs(
        self, browser
    ):
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
        self.test_place_order_within_12_hours_partial_payment_wallet(browser)

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
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        time.sleep(4)  # To make sure the screenshot is taken

        # Step 7: Verify 'Place Order' button is displayed
        print("Step 7: Verifying 'Place Order' button is displayed...")
        place_order_btn = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "button.placeorder.headerplaceOrder")
            )
        )
        assert (
            place_order_btn.is_displayed()
        ), "'Place Order' button not visible after payment."
        print(
            "Test Completed: 'Place Order' button is visible. Payment flow successful."
        )

    # TC_PO_08: Within 12 hours deadline, partial payment (25%) wallet & pay remaining via stripe
    def test_pay_remaining_stripe_after_partial_payment_wallet_within_12hrs(
        self, browser
    ):
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
        self.test_place_order_within_12_hours_partial_payment_wallet(browser)

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
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()

        # Step 16: Verify 'Pay' button is displayed
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'SubmitButton') and @type='submit']",
                )
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # TC_PO_09: 12-24 hours deadline, partial payment (25%), wallet payment
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "Between 12-24hrs", "14hrs")
        set_pages(browser)
        select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 13: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']")
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)  # To make sure the screenshot is taken
        assert (
            paid_badge.is_displayed()
        ), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # TC_PO_10: 12-24 hours deadline, partial payment (25%), Stripe payment
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "Between 12-24hrs", "14hrs")
        set_pages(browser)
        select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'SubmitButton') and @type='submit']",
                )
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # TC_PO_11: Within 12 hours deadline, partial payment (25%), wallet payment
    def test_place_order_within_12_hours_partial_payment_wallet(self, browser):
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "Within 12hrs", "8hrs")
        set_pages(browser)
        select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']")
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)  # To make sure the screenshot is taken

        assert (
            paid_badge.is_displayed()
        ), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")

    # TC_PO_12: Within 12 hours deadline, partial payment (25%), Stripe payment
    def test_place_order_within_12_hours_partial_payment_stripe(self, browser):
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "Within 12hrs", "3hrs")
        set_pages(browser)
        select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'SubmitButton') and @type='submit']",
                )
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # TC_PO_13: More than 24 hrs deadline, partial payment (25%), stripe payment
    def test_place_order_more_than_24_hours_deadline_partial_payment_stripe(
        self, browser
    ):
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "More than 24hrs", "")
        set_pages(browser)
        select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='no']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Waiting for Stripe 'Pay' button...")
        pay_button = WebDriverWait(browser, self.WAIT_TIMEOUT_LONG).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(@class, 'SubmitButton') and @type='submit']",
                )
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert pay_button.is_displayed(), "Pay button not visible or not ready."
        print("Test Successful: Stripe page loaded and Pay button is available.")

    # TC_PO_14: More than 24 hrs deadline, partial payment (25%), wallet payment
    def test_place_order_more_than_24_hours_deadline_partial_payment_wallet(
        self, browser
    ):
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
        login(browser)
        navigate_to_place_order(browser)
        fill_order_details(browser)
        add_instructions(browser)
        select_deadline(browser, "More than 24hrs", "")
        set_pages(browser)
        select_payment_type(browser, "partial")
        print("Clicking 'Complete Your Payment'...")
        complete_payment_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Complete Your Payment')]")
            )
        )
        complete_payment_button.click()
        payment_method = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='yes']"))
        )
        payment_method.click()
        confirm_button = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Confirm')]")
            )
        )
        confirm_button.click()
        print("Step 12: Verifying order complete page loaded...")
        paid_badge = WebDriverWait(browser, self.WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "div.paid_badge img[src='/paid_badge.svg']")
            )
        )
        time.sleep(self.SCREENSHOT_DELAY)
        assert (
            paid_badge.is_displayed()
        ), "Success badge not visible – payment/order may have failed."
        print("Test Completed: Order success confirmed via 'PAID' badge.")
