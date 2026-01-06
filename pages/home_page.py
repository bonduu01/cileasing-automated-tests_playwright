from pages.base_page import BasePage
from playwright.sync_api import Page

from utils.constants import HOME_PAGE_TITLE, BASE_URL, LOGIN_EMAIL_SELECTOR, LOGIN_PWD_SELECTOR, LOGIN_BUTTON_SELECTOR


class HomePage(BasePage):


    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def go_to_home_page(self):
        self.navigate_to(BASE_URL)

    def verify_home_page_loads(self):
        self.verify_title(HOME_PAGE_TITLE)
        self.verify_element_is_disabled("input[name='password'][type='password']")

    def login_user(self, email: str, password: str):
        self.fill_input(LOGIN_EMAIL_SELECTOR, email)
        self.fill_input(LOGIN_PWD_SELECTOR, password)
        self.click_element(LOGIN_BUTTON_SELECTOR)



