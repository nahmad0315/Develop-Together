import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.gmail_oauth import get_gmail_service
from utils.gmail_services import get_latest_reset_email

class TestForgotPassword:
    
    # Test Case 1: Valid flow for forgot password
    @pytest.mark.usefixtures("browser")
    def test_forgot_password_valid_flow(self, browser):
        """Test forgot password flow with valid email and successful password reset."""

        print("\n[Step 1] Navigating to Login Page...")
        browser.get("https://portal.nerdessay.com/login")

        print("[Step 2] Clicking on 'Forgot Password'...")
        forgot_password_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot password?"))
        )
        forgot_password_button.click()

        print("[Step 3] Entering registered email...")
        email_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        registered_email = "nahmad0313@gmail.com"
        email_field.send_keys(registered_email)

        submit_button = browser.find_element(
            By.XPATH,
            "//button[contains(@class, 'loginbtn') and contains(@class, 'email-btns') and contains(@class, 'buttonhover')]"
        )
        submit_button.click()

        print("[Step 4] Waiting for reset email to arrive...")
        reset_link = None
        attempts = 0
        max_attempts = 10

        while not reset_link and attempts < max_attempts:
            time.sleep(5)
            service = get_gmail_service()
            reset_link = get_latest_reset_email(service)
            attempts += 1

        assert reset_link is not None, "[Error] Reset link was not found in the email after multiple attempts."
        print(f"[Success] Found reset link: {reset_link}")

        print("[Step 5] Navigating to Reset Password Link...")
        browser.get(reset_link)

        print("[Step 6] Setting new password...")
        new_password = "1234567890"

        new_pass_input = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "newPass"))
        )
        confirm_pass_input = browser.find_element(By.ID, "confirmPass")

        new_pass_input.send_keys(new_password)
        confirm_pass_input.send_keys(new_password)

        submit_reset_button = browser.find_element(By.CLASS_NAME, "loginbtn")
        submit_reset_button.click()

        WebDriverWait(browser, 10).until(
            EC.url_contains("/login")
        )
        print("[Step 7] Password reset successful, back to Login page.")

        print("[Step 8] Logging in with the new password...")
        email_input_login = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        password_input_login = browser.find_element(By.ID, "password")

        email_input_login.send_keys(registered_email)
        password_input_login.send_keys(new_password)

        login_button = browser.find_element(By.ID, "buttonText")
        login_button.click()

        print("[Step 9] Verifying successful login...")
       
        # Wait until the "Place Order" button is clickable (i.e., login succeeded)
        WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Place Order')]"))
        )

        time.sleep(2)  # Optional: Wait for a bit to ensure the screenshot is taken after login
        # Now verify if "Place Order" text is present somewhere in the page source
        assert "Place Order" in browser.page_source, "[Error] 'Place Order' not found after login."
        print("[Success] Login with new password successful!")


# Test Case 2: Not Registered email on forgot password
    def test_unregistered_email_forgot_password(self, browser):
        print("Testing forgot password...")

        # Navigate to the login page
        browser.get("https://portal.nerdessay.com/login")

        # Click "Forgot password?"
        forgot_password_button = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.LINK_TEXT, "Forgot password?"))
        )
        forgot_password_button.click()

        # Enter email
        email_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        email_field.send_keys("asdfghj@gmail.com")

        # Click submit
        submit_button = browser.find_element(By.XPATH, "//button[contains(@class, 'loginbtn') and contains(@class, 'email-btns') and contains(@class, 'buttonhover')]")
        submit_button.click()

        # Validate "Your email is not registered." error appears
        print("[Step] Submitting un registered email and checking for error...")
        error_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.error-message"))
        )

        error_text = error_element.text
        print(f"[Info] Error shown: {error_text}")

        time.sleep(2)  # Optional: Wait for a bit to ensure the screenshot is taken
        assert "Your Email is Not Registered." in error_text, "[Error] Mismatch password error not shown."
        print("[Success] Correct error message displayed for Non-registered Email.")


