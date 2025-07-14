import { Page, Locator, expect } from "@playwright/test";

export class SignInPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly SignInButton: Locator;
  readonly headerPOButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByTestId("signin-email-input");
    this.passwordInput = page.getByTestId("signin-password-input");
    this.SignInButton = page.getByTestId("signin-submit-btn");
    this.headerPOButton = page.getByTestId("Header-place-order-btn");
  }

  async goto() {
    await this.page.goto("/sign-in");
  }

  async fillEmail(email: string) {
    await this.emailInput.fill(email);
  }

  async fillPassword(password: string) {
    await this.passwordInput.fill(password);
  }

  async clickSignIn() {
    await this.SignInButton.click();
  }

  async login(email: string, password: string) {
    await this.goto();
    await this.fillEmail(email);
    await this.fillPassword(password);
    await this.clickSignIn();
  }

  async assertDashboardVisible() {
    await expect(this.headerPOButton).toBeVisible();
  }
}
