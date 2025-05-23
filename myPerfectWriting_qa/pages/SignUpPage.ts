import { Page } from "@playwright/test";

export class SignUpPage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  async navigateToSignUp() {
    await this.page.goto("https://portal.nerdessay.com/register"); // Update this if you have a full URL or route
  }

  async fillForm(email: string, password: string, confirmPassword: string) {
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.fill(
      'input[name="password_confirmation"]',
      confirmPassword
    );
  }

  // async submitForm() {
  //   await this.page.click('button[type="submit"]');
  // }

  async expectSuccessMessage() {
    await this.page.waitForSelector("button#submit");
  }
}
