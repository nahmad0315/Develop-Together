import { test, expect } from "@playwright/test";
import { SignUpPage } from "../../pages/SignUpPage";

test.describe("Sign Up Flow – My Perfect Writing Portal", () => {
  test("TC01 - Successful signup with valid credentials", async ({ page }) => {
    const signUpPage = new SignUpPage(page);
    await signUpPage.navigateToSignUp();

    // Use timestamp to avoid duplicate email conflicts
    const uniqueEmail = `SQAauto+${Date.now()}@mail.com`;
    const password = "StrongPass123!";

    await signUpPage.fillForm(uniqueEmail, password, password);
    await signUpPage.submitForm();

    // Adjust the expectation based on actual behavior after sign up
    await expect(page).toHaveURL(/verify|check-email|signin/);
    // or if it shows a message instead of redirect:
    // await expect(page.getByText('Please check your email')).toBeVisible();
  });
});
