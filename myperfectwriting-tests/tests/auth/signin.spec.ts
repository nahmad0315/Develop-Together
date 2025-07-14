export async function signin(page, email: string, password: string) {
  await page.goto("/sign-in");
  await page.getByTestId("signin-email-input").fill(email);
  await page.getByTestId("signin-password-input").fill(password);
  await page.getByTestId("signin-submit-btn").click();
}

import { test, expect } from "@playwright/test";

const validEmail = "nahmad0313@gmail.com";
const validPassword = "123456789";

test("TC-SI-01 - Sign in with valid credentials", async ({ page }) => {
  await signin(page, validEmail, validPassword);
  await expect(page.getByTestId("Header-place-order-btn")).toBeVisible();
});

test("TC-SI-02 - Sign in with incorrect password", async ({ page }) => {
  await signin(page, validEmail, "wrongpassword");
  const toast = page.locator("text=Invalid Password");
  await expect(toast).toBeVisible();
});

test("TC-SI-03 - Sign in with unregistered email", async ({ page }) => {
  await signin(page, "notregistered@example.com", validPassword);
  const toast = page.locator(
    "text=Invalid email or email does not exist. Please sign up!"
  );
  await expect(toast).toBeVisible();
});

test("TC-SI-04 - Sign in with empty email and password fields", async ({
  page,
}) => {
  await page.goto("/sign-in");
  await page.getByTestId("signin-submit-btn").click();
  const toast = page.locator("text=Please enter your email");
  await expect(toast).toBeVisible();
});
