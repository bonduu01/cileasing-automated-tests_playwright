from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import ADD_BANK_DETAILS_PAGE
from utils.decorators import log_method, log_page_state
import logging

logger = logging.getLogger(__name__)


class AddBankDetailsPage(BasePage):
    """Page Object for the Login Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.add_bank_details_url
        logger.info(f"🏗️ Initialized LoginPage - URL: {self.url}")

    @log_method
    def create_new_bank_details(self, bank_name: str | None = None, bank_id: str | None = None, sort_code: str | None =
    None) -> None:
        """ Add a default bank account number """
        bank_name = bank_name or settings.bank_name
        bank_id = bank_id or settings.bank_id
        sort_code = sort_code or settings.sort_code

        logger.info(f"🔐 Attempting to create bank details using: {bank_name}, {bank_id} and {sort_code}")

        self.ant_select_option(
            ADD_BANK_DETAILS_PAGE.BANK_NAME_DROPDOWN,
            ADD_BANK_DETAILS_PAGE.BANK_NAME
        )
        logger.info(f"✅ Selected {ADD_BANK_DETAILS_PAGE.BANK_NAME} from dropdown")
        self.fill_input(ADD_BANK_DETAILS_PAGE.BANK_ID, bank_id)
        self.verify_input_value_length(ADD_BANK_DETAILS_PAGE.BANK_ID, 10)
        self.verify_element_has_value(ADD_BANK_DETAILS_PAGE.BANK_ID, bank_id)
        logger.info(f"✅ Financial ID: {bank_id} added and verified")
        self.fill_input(ADD_BANK_DETAILS_PAGE.SORT_CODE, sort_code)
        self.verify_element_has_value(ADD_BANK_DETAILS_PAGE.SORT_CODE, sort_code)
        logger.info(f"✅ Sort Code: {sort_code} added and verified")
        self.click_element(ADD_BANK_DETAILS_PAGE.ADD_BANK_BUTTON)
        logger.info(f"✅ Bank Created Successfully")
