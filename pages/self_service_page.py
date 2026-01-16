"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page, expect

from pages.add_bank_details_page import AddBankDetailsPage
from pages.edit_self_service_page import EditSelfServicePage
from pages.home_page import HomePage
from pages.base_page import BasePage
from config import settings
from utils.constants import SELF_SERVICE_PAGE
import logging

from utils.decorators import log_method, log_page_state

logger = logging.getLogger(__name__)

class SelfServicePage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.self_service_url

    @log_method
    def verify_self_service_page_loads(self) -> None:
        """Verify the self-service page has loaded correctly."""
        logger.info(f"✅ Verify Logged in user")
        self.verify_element_visible(SELF_SERVICE_PAGE.PERSONAL_NAME)

    @log_method
    def click_to_logout(self) -> HomePage:
        """Click on the logout button"""
        logger.info("🖱️ Click to logout")
        self.click_element(SELF_SERVICE_PAGE.MM_PROFILE)
        self.click_element(SELF_SERVICE_PAGE.LOGOUT_LINK)
        return HomePage(self.page)

    @log_method
    def click_to_edit_personal_data_details(self) -> EditSelfServicePage:
        """ Edit Personal data"""
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

    @log_method
    def click_to_add_banking_details(self) -> AddBankDetailsPage:
        """ Add Bank Details """
        try:
            logger.info("🖱️ Click a button to add Bank Details")
            # Wait for the page to be fully loaded
            self.page.wait_for_load_state("domcontentloaded")
            self.click_element(SELF_SERVICE_PAGE.ADD_BANK_DETAIL_MODULE)
            logger.info("✅ Click Bank Details link")

            self.click_element(SELF_SERVICE_PAGE.ADD_NEW_BANK_DETAIL_BUTTON)

            logger.info("✅ Click Add Bank Details link")
            logger.info("✅ Navigate to Add Bank Details Page")
            return AddBankDetailsPage(self.page)

        except Exception as e:
            logger.error(f"❌ Failed to add bank detail : {e}")
            # Debug info
            self._debug_add_bank_module()
            self._debug_add_bank_details()
            self.screenshot("error_add_bank_detail_link.png", full_page=True)
            raise

    def _debug_add_bank_module(self):
        """Debug helper for add bank detail"""
        try:
            selector = SELF_SERVICE_PAGE.ADD_BANK_DETAIL_MODULE
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

    def _debug_add_bank_details(self):
        """Debug helper for add bank detail"""
        try:
            selector = SELF_SERVICE_PAGE.ADD_NEW_BANK_DETAIL_BUTTON
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
