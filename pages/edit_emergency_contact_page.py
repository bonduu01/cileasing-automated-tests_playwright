"""
Home Page Object for the CAndILeasing application.
"""

from playwright.sync_api import Page

from pages.base_page import BasePage
from config import settings
from utils.constants import EDIT_EMERGENCY_CONTACT_PAGE
import logging

from utils.decorators import log_method

logger = logging.getLogger(__name__)


class EditEmergencyContactPage(BasePage):
    """Page Object for the Home Page."""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @log_method
    def edit_emergency_contacts_details(self, first_name: str | None = None, other_name: str | None = None,
                              surname: str | None = None, maiden_name: str | None = None,
                              previous_name: str | None = None, mobile_number: str | None = None,
                              work_number: str | None = None, relationship: str | None = None,
                              email: str | None = None, location: str | None = None) -> None:
        """ Add emergency contact details page """
        first_name = first_name or settings.first_name
        other_name = other_name or settings.other_name
        surname = surname or settings.surname
        maiden_name = maiden_name or settings.maiden_name
        previous_name = previous_name or settings.previous_name
        mobile_number = mobile_number or settings.mobile_number
        work_number = work_number or settings.work_number
        relationship = relationship or settings.relationship_1
        email = email or settings.email
        location = location or settings.location

        logger.info(f"🔐 Fill emergency contacts form")

        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.FIRST_NAME, first_name)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.OTHER_NAME, other_name)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.SURNAME, surname)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.MAIDEN_NAME, maiden_name)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.PREVIOUS_NAME, previous_name)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.MOBILE_NUMBER, mobile_number)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.WORK_NUMBER, work_number)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.RELATIONSHIP, relationship)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.EMAIL, email)
        self.fill_input(EDIT_EMERGENCY_CONTACT_PAGE.LOCATION, location)

        logger.info(f"🔐 Submit emergency contacts form")
        self.click_element(EDIT_EMERGENCY_CONTACT_PAGE.EDIT_CONTACT_BUTTON)
