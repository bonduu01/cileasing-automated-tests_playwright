import pytest
from playwright.sync_api import Page
from config import settings
import logging

from pages import SelfServicePage

logger = logging.getLogger(__name__)


class TestAddBankDetailsPage:
    """Test suite for Self-Service functionalities."""

    @pytest.fixture(autouse=True)
    def setup_test_logging(self, request):
        """Log test setup and teardown."""
        test_name = request.node.name
        logger.info(f"\n{'#' * 80}")
        logger.info(f"🧪 STARTING TEST: {test_name}")
        logger.info(f"{'#' * 80}\n")

        yield

        logger.info(f"\n{'#' * 80}")
        logger.info(f"🏁 FINISHED TEST: {test_name}")
        logger.info(f"{'#' * 80}\n")

    @pytest.fixture(autouse=True)
    def setup(self, authenticated_page: Page):
        """Setup before each test - store page in self"""
        logger.info("📋 Authenticate User module")
        self.page = authenticated_page
        self.self_service_page = SelfServicePage(self.page)

        yield
        # Cleanup if needed

    @pytest.mark.regression
    def test_to_add_new_bank_details(self) -> None:
        """Test Add New Bank details with debugging"""
        logger.info("📋 Test go add bank Details")
        # Debug: Check current page
        logger.info(f"📍 Current URL: {self.page.url}")
        logger.info(f"📍 Page Title: {self.page.title()}")

        # Wait for page to be ready
        self.page.wait_for_load_state("domcontentloaded")

        # # Take screenshot before clicking
        # self.page.screenshot(path="before_click_edit.png", full_page=True)

        # Debug: Check if Add Bank Button is visible
        from utils.constants import SELF_SERVICE_PAGE
        add_bank_detail_module_link = self.page.locator(SELF_SERVICE_PAGE.CLICK_BANK_DETAIL)

        logger.info(f"🔍 Add Bank Button visible: {add_bank_detail_module_link.is_visible()}")
        logger.info(f"🔍 Add Bank Button count: {add_bank_detail_module_link.count()}")

        if add_bank_detail_module_link.count() > 0:
            logger.info(f"🔍 Add Bank Button text: {add_bank_detail_module_link.text_content()}")

        # Click to add
        add_bank_details_page = self.self_service_page.click_to_add_banking_details()

        # Debug: Check navigation happened
        logger.info(f"📍 After click URL: {self.page.url}")
        add_bank_details_page.create_new_bank_details()
        logger.info("✅ Add bank details created successful")

    @pytest.mark.regression
    def test_to_edit_bank_details(self) -> None:
        """Test editing personal details with debugging"""
        logger.info("📋 Test go add bank Details")
        # Debug: Check current page
        logger.info(f"📍 Current URL: {self.page.url}")
        logger.info(f"📍 Page Title: {self.page.title()}")

        # Wait for page to be ready
        self.page.wait_for_load_state("domcontentloaded")

        # # Take screenshot before clicking
        # self.page.screenshot(path="before_click_edit.png", full_page=True)

        # Debug: Check if Add Bank Button is visible
        from utils.constants import SELF_SERVICE_PAGE
        bank_detail_link = self.page.locator(SELF_SERVICE_PAGE.CLICK_BANK_DETAIL)

        logger.info(f"🔍 Add Bank Button visible: {bank_detail_link.is_visible()}")
        logger.info(f"🔍 Add Bank Button count: {bank_detail_link.count()}")

        if bank_detail_link.count() > 0:
            logger.info(f"🔍 Add Bank Button text: {bank_detail_link.text_content()}")

        # Click to edit
        edit_bank_details_page = self.self_service_page.click_to_edit_bank_details()
        edit_bank_details_page.edit_bank_details()
