"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import HOME_PAGE, LOGIN_PAGE
import logging

from utils.decorators import log_method, log_page_state

logger = logging.getLogger(__name__)

class HomePage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.base_url
        logger.info(f"🏗️ Initialized HomePage - URL: {self.url}")

    @log_method
    @log_page_state
    def go_to_home_page(self) -> None:
        """Navigate to the home page."""
        logger.info(f"🔄 Navigating to home page: {self.url}")
        self.navigate_to(self.url)

    @log_method
    def verify_home_page_loads(self) -> None:
        """Verify the home page has loaded correctly."""
        logger.info("✅ Verifying HomePage loads")
        self.verify_title(HOME_PAGE.TITLE)
        self.verify_element_is_disabled(LOGIN_PAGE.PASSWORD_DISABLED)
