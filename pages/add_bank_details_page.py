from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.decorators import log_method, log_page_state
import logging

logger = logging.getLogger(__name__)


class AddBankDetailsPage(BasePage):
    """Page Object for the Login Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.add_bank_details_url
        logger.info(f"🏗️ Initialized LoginPage - URL: {self.url}")
