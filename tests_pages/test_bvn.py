import pytest
from playwright.sync_api import Page
from config import settings
import logging

from pages import SelfServicePage

logger = logging.getLogger(__name__)


class TestBvnPage:
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

    # @pytest.mark.regression
    # def test_to_add_bvn(self) -> None:
    #     """Test Add New Bank details with debugging"""
    #     logger.info("📋 Test go add bvn")
    #     # Debug: Check current page
    #     logger.info(f"📍 Current URL: {self.page.url}")
    #     logger.info(f"📍 Page Title: {self.page.title()}")
    #
    #     # Wait for page to be ready
    #     self.page.wait_for_load_state("domcontentloaded")
    #
    #     # Debug: Check if Add BVN Button is visible
    #     from utils.constants import SELF_SERVICE_PAGE
    #     click_bvn_button = self.page.locator(SELF_SERVICE_PAGE.BVN_BUTTON)
    #
    #     logger.info(f"🔍 BVN link is visible: {click_bvn_button.is_visible()}")
    #
    #     if click_bvn_button.count() > 0:
    #         logger.info(f"🔍 Add Bank Button text: {click_bvn_button.text_content()}")
    #
    #     # Click to add
    #     add_bvn_page = self.self_service_page.click_to_add_bvn_number()
    #
    #     logger.info(f"📍 After click URL: {self.page.url}")
    #     add_bvn_page.create_bvn()
    #     logger.info("✅ BVN created successfully")

    @pytest.mark.regression
    def test_to_edit_bvn(self) -> None:
        """Test editing personal details with debugging"""
        logger.info("📋 Test edit bvn")
        # Debug: Check current page
        logger.info(f"📍 Current URL: {self.page.url}")
        logger.info(f"📍 Page Title: {self.page.title()}")

        # Wait for page to be ready
        self.page.wait_for_load_state("domcontentloaded")

        # Click to add
        edit_bvn_page = self.self_service_page.click_to_edit_bvn_number()

        logger.info(f"📍 After click URL: {self.page.url}")
        edit_bvn_page.edit_bvn()
        logger.info("✅ BVN edited successfully")
