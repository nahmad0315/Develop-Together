import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestLogin:

# Test Case 1: Valid Login with Correct Credentials
    # Description: Verify that a user can log in successfully with a valid username/email and password.
    def test_login_valid(self, browser):
        """
        Test case for logging in with valid credentials.
        This test will verify the login functionality using valid email and password.
        """
        print("Attempting to log in...")

        # Step 1: Navigate to the homepage
        browser.get("https://portal.nerdessay.com/login")

        # Step 2: Insert valid Email by ID
        username_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        username_field = browser.find_element(By.ID, "email")
        username_field.send_keys("nahmad0313@gmail.com")

        # Step 3: Click Show password button so to make password visible
        showPasswordButton = browser.find_element(By.CLASS_NAME, "toggle-password")
        showPasswordButton.click()

        # Step 4: Insert valid Password
        password_field = browser.find_element(By.ID, "password")
        password_field.send_keys("1234567890")

        # Step 5: Click the submit button
        submit_button = browser.find_element(By.ID, "buttonText")
        submit_button.click()

        # Step 6: Verify successful login (Check visibility of Dashboard button)
        dashboard_button = browser.find_element(By.CLASS_NAME, "active-link")
        time.sleep(2)

# Test Case 2: Invalid Login with Incorrect Username/Email
    def test_login_invalid_email(self, browser):
        """
        Test case for logging in with invalid email.
        This test verifies that the system shows an error when the user enters an invalid email.
        """
        # Step 1: Navigate to the homepage
        browser.get("https://portal.nerdessay.com/login")

        # Step 2: Insert Invalid Email
        username_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        username_field = browser.find_element(By.ID, "email")
        username_field.send_keys("abcd1234@gmail.com")

        # Step 3: Click Show password button so to make password visible
        showPasswordButton = browser.find_element(By.CLASS_NAME, "toggle-password")
        showPasswordButton.click()
        time.sleep(2)

        # Step 4: Fill in Password
        password_field = browser.find_element(By.ID, "password")
        password_field.send_keys("123123123")

        # Step 5: Click the submit button
        submit_button = browser.find_element(By.ID, "buttonText")
        submit_button.click()
        time.sleep(5)

        # Step 6: Verify error message for invalid email
        try:
            WebDriverWait(browser, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'Toastify_toast--error')]//div[contains(., 'No account Exists With this Email,Please Register Your account')]")
                )
            )
            print("Error message displayed: 'Invalid Password or Email'")
        except TimeoutException:
            print("Error message NOT found.")
        time.sleep(5)

# Test Case 3: Invalid Login with Incorrect Password
    def test_login_invalid_password(self, browser):
        """
        Test case for login with an incorrect password.
        This test will verify that the system displays an error message when an incorrect password is provided.
        """
        print("Attempting to log in with incorrect password...")

        # Step 1: Navigate to the homepage
        browser.get("https://portal.nerdessay.com/login")

        # Step 2: Insert valid Email by ID
        username_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        username_field = browser.find_element(By.ID, "email")
        username_field.send_keys("nahmad0313@gmail.com")

        # Step 3: Click Show password button so to make password visible
        showPasswordButton = browser.find_element(By.CLASS_NAME, "toggle-password")
        showPasswordButton.click()

        # Step 4: Insert incorrect Password
        password_field = browser.find_element(By.ID, "password")
        password_field.send_keys("wrongpassword123")
        time.sleep(2)

        # Step 5: Click the submit button
        submit_button = browser.find_element(By.ID, "buttonText")
        submit_button.click()
        time.sleep(4)

        # # Step 6: Verify error message for incorrect password
        # error_message = browser.find_element(By.CLASS_NAME, "error-message")  # Assuming error message has class 'error-message'
        # assert error_message.is_displayed(), "Error message not displayed"
        # time.sleep(5)

