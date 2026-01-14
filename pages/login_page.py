"""
Login Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

from pages.self_service_page import SelfServicePage
from pages.base_page import BasePage
from config import settings
from utils.constants import LOGIN_PAGE


class LoginPage(BasePage):
    """Page Object for the Login Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.base_url

    def go_to_login_page(self) -> None:
        """Navigate to the login page."""
        self.navigate_to(self.url)

    def login_user(self, email: str | None = None, password: str | None = None) -> None:
        """
        Perform login with provided or default credentials.

        Args:
            email: User email (defaults to TEST_USERNAME from .env)
            password: User password (defaults to TEST_PASSWORD from .env)
        """
        email = email or settings.test_username
        password = password or settings.test_password

        self.fill_input(LOGIN_PAGE.EMAIL_INPUT, email)
        self.fill_input(LOGIN_PAGE.PASSWORD_INPUT, password)
        self.click_element(LOGIN_PAGE.SUBMIT_BUTTON)
        self.wait(5000)

    def enter_email(self, email: str) -> None:
        """Enter email address."""
        self.fill_input(LOGIN_PAGE.EMAIL_INPUT, email)

    def enter_password(self, password: str) -> None:
        """Enter password."""
        self.fill_input(LOGIN_PAGE.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """Click the login button."""
        self.click_element(LOGIN_PAGE.SUBMIT_BUTTON)

    def verify_login_successful_load_companies(self) -> None:
        """Assert that the login successful message is displayed"""
        self.verify_element_visible(LOGIN_PAGE.DEFAULT_COMPANY)
        self.verify_element_visible(LOGIN_PAGE.FLOUR_MILLS_COMPANY)

    def verify_error_message(self) -> None:
        """Assert an error message is displayed."""
        self.verify_has_text_visible(LOGIN_PAGE.ERROR_TOAST, LOGIN_PAGE.ERROR_INVALID_CREDENTIALS)

    def verify_error_toast_visible(self):
        """Verify error toast alert is visible."""
        self.verify_element_visible(LOGIN_PAGE.ERROR_TOAST, timeout=1000)

    def verify_password_blank_error(self):
        """Verify 'Password cannot be blank' validation error."""
        self.verify_validation_error(LOGIN_PAGE.ERROR_PASSWORD_BLANK)

    def verify_username_blank_error(self):
        """Verify 'Username cannot be blank' validation error."""
        self.verify_validation_error(LOGIN_PAGE.ERROR_USERNAME_BLANK)
        self.verify_validation_error(LOGIN_PAGE.ERROR_PASSWORD_BLANK)

    def is_password_blank_error_visible(self):
        """Check if password blank error is visible."""
        return self.is_validation_error_visible(LOGIN_PAGE.ERROR_PASSWORD_BLANK)

    def is_username_blank_error_visible(self):
        """Check if password blank error is visible."""
        return self.is_validation_error_visible(LOGIN_PAGE.ERROR_USERNAME_BLANK)

    def click_default_company_link(self) -> SelfServicePage:
        """Click the default company link."""
        self.click_element(LOGIN_PAGE.DEFAULT_LINK)
        return SelfServicePage(self.page)

    # def get_validation_error_message(self):
    #     """Get validation error message text."""
    #     return self.get_validation_error_text(LOGIN_PAGE.VALIDATION_ERROR)
    #
    # def wait_for_password_blank_error(self, timeout: float = 5000):
    #     """Wait for password blank error to appear."""
    #     return self.wait_for_validation_error(LOGIN_PAGE.ERROR_PASSWORD_BLANK, timeout)
    #
    # def verify_validation_error_by_text(self, error_text: str):
    #     """Verify validation error with specific text."""
    #     self.verify_field_error_by_text(error_text)