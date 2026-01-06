import re

from playwright.sync_api import Page, expect, TimeoutError
import os, time

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str, wait_until: str = "domcontentloaded") -> None:
        self.page.goto(url, wait_until=wait_until)

    def click_element(self, selector: str) -> None:
        self.page.click(selector)

    def get_value_from_selector(self, selector: str) -> str:
        """Returns the visible text content of an element specified by selector."""
        element = self.page.locator(selector).first
        value = element.text_content()
        return value.strip() if value else ""

    def get_role(self, role: str, role_name: str):
        self.page.get_by_role(role, name=role_name)

    def fill_input(self, selector: str, value: str) -> None:
        self.page.fill(selector, value)

    def check_checkbox(self, selector: str) -> None:
        self.page.locator(selector).check()

    def select_dropdown_option(self, selector: str, value: str) -> None:
        self.page.locator(selector).select_option(value)

    def upload_file(self, selector: str, file_path: str) -> None:
        self.page.set_input_files(selector, file_path)

    def verify_title(self, expected_title: str) -> None:
        expect(self.page).to_have_title(expected_title)

    def verify_text_visible(self, text: str) -> None:
        expect(self.page.get_by_text(text)).to_be_visible()

    def verify_has_text_visible(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector, has_text=text)).to_be_visible()

    def verify_element_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    def verify_url(self, expected_url: str) -> None:
        self.page.wait_for_url(expected_url)

    def verify_element_has_value(self, selector: str, expected_value: str) -> None:
        expect(self.page.locator(selector)).to_have_value(expected_value)

    def wait(self, milliseconds: int) -> None:
        self.page.wait_for_timeout(milliseconds)

    def wait_for_selector(self, selector: str):
        self.page.wait_for_selector(selector)

    def verify_element_to_contain_text(self, selector: str, expected_value: str):
        expect(self.page.locator(selector)).to_contain_text(expected_value)

    def verify_element_is_enabled(self, selector: str):
        expect(self.page.locator(selector)).to_be_enabled()

    def verify_element_is_disabled(self, selector: str):
        input_value = self.page.locator(selector)
        input_value.wait_for(state="attached", timeout=10000)
        # expect(self.page.locator(selector)).to_be_attached()
        expect(self.page.locator(selector)).to_be_disabled()

    def verify_selector_to_have_text(self, selector: str, expected_value: str):
        expect(self.page.locator(selector)).to_have_text(expected_value)

    def scroll_to_txt_via_element(self, selector: str, expected_value: str):
        self.page.locator(selector, has_text=expected_value).scroll_into_view_if_needed()

    def click_and_verify_download(self, selector: str, save_path: str) -> None:
        # Trigger download
        with self.page.expect_download() as download_info:
            self.click_element(selector)
        download = download_info.value
        # Save file to desired path
        download.save_as(save_path)
        # Get actual file path
        file_path_actual = download.path()
        # --- Validations ---
        assert file_path_actual and os.path.exists(file_path_actual), \
            f"Downloaded file not found at {file_path_actual}"
        filename = download.suggested_filename
        assert re.match(r".*\.(txt|pdf)$", filename), \
            f"Unexpected file type: {filename}"
        print(f"Download successful: {file_path_actual}")

    def scroll_down(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