# Test Case 3: Empty password fields during password reset
    @pytest.mark.usefixtures("browser")
    def test_forgot_password_empty_fields(self, browser):
        """
        Validate that an error is shown when both password fields are left empty.
        Expectation: User must be warned to fill the password fields before proceeding.
        """
        print("[Step 1] Navigating to login page...")
        browser.get("https://portal.nerdessay.com/login")

        print("[Step 2] Clicking on 'Forgot Password'...")
        forgot_password_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot password?"))
        )
        forgot_password_button.click()

        print("[Step 3] Submitting forgot password with registered email...")
        email_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        registered_email = "nahmad0313@gmail.com"
        email_field.send_keys(registered_email)

        submit_button = browser.find_element(
            By.XPATH,
            "//button[contains(@class, 'loginbtn') and contains(@class, 'email-btns') and contains(@class, 'buttonhover')]"
        )
        submit_button.click()

        print("[Step 4] Waiting for reset email arrival...")
        reset_link = None
        attempts = 0
        while not reset_link and attempts < 10:
            time.sleep(5)
            service = get_gmail_service()
            reset_link = get_latest_reset_email(service)
            attempts += 1

        assert reset_link is not None, "[Error] Reset link was not found in the email."

        print("[Step 5] Navigating to Reset Password page...")
        browser.get(reset_link)
        
        print("[Step 6] Submitting reset form without entering any passwords...")
        submit_reset_button = browser.find_element(By.CLASS_NAME, "loginbtn")

        # Capture current URL before clicking Submit
        current_url_before = browser.current_url
        submit_reset_button.click()

        # Wait 2 seconds to allow potential page transition
        time.sleep(2)

        # Capture URL after click
        current_url_after = browser.current_url

        print(f"[Info] URL before submit: {current_url_before}")
        print(f"[Info] URL after submit: {current_url_after}")

        # The URL should not change if form validation failed
        assert current_url_before == current_url_after, "[Error] Form submitted despite empty email field."
        print("[Success] Empty password fields prevented form password reset as expected.")
        time

# Test Case 4: Empty email field during forgot password
    @pytest.mark.usefixtures("browser")
    def test_forgot_password_empty_email(self, browser):
        """
        Validate that an error is shown when trying to submit forgot password without email.
        Expectation: User should be warned that email is mandatory.
        """
        print("[Step 1] Navigating to login page...")
        browser.get("https://portal.nerdessay.com/login")

        print("[Step 2] Clicking on 'Forgot Password'...")
        forgot_password_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot password?"))
        )
        forgot_password_button.click()

        print("[Step 3] Clicking submit without entering email...")
        submit_button = browser.find_element(
            By.XPATH,
            "//button[contains(@class, 'loginbtn') and contains(@class, 'email-btns') and contains(@class, 'buttonhover')]"
        )
        # Capture current URL before clicking Submit
        current_url_before = browser.current_url
        submit_button.click()

        # Wait 2 seconds to allow potential page transition
        time.sleep(2)

        # Capture URL after click
        current_url_after = browser.current_url

        print(f"[Info] URL before submit: {current_url_before}")
        print(f"[Info] URL after submit: {current_url_after}")

        # The URL should not change if form validation failed
        assert current_url_before == current_url_after, "[Error] Form submitted despite empty email field."
        print("[Success] Empty email field prevented form submission as expected.")
        time.sleep(2)  # Optional: Wait for a bit to ensure the screenshot is taken

# Test Case 5: Mismatched passwords during password reset
    @pytest.mark.usefixtures("browser")
    def test_forgot_password_mismatched_passwords(self, browser):
        """
        Validate that an error appears when 'New Password' and 'Confirm Password' do not match.
        Expectation: User must match passwords before reset can happen.
        """
        print("[Step 1] Navigating to login page...")
        browser.get("https://portal.nerdessay.com/login")

        print("[Step 2] Clicking 'Forgot Password'...")
        forgot_password_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot password?"))
        )
        forgot_password_button.click()

        print("[Step 3] Submitting forgot password with registered email...")
        email_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        registered_email = "nahmad0313@gmail.com"
        email_field.send_keys(registered_email)
        submit_button = browser.find_element(
            By.XPATH,
            "//button[contains(@class, 'loginbtn') and contains(@class, 'email-btns') and contains(@class, 'buttonhover')]"
        )
        submit_button.click()

        print("[Step 4] Waiting for reset email...")
        reset_link = None
        attempts = 0
        while not reset_link and attempts < 10:
            time.sleep(5)
            service = get_gmail_service()
            reset_link = get_latest_reset_email(service)
            attempts += 1

        assert reset_link is not None, "[Error] Reset link not found."

        print("[Step 5] Navigating to Reset Password page...")
        browser.get(reset_link)

        print("[Step 6] Entering mismatched passwords and submitting...")
        new_pass_input = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "newPass"))
        )
        confirm_pass_input = browser.find_element(By.ID, "confirmPass")
        new_pass_input.send_keys("password123")
        confirm_pass_input.send_keys("password321")

        submit_reset_button = browser.find_element(By.CLASS_NAME, "loginbtn")
        submit_reset_button.click()

        # Validate "Passwords do not match" error appears
        print("[Step] Submitting mismatched passwords and checking for error...")
        error_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.error-message"))
        )

        error_text = error_element.text
        print(f"[Info] Error shown: {error_text}")
        time.sleep(2)# Optional: Wait for a bit to ensure the screenshot is taken

        assert "Passwords do not match" in error_text, "[Error] Mismatch password error not shown."
        print("[Success] Correct error message displayed for mismatched passwords.")