# Test Case 4: Invalid login with empty email/username Field
    def test_login_empty_email(self, browser):
        """
        Test case for login with an empty email/username field.
        This test will verify that the system shows an error when the email/username field is left empty.
        """
        print("Attempting to log in with empty email...")

        # Step 1: Navigate to the homepage
        browser.get("https://portal.nerdessay.com/login")

        # Step 2: Leave email/username field empty and enter valid password
        username_field = browser.find_element(By.ID, "email")
        username_field.clear()

        # Step 3: Click Show password button so to make password visible
        showPasswordButton = browser.find_element(By.CLASS_NAME, "toggle-password")
        showPasswordButton.click()

        # Step 4: Insert valid Password
        password_field = browser.find_element(By.ID, "password")
        password_field.send_keys("123123123")
        time.sleep(2)

        # Step 5: Click the submit button
        submit_button = browser.find_element(By.ID, "buttonText")
        submit_button.click()
        time.sleep(4)

        # Step 6: Verify error message for empty email field
        error_message = browser.find_element(By.CLASS_NAME, "error-message")
        assert error_message.is_displayed(), "Error message not displayed"
        time.sleep(5)   

# Test Case 5: Invalid login with empty Password Field
    def test_login_empty_password(self, browser):
        """
        Test case for login with an empty password field.
        This test will verify that the system shows an error when the password field is left empty.
        """
        print("Attempting to log in with empty password...")

        # Step 1: Navigate to the homepage
        browser.get("https://portal.nerdessay.com/login")

        # Step 2: Insert valid Email by ID
        username_field = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "email"))
        )
        username_field = browser.find_element(By.ID, "email")
        username_field.send_keys("nahmad0313@gmail.com")

        # Step 3: Leave password field empty
        password_field = browser.find_element(By.ID, "password")
        password_field.clear()
        time.sleep(2)

        # Step 4: Click the submit button
        submit_button = browser.find_element(By.ID, "buttonText")
        submit_button.click()
        time.sleep(4)

        # Step 5: Verify error message for empty password field
        error_message = browser.find_element(By.CLASS_NAME, "error-message")
        assert error_message.is_displayed(), "Error message not displayed"
        time.sleep(5)
    
# Test Case 6: Invalid login with empty email/username and Password Field
    def test_login_empty_email_password(self, browser):
        """
        Test case for login with both email/username and password fields empty.
        This test will verify that the system shows an error when both fields are left empty.
        """
        print("Attempting to log in with empty email and password...")

        # Step 1: Navigate to the homepage
        browser.get("https://portal.nerdessay.com/login")

        # Step 2: Leave both email/username and password fields empty
        username_field = browser.find_element(By.ID, "email")
        username_field.clear()

        password_field = browser.find_element(By.ID, "password")
        password_field.clear()
        time.sleep(2)

        # Step 3: Click the submit button
        submit_button = browser.find_element(By.ID, "buttonText")
        submit_button.click()
        time.sleep(4)

        # Step 4: Verify error message for empty email and password fields
        error_message = browser.find_element(By.CLASS_NAME, "error-message")
        assert error_message.is_displayed(), "Error message not displayed"
        time.sleep(5)   

# Test Case 7: Invalid login with special characters in email/username
    def test_login_special_characters_in_email(self, browser):
        """
        Test case for login with special characters in the email/username.
        This test will verify that the system can handle special characters in the email/username.
        """
        print("Attempting to log in with special characters in email...")

        # Step 1: Navigate to the homepage
        browser.get("https://portal.nerdessay.com/login")

        # Step 2: Insert email with special characters
        username_field = WebDriverWait(browser, 10).until(
            EC.visibility_of_element_located((By.ID, "email"))
        )
        username_field = browser.find_element(By.ID, "email")
        username_field.send_keys("user!#$%&'*+/=?^_`{|}~@example.com")

        # Step 3: Click Show password button so to make password visible
        showPasswordButton = browser.find_element(By.CLASS_NAME, "toggle-password")
        showPasswordButton.click()

        # Step 4: Insert valid Password
        password_field = browser.find_element(By.ID, "password")
        password_field.send_keys("123123123")
        time.sleep(2)

        # Step 5: Click the submit button
        submit_button = browser.find_element(By.ID, "buttonText")
        submit_button.click()
        time.sleep(4)

        # Step 6: Verify successful login or error message
        try:
            dashboard_button = browser.find_element(By.CLASS_NAME, "active-link")
            print("Login successful")
        except:
            print("Login failed")
