// test.setTimeout(120_000); // 2 minutes

// import { test, expect } from "@playwright/test";
// import { SignUpPage } from "../../pages/SignUpPage";
// import { getVerificationLink } from "../../utils/gmailHelper";

// test("TC01 - Full signup + email verification + login flow", async ({
//   page,
// }) => {
//   const signUpPage = new SignUpPage(page);

//   // Generate dynamic Gmail alias
//   // const timestamp = Date.now();
//   // const email = `nahmad0313+${timestamp}@gmail.com`; // Gmail alias for unique email
//   const email = `nahmad0313@gmail.com`;
//   const password = "123456789";

//   // Step 1: Go to signup and register
//   await signUpPage.navigateToSignUp();
//   await signUpPage.fillForm(email, password, password);
//   await signUpPage.submitForm();

//   // Wait for signup confirmation message or redirect
//   await expect(page.getByTestId("signup-back-to-signup-link")).toBeVisible({
//     timeout: 300000, // 5 minutes
//   });

//   // Step 2: Get email verification link from Gmail
//   const verifyLink = await getVerificationLink(email);

//   // Step 3: Visit verification link → should land on Sign In page
//   await page.goto(verifyLink);
//   await expect(page.getByTestId("signin-email-input")).toBeVisible();

//   // Step 4: Log in with the same credentials
//   await page.fill('[data-testid="signin-email-input"]', email);
//   await page.fill('[data-testid="signin-password-input"]', password);
//   await page.click('[data-testid="signin-submit-btn"]');

//   // Step 5: Confirm dashboard appears
//   await expect(page.getByTestId("Header-place-order-btn")).toBeVisible();
// });

import { test, expect } from "@playwright/test";
import { SignUpPage } from "../../pages/SignUpPage";
import { getVerificationLink } from "../../utils/gmailHelper";

test.setTimeout(120_000); // 2 minutes

async function signup(page, email: string, password: string) {
  const signUpPage = new SignUpPage(page);
  await signUpPage.navigateToSignUp();
  await signUpPage.fillForm(email, password, password);
  await signUpPage.submitForm();
  await expect(page.getByTestId("signup-back-to-signup-link")).toBeVisible({
    timeout: 300000,
  });
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

test("TC01 - Full signup + email verification + login flow", async ({
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
  await signup(page, email, password);

  // Wait for the toast to appear and assert its text
  const toast = page.locator(
    "text=This email is already registered. Please Sign-in with your Google Account."
  );
  await expect(toast).toBeVisible();
});