# Test Case 6: Password less than 4 characters
    @pytest.mark.usefixtures("browser")
    def test_forgot_password_short_password(self, browser):
        """
        Validate that an error appears if the password length is less than 4 characters.
        Expectation: Password must meet minimum character requirement.
        """
        print("[Step 1] Navigating to login page...")
        browser.get("https://portal.nerdessay.com/login")

        print("[Step 2] Clicking 'Forgot Password'...")
        forgot_password_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot password?"))
        )
        forgot_password_button.click()

        print("[Step 3] Submitting forgot password with registered email...")
        email_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        registered_email = "nahmad0313@gmail.com"
        email_field.send_keys(registered_email)
        submit_button = browser.find_element(
            By.XPATH,
            "//button[contains(@class, 'loginbtn') and contains(@class, 'email-btns') and contains(@class, 'buttonhover')]"
        )
        submit_button.click()

        print("[Step 4] Waiting for reset email...")
        reset_link = None
        attempts = 0
        while not reset_link and attempts < 10:
            time.sleep(5)
            service = get_gmail_service()
            reset_link = get_latest_reset_email(service)
            attempts += 1

        assert reset_link is not None, "[Error] Reset link not found."

        print("[Step 5] Navigating to Reset Password page...")
        browser.get(reset_link)

        print("[Step 6] Entering a password with less than 4 characters...")
        new_pass_input = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "newPass"))
        )
        confirm_pass_input = browser.find_element(By.ID, "confirmPass")
        new_pass_input.send_keys("123")
        confirm_pass_input.send_keys("123")

        submit_reset_button = browser.find_element(By.CLASS_NAME, "loginbtn")
        submit_reset_button.click()

         # Validate "Passwords do not match" error appears
        print("[Step] Submitting mismatched passwords and checking for error...")
        error_element = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "p.error-message"))
        )

        error_text = error_element.text
        print(f"[Info] Error shown: {error_text}")
        time.sleep(2) # Optional: Wait for a bit to ensure the screenshot is taken
        
        assert "The password field must be at least 8 characters." in error_text, "[Error] Mismatch password error not shown."
        print("[Success] Correct error message displayed for passwords less than 8 characters.")


# Test Case 7: Invalid email format during forgot password
    @pytest.mark.usefixtures("browser")
    def test_forgot_password_invalid_email_format(self, browser):
        """
        Validate that an error is shown for an invalid email format during forgot password.
        Expectation: Email must have proper structure (example@domain.com).
        """
        print("[Step 1] Navigating to login page...")
        browser.get("https://portal.nerdessay.com/login")

        print("[Step 2] Clicking on 'Forgot Password'...")
        forgot_password_button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Forgot password?"))
        )
        forgot_password_button.click()

        print("[Step 3] Entering invalid email format...")
        email_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        invalid_email = "invalidemail"  # No @ symbol
        email_field.send_keys(invalid_email)

        submit_button = browser.find_element(
            By.XPATH,
            "//button[contains(@class, 'loginbtn') and contains(@class, 'email-btns') and contains(@class, 'buttonhover')]"
        )
        # Capture URL after click
        current_url_before = browser.current_url
        submit_button.click()

        # Wait 2 seconds to allow potential page transition
        time.sleep(2)

        # Capture URL after click
        current_url_after = browser.current_url

        print(f"[Info] URL before submit: {current_url_before}")
        print(f"[Info] URL after submit: {current_url_after}")
        time.sleep(2) # Optional: Wait for a bit to ensure the screenshot is taken

        # The URL should not change if form validation failed
        assert current_url_before == current_url_after, "[Error] Form submitted despite empty email field."
        print("[Success] Invalid email prevented form submission as expected.")