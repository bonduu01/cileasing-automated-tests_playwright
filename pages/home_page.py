from pages.base_page import BasePage
from playwright.sync_api import Page

from utils.constants import  HOME_PAGE_TITLE


class HomePage(BasePage):
    HOME_PAGE_TITLE = HOME_PAGE_TITLE

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def go_to_home_page(self):
        self.navigate_to(self.base_url)
        self.wait_for_url(self.base_url)

    def verify_home_page_loads(self):
        self.assert_title(self.HOME_PAGE_TITLE)

