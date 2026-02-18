# pages/base_page.py

"""
Base Page Object providing common interactions for all page objects.
"""

from __future__ import annotations

import os
import re
import logging
import time
from typing import TYPE_CHECKING

from playwright.sync_api import Page, expect, Locator, Download
from utils.decorators import log_method

if TYPE_CHECKING:
    from playwright.sync_api import Response

logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all Page Objects with common functionality."""

    def __init__(self, page: Page) -> None:
        self.page = page
        logger.info(f"🏗️ Initialized {self.__class__.__name__}")

    # --- Navigation ---

    @log_method
    def navigate_to(self, url: str, wait_until: str = "networkidle") -> Response | None:
        """Navigate to a URL and wait for the specified load state."""
        logger.info(f"🌐 URL: {url}, Wait: {wait_until}")
        try:
            response = self.page.goto(url, wait_until=wait_until)
            if response:
                logger.info(f"   📊 Status: {response.status}, OK: {response.ok}")
            return response
        except Exception as e:
            logger.error(f"   ❌ Navigation failed: {e}")
            self._take_screenshot("navigation_error")
            raise

    @log_method
    def reload(self, wait_until: str = "domcontentloaded") -> Response | None:
        """Reload the current page."""
        logger.info(f"🔄 Reloading page")
        return self.page.reload(wait_until=wait_until)

    @log_method
    def go_back(self, wait_until: str = "domcontentloaded") -> Response | None:
        """Navigate back in browser history."""
        logger.info(f"⬅️ Going back")
        return self.page.go_back(wait_until=wait_until)

    # --- Element Interaction ---

    @log_method
    def click_element(self, selector: str, timeout: int = 30000, **kwargs) -> None:
        """
        Click an element identified by selector with proper waits.

        Args:
            selector: CSS selector or locator string
            timeout: Timeout in milliseconds (default: 30000)
            **kwargs: Additional click options (force, button, etc.)
        """
        logger.info(f"🖱️ Selector: {selector}")
        try:
            locator = self.page.locator(selector)

            # Log element state before interaction
            self._log_element_state(locator, selector)

            # Wait for element to be attached
            locator.wait_for(state="attached", timeout=timeout)

            # Wait for element to be visible
            locator.wait_for(state="visible", timeout=timeout)

            # Scroll into view if needed
            locator.scroll_into_view_if_needed(timeout=timeout)

            # Wait for element to be enabled
            expect(locator).to_be_enabled(timeout=timeout)

            # Click the element
            locator.click(timeout=timeout, **kwargs)

            logger.info(f"   ✅ Click successful")
        except Exception as e:
            logger.error(f"   ❌ Click failed: {e}")
            self._take_screenshot(f"click_error")
            raise

    @log_method
    def fill_input(self, selector: str, value: str, timeout: int = 30000) -> None:
        """Fill an input field with the specified value."""
        logger.info(f"✍️ Selector: {selector}, Value: {value}")
        try:
            locator = self.page.locator(selector)

            # Log element state
            self._log_element_state(locator, selector)

            # Wait for element to be visible
            locator.wait_for(state="visible", timeout=timeout)

            # Scroll into view
            locator.scroll_into_view_if_needed(timeout=timeout)

            # Fill the input
            self.page.fill(selector, value)

            # Verify value was set
            expect(locator).to_have_value(value, timeout=5000)

            logger.info(f"   ✅ Fill successful")
        except Exception as e:
            logger.error(f"   ❌ Fill failed: {e}")
            self._take_screenshot(f"fill_error")
            raise

    @log_method
    def type_text(self, selector: str, text: str, delay: float = 0) -> None:
        """Type text into an element character by character."""
        logger.info(f"⌨️ Selector: {selector}, Text length: {len(text)}, Delay: {delay}ms")
        self.page.type(selector, text, delay=delay)

    @log_method
    def clear_input(self, selector: str) -> None:
        """Clear the content of an input field."""
        logger.info(f"🧹 Clearing: {selector}")
        self.page.fill(selector, "")

    def check_checkbox(self, selector: str) -> None:
        """Check a checkbox or radio button."""
        logger.info(f"☑️ Checking: {selector}")
        self.page.locator(selector).check()

    def uncheck_checkbox(self, selector: str) -> None:
        """Uncheck a checkbox."""
        logger.info(f"☐ Unchecking: {selector}")
        self.page.locator(selector).uncheck()

    def select_dropdown_option(
            self, selector: str, value: str | None = None, label: str | None = None
    ) -> list[str]:
        """Select an option from a dropdown."""
        logger.info(f"📋 Selecting dropdown: {selector}, Value: {value}, Label: {label}")
        locator = self.page.locator(selector)
        if label:
            return locator.select_option(label=label)
        return locator.select_option(value=value)

    # base_page.py
    def ant_select_date_picker(self, selector: str, date_value: str):
        input_field = self.page.locator(selector)
        input_field.wait_for(state="visible", timeout=5000)
        input_field.clear()
        input_field.fill(date_value)
    # base_page.py

    def ant_select_option(self, dropdown_locator: str, option_text: str):
        """
        Stable Ant Design Select handler.
        Handles virtualized lists and dynamic rendering.
        """

        # 1️⃣ Wait for any loading spinner
        logger.info("📋 Waiting for dropdown to finish loading...")
        try:
            self.page.locator(".ant-select-loading").wait_for(
                state="hidden", timeout=15_000
            )
            logger.info("✅ Dropdown finished loading")
        except:
            logger.info("ℹ️ No loading state detected")

        # 2️⃣ Open dropdown
        logger.info(f"📋 Opening dropdown: {dropdown_locator}")
        self.page.locator(dropdown_locator).click()

        # 3️⃣ Wait for visible dropdown panel
        dropdown = self.page.locator(
            ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"
        )
        dropdown.wait_for(state="visible", timeout=10_000)
        logger.info("✅ Dropdown panel visible")

        # 4️⃣ Try selecting using role (BEST METHOD)
        try:
            option = self.page.get_by_role("option", name=option_text)

            option.wait_for(state="visible", timeout=5_000)
            option.click()

            logger.info(f"✅ Selected: {option_text}")
            dropdown.wait_for(state="hidden", timeout=5_000)
            return

        except Exception:
            logger.info("⚠️ Role-based selection failed, trying fallback...")

        # 5️⃣ Fallback: Use title attribute inside visible dropdown
        option = dropdown.locator(
            f".ant-select-item-option[title='{option_text}']"
        )

        option.wait_for(state="visible", timeout=5_000)
        option.click()

        logger.info(f"✅ Selected (fallback): {option_text}")
        dropdown.wait_for(state="hidden", timeout=5_000)

    def upload_file(self, selector: str, file_path: str | list[str]) -> None:
        """Upload file(s) to a file input."""
        logger.info(f"📤 Uploading file: {file_path} to {selector}")
        self.page.set_input_files(selector, file_path)

    def hover_element(self, selector: str) -> None:
        """Hover over an element."""
        logger.info(f"🖱️ Hovering: {selector}")
        self.page.hover(selector)

    def press_key(self, selector: str, key: str) -> None:
        """Press a key while focused on an element."""
        logger.info(f"⌨️ Pressing key '{key}' on: {selector}")
        self.page.press(selector, key)

    # --- Element Getters ---

    def get_locator(self, selector: str) -> Locator:
        """Get a locator for the specified selector."""
        return self.page.locator(selector)

    def get_role(self, role: str, name: str | None = None, **kwargs) -> Locator:
        """Get element by ARIA role."""
        return self.page.get_by_role(role, name=name, **kwargs)

    def get_by_text(self, text: str, exact: bool = False) -> Locator:
        """Get element by text content."""
        return self.page.get_by_text(text, exact=exact)

    def get_by_label(self, label: str, exact: bool = False) -> Locator:
        """Get element by associated label."""
        return self.page.get_by_label(label, exact=exact)

    def get_by_placeholder(self, placeholder: str, exact: bool = False) -> Locator:
        """Get element by placeholder attribute."""
        return self.page.get_by_placeholder(placeholder, exact=exact)

    def get_by_test_id(self, test_id: str) -> Locator:
        """Get element by data-testid attribute."""
        return self.page.get_by_test_id(test_id)

    # --- Text Extraction ---

    def get_value_from_selector(self, selector: str) -> str:
        """Get the text content of an element."""
        text = self.page.locator(selector).first.text_content()
        return text.strip() if text else ""

    def get_inner_text(self, selector: str) -> str:
        """Get the inner text of an element."""
        return self.page.locator(selector).first.inner_text()

    def get_input_value(self, selector: str) -> str:
        """Get the value of an input element."""
        return self.page.locator(selector).input_value()

    def get_attribute(self, selector: str, attribute: str) -> str | None:
        """Get an attribute value from an element."""
        return self.page.locator(selector).first.get_attribute(attribute)

    # --- Assertions ---

    @log_method
    def verify_title(self, expected_title: str | re.Pattern) -> None:
        """Assert the page title matches expected value."""
        logger.info(f"📄 Verifying title: {expected_title}")
        expect(self.page).to_have_title(expected_title)

    @log_method
    def verify_url(self, expected_url: str | re.Pattern) -> None:
        """Assert the page URL matches expected value."""
        logger.info(f"🔗 Verifying URL: {expected_url}")
        expect(self.page).to_have_url(expected_url)

    @log_method
    def verify_element_visible(self, selector: str, timeout: float | None = None) -> None:
        """Assert an element is visible."""
        logger.info(f"👁️ Verifying visible: {selector}")
        try:
            expect(self.page.locator(selector)).to_be_visible(timeout=timeout)
            logger.info(f"   ✅ Element is visible")
        except Exception as e:
            logger.error(f"   ❌ Element not visible: {e}")
            self._take_screenshot("verify_visible_error")
            raise

    @log_method
    def verify_element_hidden(self, selector: str, timeout: float | None = None) -> None:
        """Assert an element is hidden."""
        logger.info(f"🙈 Verifying hidden: {selector}")
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)

    def verify_element_is_enabled(self, selector: str) -> None:
        """Assert an element is enabled."""
        logger.info(f"✅ Verifying enabled: {selector}")
        expect(self.page.locator(selector)).to_be_enabled()

    def verify_element_is_disabled(self, selector: str, timeout: float | None = None) -> None:
        """Assert an element is disabled."""
        logger.info(f"🚫 Verifying disabled: {selector}")
        locator = self.page.locator(selector)
        locator.wait_for(state="attached", timeout=timeout or 10000)
        expect(locator).to_be_disabled()

    @log_method
    def verify_selector_to_have_text(self, selector: str, expected_text: str | re.Pattern) -> None:
        """Assert an element has exact text."""
        logger.info(f"📝 Verifying text - Selector: {selector}, Expected: {expected_text}")
        expect(self.page.locator(selector)).to_have_text(expected_text)

    @log_method
    def verify_text_visible(self, text: str) -> None:
        """Assert text is visible on the page."""
        logger.info(f"📝 Verifying text visible: {text}")
        expect(self.page.get_by_text(text)).to_be_visible()

    @log_method
    def verify_has_text_visible(self, selector: str, text: str) -> None:
        """Assert element with specific text is visible."""
        logger.info(f"📝 Verifying text visible - Selector: {selector}, Text: {text}")
        try:
            expect(self.page.locator(selector, has_text=text)).to_be_visible()
            logger.info(f"   ✅ Text is visible")
        except Exception as e:
            logger.error(f"   ❌ Text not visible: {e}")
            self._take_screenshot("verify_text_error")
            raise

    def verify_element_to_contain_text(
            self, selector: str, expected_text: str | re.Pattern
    ) -> None:
        """Assert an element contains text."""
        logger.info(f"📝 Verifying contains text: {selector} contains {expected_text}")
        expect(self.page.locator(selector)).to_contain_text(expected_text)

    def verify_element_has_value(self, selector: str, expected_value: str | re.Pattern) -> None:
        """Assert an input has the expected value."""
        logger.info(f"📝 Verifying value: {selector} = {expected_value}")
        expect(self.page.locator(selector)).to_have_value(expected_value)

    def verify_element_checked(self, selector: str) -> None:
        """Assert a checkbox/radio is checked."""
        logger.info(f"☑️ Verifying checked: {selector}")
        expect(self.page.locator(selector)).to_be_checked()

    def verify_element_not_checked(self, selector: str) -> None:
        """Assert a checkbox/radio is not checked."""
        logger.info(f"☐ Verifying not checked: {selector}")
        expect(self.page.locator(selector)).not_to_be_checked()

    @log_method
    def verify_validation_error(self, error_text: str, timeout: float = 5000) -> None:
        """Verify validation error message is visible."""
        logger.info(f"⚠️ Verifying validation error: {error_text}")
        error_locator = self.page.get_by_text(error_text, exact=True)
        expect(error_locator).to_be_visible(timeout=timeout)

    def verify_field_error_by_text(self, error_text: str) -> None:
        """Verify field validation error by text content."""
        logger.info(f"⚠️ Verifying field error: {error_text}")
        self.verify_text_visible(error_text)

    def get_validation_error_text(self, selector: str = 'p.text-xs.mt-1') -> str:
        """Get validation error text from error paragraph."""
        return self.get_value_from_selector(selector)

    @log_method
    def is_validation_error_visible(self, error_text: str) -> bool:
        """Check if validation error with specific text is visible."""
        logger.info(f"🔍 Checking validation error visibility: {error_text}")
        result = self.page.get_by_text(error_text).is_visible()
        logger.info(f"   Result: {result}")
        return result

    def wait_for_validation_error(self, error_text: str, timeout: float = 5000):
        """Wait for validation error to appear."""
        logger.info(f"⏳ Waiting for validation error: {error_text}")
        error_locator = self.page.get_by_text(error_text)
        error_locator.wait_for(state="visible", timeout=timeout)
        return error_locator

    def verify_error_text_color(self, selector: str = 'p.text-\\[red\\]') -> None:
        """Verify error text has red color class."""
        logger.info(f"🎨 Verifying error text color: {selector}")
        self.verify_element_visible(selector)

    def verify_input_value_length(self, selector: str, expected_length: int):
        """Verifies that an input element's value has the expected character length."""
        element = self.page.locator(selector)
        logger.info(f"🎨 Verifying error text color: {selector}")
        # Ensure element is visible first
        expect(element).to_be_visible()

        # Use a custom assertion with expect for length validation
        expect(element).to_have_value(
            re.compile(f"^.{{{expected_length}}}$")
        )
    # --- Waiting ---

    @log_method
    def wait_for_selector(
            self, selector: str, state: str = "visible", timeout: float | None = None
    ) -> Locator:
        """Wait for a selector to reach the specified state."""
        logger.info(f"⏳ Waiting for: {selector}, State: {state}")
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
        return self.page.locator(selector)

    @log_method
    def wait_for_url(self, url: str | re.Pattern, timeout: float | None = None) -> None:
        """Wait for navigation to a URL."""
        logger.info(f"⏳ Waiting for URL: {url}")
        self.page.wait_for_url(url, timeout=timeout)

    def wait_for_load_state(self, state: str = "load") -> None:
        """Wait for a specific load state."""
        logger.info(f"⏳ Waiting for load state: {state}")
        self.page.wait_for_load_state(state)

    def wait(self, milliseconds: float) -> None:
        """Wait for a specified duration (use sparingly)."""
        logger.info(f"⏱️ Waiting for {milliseconds}ms")
        self.page.wait_for_timeout(milliseconds)

    # --- Scrolling ---

    def scroll_to_element(self, selector: str) -> None:
        """Scroll element into view."""
        logger.info(f"📜 Scrolling to: {selector}")
        self.page.locator(selector).scroll_into_view_if_needed()

    def scroll_to_txt_via_element(self, selector: str, text: str) -> None:
        """Scroll to an element containing specific text."""
        logger.info(f"📜 Scrolling to text: {text} in {selector}")
        self.page.locator(selector, has_text=text).scroll_into_view_if_needed()

    def scroll_down(self) -> None:
        """Scroll to the bottom of the page."""
        logger.info("📜 Scrolling down to bottom")
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self) -> None:
        """Scroll to the top of the page."""
        logger.info("📜 Scrolling to top")
        self.page.evaluate("window.scrollTo(0, 0)")

    # --- Downloads ---

    @log_method
    def click_and_verify_download(
            self,
            selector: str,
            save_path: str,
            expected_extensions: tuple[str, ...] = (".txt", ".pdf", ".csv", ".xlsx"),
    ) -> Download:
        """Click an element and handle the resulting file download."""
        logger.info(f"📥 Initiating download - Selector: {selector}, Save: {save_path}")

        with self.page.expect_download() as download_info:
            self.click_element(selector)

        download = download_info.value
        download.save_as(save_path)

        # Validate download
        actual_path = download.path()
        assert actual_path and os.path.exists(actual_path), (
            f"Downloaded file not found at {actual_path}"
        )

        filename = download.suggested_filename
        assert filename.endswith(expected_extensions), (
            f"Unexpected file type: {filename}, expected one of {expected_extensions}"
        )

        logger.info(f"   ✅ Download successful: {actual_path}")
        return download

    # --- Screenshots ---

    def screenshot(self, path: str, full_page: bool = False) -> bytes:
        """Take a screenshot of the page."""
        logger.info(f"📸 Taking screenshot: {path}")
        return self.page.screenshot(path=path, full_page=full_page)

    def screenshot_element(self, selector: str, path: str) -> bytes:
        """Take a screenshot of a specific element."""
        logger.info(f"📸 Taking element screenshot: {selector} -> {path}")
        return self.page.locator(selector).screenshot(path=path)

    # --- JavaScript Execution ---

    def evaluate(self, expression: str):
        """Execute JavaScript in the page context."""
        logger.info(f"⚙️ Evaluating JS: {expression[:50]}...")
        return self.page.evaluate(expression)

    # --- State Checks ---

    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible."""
        result = self.page.locator(selector).is_visible()
        logger.debug(f"👁️ Is visible '{selector}': {result}")
        return result

    def is_enabled(self, selector: str) -> bool:
        """Check if an element is enabled."""
        result = self.page.locator(selector).is_enabled()
        logger.debug(f"✅ Is enabled '{selector}': {result}")
        return result

    def is_checked(self, selector: str) -> bool:
        """Check if a checkbox/radio is checked."""
        result = self.page.locator(selector).is_checked()
        logger.debug(f"☑️ Is checked '{selector}': {result}")
        return result

    def count_elements(self, selector: str) -> int:
        """Count the number of elements matching the selector."""
        count = self.page.locator(selector).count()
        logger.debug(f"🔢 Count '{selector}': {count}")
        return count

    # --- Helper Methods for Logging ---

    def _log_element_state(self, locator: Locator, selector: str):
        """Log detailed element state information."""
        try:
            count = locator.count()
            logger.info(f"   🔍 Element state - Count: {count}")

            if count > 0:
                is_visible = locator.first.is_visible()
                is_enabled = locator.first.is_enabled()
                logger.info(f"      Visible: {is_visible}, Enabled: {is_enabled}")

                # Try to get text content
                try:
                    text = locator.first.text_content()
                    if text and text.strip():
                        logger.info(f"      Text: '{text.strip()[:50]}'")
                except:
                    pass
            else:
                logger.warning(f"   ⚠️ Element not found in DOM: {selector}")

        except Exception as e:
            logger.warning(f"   ⚠️ Could not log element state: {e}")

    def _take_screenshot(self, name: str):
        """Take screenshot for debugging."""
        try:
            timestamp = int(time.time())
            filename = f"screenshots/{name}_{timestamp}.png"

            # Create screenshots directory if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)

            self.page.screenshot(path=filename, full_page=True)
            logger.info(f"   📸 Screenshot saved: {filename}")
        except Exception as e:
            logger.warning(f"   ⚠️ Screenshot failed: {e}")
