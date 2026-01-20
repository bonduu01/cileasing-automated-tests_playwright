"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import EDIT_BANK_DETAILS_PAGE
import logging

from utils.decorators import log_method

logger = logging.getLogger(__name__)


class EditBankDetailsPage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @log_method
    def edit_bank_details(self, bank_name: str | None = None, bank_id: str | None = None, sort_code: str | None =
    None) -> None:
        """ Add a default bank account number """
        bank_name = bank_name or settings.bank_name
        bank_id = bank_id or settings.bank_id
        sort_code = sort_code or settings.sort_code

        # Clear textboxes
        self.clear_input(EDIT_BANK_DETAILS_PAGE.BANK_ID)
        self.clear_input(EDIT_BANK_DETAILS_PAGE.SORT_CODE)
        logger.info("✅ TextBoxes value cleared")

        logger.info(f"🔐 Attempting to edit bank details to: {bank_name}, {bank_id} and {sort_code}")
        self.ant_select_option(
            EDIT_BANK_DETAILS_PAGE.BANK_NAME_DROPDOWN,
            EDIT_BANK_DETAILS_PAGE.BANK_NAME
        )
        logger.info("✅ Edit Bank details page and click Submit")
        self.fill_input(EDIT_BANK_DETAILS_PAGE.BANK_ID, bank_id)
        self.verify_input_value_length(EDIT_BANK_DETAILS_PAGE.BANK_ID, 10)
        self.fill_input(EDIT_BANK_DETAILS_PAGE.SORT_CODE, sort_code)
        self.click_element(EDIT_BANK_DETAILS_PAGE.EDIT_SUBMIT_BUTTON)
