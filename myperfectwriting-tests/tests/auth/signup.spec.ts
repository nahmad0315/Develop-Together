import { test, expect } from "@playwright/test";
import { SignUpPage } from "../../pages/SignUpPage";
import { getVerificationLink } from "../../utils/gmailHelper";

test.setTimeout(120_000); // 2 minutes

async function signup(
  page,
  email: string,
  password: string,
  expectSuccess: boolean = true,
  confirmPassword?: string
) {
  const signUpPage = new SignUpPage(page);
  await signUpPage.navigateToSignUp();
  await signUpPage.fillForm(email, password, confirmPassword ?? password);
  await signUpPage.submitForm();
  if (expectSuccess) {
    await expect(page.getByTestId("signup-back-to-signup-link")).toBeVisible({
      timeout: 300000,
    });
  }
}

async function verifyEmail(page, email: string) {
  const verifyLink = await getVerificationLink(email);
  await page.goto(verifyLink);
  await expect(page.getByTestId("signin-email-input")).toBeVisible();
}

async function login(page, email: string, password: string) {
  await page.fill('[data-testid="signin-email-input"]', email);
  await page.fill('[data-testid="signin-password-input"]', password);
  await page.click('[data-testid="signin-submit-btn"]');
  await expect(page.getByTestId("Header-place-order-btn")).toBeVisible();
}

test("TC-SU-01 - Full signup + email verification + login flow", async ({
  page,
}) => {
  const email = `nahmad0313@gmail.com`;
  const password = "123456789";

  await signup(page, email, password);
  await verifyEmail(page, email);
  await login(page, email, password);
});

test("TC02 - Signup with Already Registered Email", async ({ page }) => {
  const email = `dtdeveloperwork@gmail.com`; // Use the same email for signup again
  const password = "12345678";

  // Signup with the email
  await signup(page, email, password, false);

  // Wait for the toast to appear and assert its text
  const toast = page.locator(
    "text=This email is already registered. Please Sign-in with your Google Account."
  );
  await expect(toast).toBeVisible();
});

// TC03 - Signup with invalid email format
test("TC03 - Signup with invalid email format", async ({ page }) => {
  const signUpPage = new SignUpPage(page);
  const email = "invalid-email";
  const password = "123456789";

  await signUpPage.navigateToSignUp();

  // Capture the URL before submitting
  const urlBefore = page.url();

  await signUpPage.fillForm(email, password, password);
  await signUpPage.submitForm();

  // Capture the URL before submitting
  const urlAfter = page.url();

  // Assert that the URL has not changed
  expect(urlAfter).toBe(urlBefore);
});

// TC04 - Signup with password less than 8 characters
test("TC04 - Signup with password less than 8 characters", async ({ page }) => {
  const email = `weakpass${Date.now()}@gmail.com`;
  const password = "1234567";
  await signup(page, email, password, false);

  // Wait for the toast to appear and assert its text
  const toast = page.locator(
    "text=Password should be at least 8 characters long"
  );
  await expect(toast).toBeVisible();
});

// TC05 - Signup with mismatched passwords
test("TC05 - Signup with mismatched passwords", async ({ page }) => {
  const email = `mismatch${Date.now()}@gmail.com`;
  const password = "123456789";
  const confirmPassword = "987654321";

  await signup(page, email, password, false, confirmPassword);

  // Wait for the toast to appear and assert its text
  const toast = page.locator("text=Password and confirm password do not match");
  await expect(toast).toBeVisible();
});

// TC06 - Signup with empty fields
test("TC06 - Signup with empty fields", async ({ page }) => {
  const signUpPage = new SignUpPage(page);
  await signUpPage.navigateToSignUp();
  await signUpPage.submitForm();

  // Wait for the toast to appear and assert its text
  const toast = page.locator("text=Please enter your email");
  await expect(toast).toBeVisible({
    timeout: 3000,
  });
});
