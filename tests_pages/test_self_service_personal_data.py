import pytest
from pages import EditSelfServicePage, SelfServicePage
from playwright.sync_api import Page
from config import settings
import logging

logger = logging.getLogger(__name__)


class TestEditSelfServicePage:
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
    def test_edit_personal_details(self) -> None:
        """Test editing personal details with debugging"""
        logger.info("📋 Test go to Edit Personal Details")
        # Debug: Check current page
        logger.info(f"📍 Current URL: {self.page.url}")
        logger.info(f"📍 Page Title: {self.page.title()}")

        # Wait for page to be ready
        self.page.wait_for_load_state("domcontentloaded")

        # Take screenshot before clicking
        self.page.screenshot(path="before_click_edit.png", full_page=True)

        # Debug: Check if edit link is visible
        from utils.constants import SELF_SERVICE_PAGE
        edit_link = self.page.locator(SELF_SERVICE_PAGE.EDIT_LINK)

        logger.info(f"🔍 Edit link visible: {edit_link.is_visible()}")
        logger.info(f"🔍 Edit link count: {edit_link.count()}")

        if edit_link.count() > 0:
            logger.info(f"🔍 Edit link text: {edit_link.text_content()}")

        # Click to edit
        self.edit_self_service_page = self.self_service_page.click_to_edit_personal_data_details()

        # Debug: Check navigation happened
        logger.info(f"📍 After click URL: {self.page.url}")

        # Take screenshot after clicking
        self.page.screenshot(path="after_click_edit.png", full_page=True)

        # Fill Form
        self.edit_self_service_page.edit_and_submit_personal_data_details(
            other_name=settings.test_other_name,
            job_title=settings.test_job_title
        )

