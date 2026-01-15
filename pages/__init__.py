"""Page Objects module."""
from pages.add_bank_details_page import AddBankDetailsPage
from pages.base_page import BasePage
from pages.edit_self_service_page import EditSelfServicePage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.self_service_page import SelfServicePage

__all__ = ["BasePage", "HomePage", "LoginPage", "SelfServicePage", "EditSelfServicePage", "AddBankDetailsPage"]
