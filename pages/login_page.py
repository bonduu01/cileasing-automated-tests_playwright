"""
Login Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

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

    # def verify_login_form_visible(self) -> None:
    #     """Verify login form elements are visible."""
    #     self.verify_element_visible(LOGIN_PAGE.EMAIL_INPUT)
    #     self.verify_element_visible(LOGIN_PAGE.PASSWORD_INPUT)
    #     self.verify_element_visible(LOGIN_PAGE.SUBMIT_BUTTON)

    def verify_error_message(self, message: str) -> None:
        """Assert an error message is displayed."""
        self.verify_text_visible(message)

    def verify_login_successful_load_companies(self) -> None:
        """Assert that the login successful message is displayed"""
        self.verify_element_visible(LOGIN_PAGE.DEFAULT_COMPANY)
        self.verify_element_visible(LOGIN_PAGE.FLOUR_MILLS_COMPANY)