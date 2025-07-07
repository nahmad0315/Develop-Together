import { Page, Locator } from "@playwright/test";
export class SignUpPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly confirmPasswordInput: Locator;
  readonly signUpButton: Locator;
  readonly googleSignUpButton: Locator;
  readonly signUpErrorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByTestId("signup-email-input");
    this.passwordInput = page.getByTestId("signup-password-input");
    this.confirmPasswordInput = page.getByTestId(
      "signup-confirm-password-input"
    );
    this.signUpButton = page.getByTestId("signup-submit-btn");
    this.googleSignUpButton = page.getByTestId("signup-google-button");
    this.signUpErrorMessage = page.getByTestId("signup-error-message");
  }
  async navigateToSignUp() {
    await this.page.goto("/sign-up");
  }

  async fillForm(email: string, password: string, confirmPassword: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.confirmPasswordInput.fill(confirmPassword);
  }

  async submitForm() {
    await this.signUpButton.click();
  }
}
