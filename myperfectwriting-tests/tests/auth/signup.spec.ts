// import { test, expect } from "@playwright/test";
// import { SignUpPage } from "../../pages/SignUpPage";

// test.describe("Sign Up Flow – My Perfect Writing Portal", () => {
//   test("TC01 - Successful signup with valid credentials", async ({ page }) => {
//     const signUpPage = new SignUpPage(page);
//     await signUpPage.navigateToSignUp();

//     // Use timestamp to avoid duplicate email conflicts
//     const uniqueEmail = `SQAauto+${Date.now()}@mail.com`;
//     const password = "StrongPass123!";

//     await signUpPage.fillForm(uniqueEmail, password, password);
//     await signUpPage.submitForm();

//     // Adjust the expectation based on actual behavior after sign up
//     // await expect(page).toHaveURL(/verify|check-email|signin/);
//     // or if it shows a message instead of redirect:
//     await expect(page.getByTestId("signup-back-to-signup-link")).toBeVisible({
//       timeout: 20000,
//     });
//   });
// });

import { test, expect } from "@playwright/test";
import { SignUpPage } from "../../pages/SignUpPage";
import { getVerificationLink } from "../../utils/gmailHelper";

test("TC01 - Full signup + email verification + login flow", async ({
  page,
}) => {
  const signUpPage = new SignUpPage(page);

  const timestamp = Date.now();
  const email = `nahmad0313@gmail.com`; // Use your Gmail that gets test emails
  const password = "StrongPass123!";

  // Step 1: Go to signup and register
  await signUpPage.navigateToSignUp();
  await signUpPage.fillForm(email, password, password);
  await signUpPage.submitForm();

  await expect(page.getByTestId("signup-back-to-signup-link")).toBeVisible({
    timeout: 30000,
  });

  // Step 2: Get email verification link from Gmail
  const verifyLink = await getVerificationLink(email);

  // Step 3: Visit verification link → should land on Sign In page
  await page.goto(verifyLink);
  await expect(page.getByTestId("signin-email-input")).toBeVisible();

  // Step 4: Log in with same credentials
  await page.fill('[data-testid="signin-email-input"]', email);
  await page.fill('[data-testid="signin-password-input"]', password);
  await page.click('[data-testid="signin-submit-btn"]');

  // Step 5: Confirm dashboard appears
  await expect(page.getByRole("link", { name: "Place Order" })).toBeVisible();
});
