"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.base_page import BasePage
from config import settings
from utils.constants import EDIT_SELF_SERVICE_PAGE
import logging

logger = logging.getLogger(__name__)

class EditSelfServicePage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.url = settings.edit_self_service_url
        logger.info(f"📍 Edit Service URL: {self.url}")

    def edit_and_submit_personal_data_details(self, other_name: str | None = None,
                                              job_title: str | None = None) -> None:
        """Authenticate user to edit self-service."""
        other_name = other_name or settings.other_name
        job_title = job_title or settings.job_title
        # # Clear textboxes
        # self.clear_input(EDIT_SELF_SERVICE_PAGE.OTHER_NAME)
        # self.clear_input(EDIT_SELF_SERVICE_PAGE.JOB_TITLE)
        logger.info(f"📍 Current URL: {self.page.url}")
        logger.info(f"📍 Page Title: {self.page.title()}")
        logger.info(f"Other Name: {other_name}")
        logger.info(f"Other Name: {job_title}")

        self.fill_input(EDIT_SELF_SERVICE_PAGE.OTHER_NAME, other_name)
        self.fill_input(EDIT_SELF_SERVICE_PAGE.JOB_TITLE, job_title)

        self.click_element(EDIT_SELF_SERVICE_PAGE.EDIT_SUBMIT_BUTTON)
