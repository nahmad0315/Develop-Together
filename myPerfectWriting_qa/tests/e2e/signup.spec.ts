import { test, expect } from "@playwright/test";
import { SignUpPage } from "../../pages/SignUpPage";

test("User can sign up successfully with valid credentials", async ({
  page,
}) => {
  const signUp = new SignUpPage(page);

  await signUp.navigateToSignUp();

  const email = `nahmad0313@gmail.com`;
  const password = "1234567890";

  await signUp.fillForm(email, password, password);
  await signUp.submitForm();
  await signUp.expectSuccessMessage();
});
