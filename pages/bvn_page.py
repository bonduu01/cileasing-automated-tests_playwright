from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import ADD_BANK_DETAILS_PAGE, ADD_BVN_PAGE
from utils.decorators import log_method
import logging

logger = logging.getLogger(__name__)


class AddBnvPage(BasePage):
    """Page Object for the Login Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.add_bank_details_url
        logger.info(f"🏗️ Initialized LoginPage - URL: {self.url}")

    @log_method
    def create_bvn(self, test_bvn_number: str | None = None) -> None:
        """ Add bvn number """
        test_bvn_number = test_bvn_number or settings.test_bvn_number

        logger.info(f"🔐 Attempting to create bank details using: {test_bvn_number}")

        self.fill_input(ADD_BVN_PAGE.BVN_INPUT, test_bvn_number)
        self.verify_input_value_length(ADD_BVN_PAGE.BVN_INPUT, 11)
        self.verify_element_has_value(ADD_BVN_PAGE.BVN_INPUT, test_bvn_number)
        logger.info(f"✅ Bank VPN: {test_bvn_number} added and verified")
        self.click_element(ADD_BVN_PAGE.ADD_BVN_BUTTON)
        logger.info(f"✅ Bank Created Successfully")
