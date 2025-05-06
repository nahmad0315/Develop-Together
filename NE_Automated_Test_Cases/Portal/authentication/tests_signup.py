import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestSignUp:

    email= "nahmad0313@gmail.com"
# Test Case 1: Valid Sign-Up with Correct Credentials
    def test_signup_valid_email(self, browser):
        """
        Test valid signup flow with correct email and password.
        Verifies success message appears after signup.
        """
        password= "1234567890"
        confirm_password= "1234567890"
        print("\n[Step 1] Navigating to signup page...")
        browser.get("https://portal.nerdessay.com/register")

        print("[Step 2] Entering valid email and password...")
        email_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys(self.email)
        password_field = browser.find_element(By.ID, "password_input")
        password_field.send_keys(password)
        confirm_password_field = browser.find_element(By.ID, "cpassword_input")
        confirm_password_field.send_keys(confirm_password)
        time.sleep(2)  # Optional: Wait for 2 seconds to observe the input

        print("[Step 3] Submitting signup form...")
        submit_button = browser.find_element(By.ID, "submitText")
        submit_button.click()

        print("[Step 4] Verifying signup success...")
        success_message = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".checkEmail h2"))
        ).text

        assert "Please check your inbox" in success_message, "[Error] Success message not found after signup."
        print("[Success] Valid signup completed successfully!")

# Test Case 2: Sign-Up with Short Password
    def test_signup_invalid_password_short(self, browser):
        """
        Test signup with password shorter than 8 characters.
        Verifies that an error message is displayed.
        """
        print("\n[Step 1] Navigating to signup page...")
        browser.get("https://portal.nerdessay.com/register")

        print("[Step 2] Entering valid email and short password...")
        email_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys("testuser_shortpass@example.com")
        password_field = browser.find_element(By.ID, "password_input")
        password_field.send_keys("1234")
        confirm_password_field = browser.find_element(By.ID, "cpassword_input")
        confirm_password_field.send_keys("1234")

        print("[Step 3] Submitting signup form...")
        submit_button = browser.find_element(By.ID, "submitText")
        submit_button.click()

        print("[Step] Waiting for password length error toast...")
        error_toast = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Password should be at least 8 characters long')]")
        )
        )
        # Assertion if the error is displayed
        assert error_toast.is_displayed(), "[Error] Password length validation toast not displayed."
        print("[Success] Password length validation toast displayed correctly!")


# Test Case 3: Sign-Up with Mismatched Passwords
    def test_signup_mismatched_passwords(self, browser):
        """
        Test signup with mismatched password and confirm password fields.
        Verifies that an error message is displayed.
        """
        print("\n[Step 1] Navigating to signup page...")
        browser.get("https://portal.nerdessay.com/register")

        print("[Step 2] Entering mismatched passwords...")
        email_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys("testuser_mismatch@example.com")
        password_field = browser.find_element(By.ID, "password_input")
        password_field.send_keys("Password123")
        confirm_password_field = browser.find_element(By.ID, "cpassword_input")
        confirm_password_field.send_keys("DifferentPassword123")

        print("[Step 3] Submitting signup form...")
        submit_button = browser.find_element(By.ID, "submitText")
        submit_button.click()

        print("[Step 4] Waiting for mismatch password error toast...")
        mismatch_error_toast = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Password and confirm password do not match')]")
        )
        )
        assert mismatch_error_toast.is_displayed(), "[Error] Mismatch password toast not displayed."
        print("[Success] Mismatch password validation toast displayed correctly!")


# Test Case 4: Sign-Up with Empty Password
    def test_signup_empty_password(self, browser):
        """
        Test signup with empty password field.
        Verifies that a field validation error appears.
        """
        print("\n[Step 1] Navigating to signup page...")
        browser.get("https://portal.nerdessay.com/register")

        print("[Step 2] Entering empty password...")
        email_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys("testuser_emptypass@example.com")
        password_field = browser.find_element(By.ID, "password_input")
        password_field.clear()
        confirm_password_field = browser.find_element(By.ID, "cpassword_input")
        confirm_password_field.send_keys("ValidPassword123")

        print("[Step 3] Trying to submit...")
        submit_button = browser.find_element(By.ID, "submitText")
        submit_button.click()

        print("[Step 4] Checking for native field validation...")
        assert not password_field.get_attribute("value"), "[Error] Password field is not empty."
        print("[Success] Empty password was correctly not allowed.")

# Test Case 5: Sign-Up with Empty Confirm Password
    def test_signup_empty_confirm_password(self, browser):
        """
        Test signup with empty confirm password field.
        Verifies that a field validation error appears.
        """
        print("\n[Step 1] Navigating to signup page...")
        browser.get("https://portal.nerdessay.com/register")

        print("[Step 2] Leaving confirm password empty...")
        email_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys("testuser_emptycpass@example.com")
        password_field = browser.find_element(By.ID, "password_input")
        password_field.send_keys("ValidPassword123")
        confirm_password_field = browser.find_element(By.ID, "cpassword_input")
        confirm_password_field.clear()

        print("[Step 3] Trying to submit...")
        submit_button = browser.find_element(By.ID, "submitText")
        submit_button.click()

        print("[Step 4] Waiting for empty password error toast...")
        mismatch_confirm_toast = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Password and confirm password do not match')]")
        )
        )
        assert mismatch_confirm_toast.is_displayed(), "[Error] Confirm password mismatch toast not displayed."
        print("[Success] Empty confirm password validation toast displayed correctly!")


# Test Case 6: Sign-Up with Invalid Email Format
    def test_signup_invalid_email(self, browser): # PROBLEM IN HERE 422 ERROR
        """
        Test signup with invalid email format.
        Verifies that invalid email is rejected.
        """
        print("\n[Step 1] Navigating to signup page...")
        browser.get("https://portal.nerdessay.com/register")

        print("[Step 2] Entering invalid email format...")
        email_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys("invalid-email")

        password_field = browser.find_element(By.ID, "password_input")
        password_field.send_keys("ValidPassword123")
        confirm_password_field = browser.find_element(By.ID, "cpassword_input")
        confirm_password_field.send_keys("ValidPassword123")

        print("[Step 3] Trying to submit...")
        submit_button = browser.find_element(By.ID, "submitText")
        submit_button.click()

        print("[Step 4] Verifying field validation...")
        assert "@" not in email_field.get_attribute("value"), "[Error] Invalid email format accepted."
        print("[Success] Invalid email format was rejected.")

# Test Case 7: Sign-Up with Existing Email
    def test_signup_existing_email(self, browser):
        """
        Test signup using already registered email.
        Verifies duplicate email signup is not allowed.
        """
        print("\n[Step 1] Navigating to signup page...")
        browser.get("https://portal.nerdessay.com/register")

        print("[Step 2] Entering already registered email...")
        email_field = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "email")))
        email_field.send_keys(self.email)   # Use the same email as in test_signup_valid_email. That is class level variable.

        password_field = browser.find_element(By.ID, "password_input")
        password_field.send_keys("ValidPassword123")
        confirm_password_field = browser.find_element(By.ID, "cpassword_input")
        confirm_password_field.send_keys("ValidPassword123")

        print("[Step 3] Trying to submit...")
        submit_button = browser.find_element(By.ID, "submitText")
        submit_button.click()

        print("[Step 4] Waiting for 'email already registered' error toast...")
        existing_email_toast = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), 'This email is already registered. Please log in with your password.')]")
        )
        )
        assert existing_email_toast.is_displayed(), "[Error] Email already registered toast not displayed."
        print("[Success] Email already registered toast displayed correctly!")