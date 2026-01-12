"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import HOME_PAGE, LOGIN_PAGE


class HomePage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.base_url

    def go_to_home_page(self) -> None:
        """Navigate to the home page."""
        self.navigate_to(self.url)

    def verify_home_page_loads(self) -> None:
        """Verify the home page has loaded correctly."""
        self.verify_title(HOME_PAGE.TITLE)
        self.verify_element_is_disabled(LOGIN_PAGE.PASSWORD_DISABLED)
