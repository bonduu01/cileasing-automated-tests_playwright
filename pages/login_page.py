from pages.base_page import BasePage
from playwright.sync_api import Page


class LoginPage(BasePage):
    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.BASE_URL = base_url

