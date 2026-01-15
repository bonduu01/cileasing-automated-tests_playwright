"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page, expect

from pages.edit_self_service_page import EditSelfServicePage
from pages.home_page import HomePage
from pages.base_page import BasePage
from config import settings
from utils.constants import SELF_SERVICE_PAGE
import logging

logger = logging.getLogger(__name__)

class SelfServicePage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.self_service_url

    def verify_self_service_page_loads(self) -> None:
        """Verify the self-service page has loaded correctly."""
        self.verify_element_visible(SELF_SERVICE_PAGE.PERSONAL_NAME)

    def click_to_logout(self) -> HomePage:
        """Click on the logout button"""
        self.click_element(SELF_SERVICE_PAGE.MM_PROFILE)
        self.click_element(SELF_SERVICE_PAGE.LOGOUT_LINK)
        return HomePage(self.page)

    # def click_to_edit_personal_data_details(self) -> EditSelfServicePage:
    #     self.click_element(SELF_SERVICE_PAGE.EDIT_LINK)
    #     return EditSelfServicePage(self.page)

    def click_to_edit_personal_data_details(self) -> EditSelfServicePage:
        """
        Click edit link and navigate to edit page.

        Returns:
            EditSelfServicePage instance
        """
        try:
            logger.info("🖱️ Clicking edit personal data link")

            # Wait for the page to be fully loaded
            self.page.wait_for_load_state("domcontentloaded")

            # Get the edit link locator
            edit_link = self.page.locator(SELF_SERVICE_PAGE.EDIT_LINK)

            # Wait for element to be visible
            edit_link.wait_for(state="visible", timeout=30000)

            # Scroll into view
            edit_link.scroll_into_view_if_needed()

            # Ensure it's enabled
            expect(edit_link).to_be_enabled(timeout=10000)

            # Click the element
            edit_link.click()

            logger.info("✅ Edit link clicked successfully")

            # Wait for navigation to complete
            self.page.wait_for_load_state("domcontentloaded")

            # Optional: Wait for edit form to be visible
            # self.page.wait_for_selector(
            #     "input[name='otherName'], input[name='jobTitle']",
            #     state="visible",
            #     timeout=10000
            # )

            return EditSelfServicePage(self.page)

        except Exception as e:
            logger.error(f"❌ Failed to click edit link: {e}")
            # Debug info
            self._debug_edit_link()
            self.screenshot("error_click_edit_link.png", full_page=True)
            raise

    def _debug_edit_link(self):
        """Debug helper for edit link"""
        try:
            selector = SELF_SERVICE_PAGE.EDIT_LINK
            locator = self.page.locator(selector)

            logger.info(f"\n🔍 Debug info for: {selector}")
            logger.info(f"   Count: {locator.count()}")

            if locator.count() > 0:
                logger.info(f"   Visible: {locator.is_visible()}")
                logger.info(f"   Enabled: {locator.is_enabled()}")
                logger.info(f"   Text: {locator.text_content()}")
            else:
                logger.info("   ❌ Element not found!")
                # List all links on page
                all_links = self.page.locator("a").all()
                logger.info(f"\n   All links on page ({len(all_links)}):")
                for i, link in enumerate(all_links[:10]):
                    text = link.text_content() or ""
                    href = link.get_attribute("href") or ""
                    logger.info(f"      {i + 1}. Text: '{text.strip()}' | href: '{href}'")

        except Exception as e:
            logger.warning(f"   Debug failed: {e}")
