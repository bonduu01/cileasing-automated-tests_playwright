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
    def test_to_add_bank_details(self) -> None:
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
        add_bank_detail_button = self.page.locator(SELF_SERVICE_PAGE.ADD_BANK_DETAIL_BUTTON)

        logger.info(f"🔍 Add Bank Button visible: {add_bank_detail_button.is_visible()}")
        logger.info(f"🔍 Add Bank Button count: {add_bank_detail_button.count()}")

        if add_bank_detail_button.count() > 0:
            logger.info(f"🔍 Add Bank Button text: {add_bank_detail_button.text_content()}")

        # Click to add
        self.add_bank_details_page = self.self_service_page.click_to_add_banking_details()

        # Debug: Check navigation happened
        logger.info(f"📍 After click URL: {self.page.url}")

        # # Take screenshot after clicking
        # self.page.screenshot(path="after_click_edit.png", full_page=True)

        # Create bank details

        # self.edit_self_service_page.edit_and_submit_personal_data_details(
        #     other_name=settings.test_other_name,
        #     job_title=settings.test_job_title
        # )
