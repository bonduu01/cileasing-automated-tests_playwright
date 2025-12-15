"""Optimized BasePage class with enhanced functionality and best practices."""
import re
import os
from pathlib import Path
from typing import Optional, Literal, Pattern, Union
from playwright.sync_api import Page, expect, Locator, Download, ElementHandle


class BasePage:
    """Base page object with common web automation methods."""

    # Default timeout values (can be overridden)
    DEFAULT_TIMEOUT = 30000  # 30 seconds
    DEFAULT_NAVIGATION_TIMEOUT = 30000

    def __init__(self, page: Page, base_url: str = ""):
        """
        Initialize BasePage.

        Args:
            page: Playwright Page instance
            base_url: Optional base URL for relative navigation
        """
        self.page = page
        self.base_url = base_url.rstrip("/") if base_url else ""

    # Navigation Methods

    def navigate_to(
            self,
            url: str,
            wait_until: Literal["load", "domcontentloaded", "networkidle", "commit"] = "domcontentloaded",
            timeout: Optional[int] = None
    ) -> None:
        """
        Navigate to a URL with configurable wait strategy.

        Args:
            url: URL to navigate to (absolute or relative to base_url)
            wait_until: When to consider navigation succeeded
            timeout: Maximum time in milliseconds
        """
        full_url = f"{self.base_url}{url}" if url.startswith("/") and self.base_url else url
        self.page.goto(full_url, wait_until=wait_until, timeout=timeout or self.DEFAULT_NAVIGATION_TIMEOUT)

    def reload_page(self, wait_until: str = "domcontentloaded") -> None:
        """Reload the current page."""
        self.page.reload(wait_until=wait_until)

    def go_back(self) -> None:
        """Navigate back in browser history."""
        self.page.go_back()

    def go_forward(self) -> None:
        """Navigate forward in browser history."""
        self.page.go_forward()

    # Locator Methods

    def get_locator(self, selector: str, **kwargs) -> Locator:
        """
        Get a locator for an element.

        Args:
            selector: CSS selector, text, or other selector
            **kwargs: Additional locator options (has_text, has, etc.)

        Returns:
            Locator object
        """
        return self.page.locator(selector, **kwargs)

    def get_by_role(
            self,
            role: str,
            name: Optional[Union[str, Pattern]] = None,
            **kwargs
    ) -> Locator:
        """Get element by ARIA role."""
        return self.page.get_by_role(role, name=name, **kwargs)

    def get_by_text(self, text: Union[str, Pattern], exact: bool = False) -> Locator:
        """Get element by text content."""
        return self.page.get_by_text(text, exact=exact)

    def get_by_label(self, text: Union[str, Pattern]) -> Locator:
        """Get form element by associated label."""
        return self.page.get_by_label(text)

    def get_by_placeholder(self, text: Union[str, Pattern]) -> Locator:
        """Get element by placeholder text."""
        return self.page.get_by_placeholder(text)

    def get_by_test_id(self, test_id: str) -> Locator:
        """Get element by data-testid attribute."""
        return self.page.get_by_test_id(test_id)

    # Interaction Methods

    def click(
            self,
            selector: str,
            timeout: Optional[int] = None,
            force: bool = False,
            **kwargs
    ) -> None:
        """
        Click an element with auto-wait.

        Args:
            selector: Element selector
            timeout: Maximum time to wait
            force: Whether to force click bypassing actionability checks
            **kwargs: Additional click options (button, click_count, position, etc.)
        """
        self.page.locator(selector).click(
            timeout=timeout or self.DEFAULT_TIMEOUT,
            force=force,
            **kwargs
        )

    def click_and_wait_for_navigation(
            self,
            selector: str,
            wait_until: str = "domcontentloaded"
    ) -> None:
        """Click element and wait for navigation to complete."""
        with self.page.expect_navigation(wait_until=wait_until):
            self.click(selector)

    def double_click(self, selector: str, **kwargs) -> None:
        """Double-click an element."""
        self.page.locator(selector).dblclick(**kwargs)

    def right_click(self, selector: str, **kwargs) -> None:
        """Right-click an element."""
        self.page.locator(selector).click(button="right", **kwargs)

    def hover(self, selector: str, timeout: Optional[int] = None) -> None:
        """Hover over an element."""
        self.page.locator(selector).hover(timeout=timeout or self.DEFAULT_TIMEOUT)

    def focus(self, selector: str) -> None:
        """Focus on an element."""
        self.page.locator(selector).focus()

    # Form Interaction Methods

    def fill(
            self,
            selector: str,
            value: str,
            timeout: Optional[int] = None,
            force: bool = False
    ) -> None:
        """
        Fill input field (clears existing value first).

        Args:
            selector: Input selector
            value: Value to fill
            timeout: Maximum time to wait
            force: Whether to bypass actionability checks
        """
        self.page.locator(selector).fill(value, timeout=timeout or self.DEFAULT_TIMEOUT, force=force)

    def type(
            self,
            selector: str,
            text: str,
            delay: int = 0,
            timeout: Optional[int] = None
    ) -> None:
        """
        Type text character by character (doesn't clear existing value).

        Args:
            selector: Input selector
            text: Text to type
            delay: Delay in milliseconds between key presses
            timeout: Maximum time to wait
        """
        self.page.locator(selector).type(text, delay=delay, timeout=timeout or self.DEFAULT_TIMEOUT)

    def clear(self, selector: str) -> None:
        """Clear an input field."""
        self.page.locator(selector).clear()

    def check(self, selector: str, timeout: Optional[int] = None) -> None:
        """Check a checkbox or radio button."""
        self.page.locator(selector).check(timeout=timeout or self.DEFAULT_TIMEOUT)

    def uncheck(self, selector: str, timeout: Optional[int] = None) -> None:
        """Uncheck a checkbox."""
        self.page.locator(selector).uncheck(timeout=timeout or self.DEFAULT_TIMEOUT)

    def select_option(
            self,
            selector: str,
            value: Optional[Union[str, list[str]]] = None,
            label: Optional[Union[str, list[str]]] = None,
            index: Optional[Union[int, list[int]]] = None
    ) -> None:
        """
        Select option(s) from dropdown.

        Args:
            selector: Select element selector
            value: Option value(s) to select
            label: Option label(s) to select
            index: Option index(es) to select
        """
        locator = self.page.locator(selector)
        if value is not None:
            locator.select_option(value)
        elif label is not None:
            locator.select_option(label=label)
        elif index is not None:
            locator.select_option(index=index)
        else:
            raise ValueError("Must provide value, label, or index")

    def upload_file(
            self,
            selector: str,
            file_path: Union[str, Path, list[Union[str, Path]]],
            timeout: Optional[int] = None
    ) -> None:
        """
        Upload file(s) to an input element.

        Args:
            selector: File input selector
            file_path: Path to file(s)
            timeout: Maximum time to wait
        """
        # Convert Path objects to strings
        if isinstance(file_path, list):
            file_path = [str(p) for p in file_path]
        else:
            file_path = str(file_path)

        self.page.locator(selector).set_input_files(
            file_path,
            timeout=timeout or self.DEFAULT_TIMEOUT
        )

    def clear_files(self, selector: str) -> None:
        """Clear file input."""
        self.page.locator(selector).set_input_files([])

    # Content Retrieval Methods

    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        Get text content of an element.

        Args:
            selector: Element selector
            timeout: Maximum time to wait

        Returns:
            Text content (stripped of whitespace)
        """
        locator = self.page.locator(selector)
        locator.wait_for(state="visible", timeout=timeout or self.DEFAULT_TIMEOUT)
        text = locator.text_content()
        return text.strip() if text else ""

    def get_inner_text(self, selector: str) -> str:
        """Get rendered inner text (respects CSS)."""
        return self.page.locator(selector).inner_text().strip()

    def get_value(self, selector: str) -> str:
        """Get input value."""
        return self.page.locator(selector).input_value()

    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get element attribute value."""
        return self.page.locator(selector).get_attribute(attribute)

    def get_all_text_contents(self, selector: str) -> list[str]:
        """Get text content of all matching elements."""
        return [text.strip() for text in self.page.locator(selector).all_text_contents()]

    def count_elements(self, selector: str) -> int:
        """Count number of elements matching selector."""
        return self.page.locator(selector).count()

    def is_visible(self, selector: str, timeout: int = 1000) -> bool:
        """Check if element is visible."""
        try:
            return self.page.locator(selector).is_visible(timeout=timeout)
        except Exception:
            return False

    def is_hidden(self, selector: str) -> bool:
        """Check if element is hidden."""
        return self.page.locator(selector).is_hidden()

    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled."""
        return self.page.locator(selector).is_enabled()

    def is_disabled(self, selector: str) -> bool:
        """Check if element is disabled."""
        return self.page.locator(selector).is_disabled()

    def is_checked(self, selector: str) -> bool:
        """Check if checkbox/radio is checked."""
        return self.page.locator(selector).is_checked()

    # Wait Methods

    def wait_for_selector(
            self,
            selector: str,
            state: Literal["attached", "detached", "visible", "hidden"] = "visible",
            timeout: Optional[int] = None
    ) -> None:
        """
        Wait for element to reach specified state.

        Args:
            selector: Element selector
            state: State to wait for
            timeout: Maximum time to wait
        """
        self.page.locator(selector).wait_for(state=state, timeout=timeout or self.DEFAULT_TIMEOUT)

    def wait_for_url(
            self,
            url: Union[str, Pattern],
            timeout: Optional[int] = None,
            wait_until: str = "load"
    ) -> None:
        """Wait for URL to match pattern."""
        self.page.wait_for_url(url, timeout=timeout or self.DEFAULT_TIMEOUT, wait_until=wait_until)

    def wait_for_load_state(
            self,
            state: Literal["load", "domcontentloaded", "networkidle"] = "load",
            timeout: Optional[int] = None
    ) -> None:
        """Wait for page load state."""
        self.page.wait_for_load_state(state, timeout=timeout)

    def wait(self, milliseconds: int) -> None:
        """Hard wait (use sparingly, prefer wait_for_selector)."""
        self.page.wait_for_timeout(milliseconds)

    def wait_for_function(self, expression: str, timeout: Optional[int] = None) -> None:
        """Wait for JavaScript expression to return truthy value."""
        self.page.wait_for_function(expression, timeout=timeout or self.DEFAULT_TIMEOUT)

    # Assertion Methods (using Playwright's auto-waiting assertions)

    def assert_title(self, expected: Union[str, Pattern], timeout: Optional[int] = None) -> None:
        """Assert page title."""
        expect(self.page).to_have_title(expected, timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_url(self, expected: Union[str, Pattern], timeout: Optional[int] = None) -> None:
        """Assert page URL."""
        expect(self.page).to_have_url(expected, timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_hidden(self, selector: str, timeout: Optional[int] = None) -> None:
        """Assert element is hidden."""
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_enabled(self, selector: str, timeout: Optional[int] = None) -> None:
        """Assert element is enabled."""
        expect(self.page.locator(selector)).to_be_enabled(timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_disabled(self, selector: str, timeout: Optional[int] = None) -> None:
        """Assert element is disabled."""
        expect(self.page.locator(selector)).to_be_disabled(timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_checked(self, selector: str, timeout: Optional[int] = None) -> None:
        """Assert checkbox/radio is checked."""
        expect(self.page.locator(selector)).to_be_checked(timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_text(self, selector: str, expected: Union[str, Pattern], timeout: Optional[int] = None) -> None:
        """Assert element has exact text."""
        expect(self.page.locator(selector)).to_have_text(expected, timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_contains_text(self, selector: str, expected: Union[str, Pattern], timeout: Optional[int] = None) -> None:
        """Assert element contains text."""
        expect(self.page.locator(selector)).to_contain_text(expected, timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_value(self, selector: str, expected: Union[str, Pattern], timeout: Optional[int] = None) -> None:
        """Assert input has value."""
        expect(self.page.locator(selector)).to_have_value(expected, timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_attribute(
            self,
            selector: str,
            name: str,
            value: Union[str, Pattern],
            timeout: Optional[int] = None
    ) -> None:
        """Assert element has attribute with value."""
        expect(self.page.locator(selector)).to_have_attribute(
            name, value, timeout=timeout or self.DEFAULT_TIMEOUT
        )

    def assert_count(self, selector: str, count: int, timeout: Optional[int] = None) -> None:
        """Assert number of elements matching selector."""
        expect(self.page.locator(selector)).to_have_count(count, timeout=timeout or self.DEFAULT_TIMEOUT)

    def assert_text_visible(self, text: Union[str, Pattern], timeout: Optional[int] = None) -> None:
        """Assert text is visible on page."""
        expect(self.page.get_by_text(text)).to_be_visible(timeout=timeout or self.DEFAULT_TIMEOUT)

    # Scroll Methods

    def scroll_to_element(self, selector: str) -> None:
        """Scroll element into view if needed."""
        self.page.locator(selector).scroll_into_view_if_needed()

    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        self.page.evaluate("window.scrollTo(0, 0)")

    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_by(self, x: int = 0, y: int = 0) -> None:
        """Scroll by specified pixels."""
        self.page.evaluate(f"window.scrollBy({x}, {y})")

    # Download Methods

    def download_file(
            self,
            selector: str,
            save_path: Union[str, Path],
            expected_extensions: Optional[list[str]] = None,
            timeout: Optional[int] = None
    ) -> Path:
        """
        Click element to trigger download and save file.

        Args:
            selector: Element that triggers download
            save_path: Path to save downloaded file
            expected_extensions: List of valid file extensions (e.g., ['.pdf', '.txt'])
            timeout: Maximum time to wait for download

        Returns:
            Path object of saved file

        Raises:
            AssertionError: If file validation fails
        """
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)

        with self.page.expect_download(timeout=timeout or self.DEFAULT_TIMEOUT) as download_info:
            self.click(selector)

        download: Download = download_info.value

        # Save file
        download.save_as(str(save_path))

        # Validate download
        actual_path = Path(download.path())
        assert actual_path.exists(), f"Downloaded file not found at {actual_path}"

        filename = download.suggested_filename

        # Validate extension if specified
        if expected_extensions:
            file_ext = Path(filename).suffix.lower()
            assert file_ext in expected_extensions, \
                f"Unexpected file type: {filename}. Expected one of {expected_extensions}"

        print(f"✓ Download successful: {filename} → {save_path}")
        return save_path

    # JavaScript Execution

    def execute_script(self, script: str, *args) -> any:
        """Execute JavaScript in page context."""
        return self.page.evaluate(script, *args)

    def add_script_tag(self, content: Optional[str] = None, url: Optional[str] = None) -> None:
        """Add script tag to page."""
        self.page.add_script_tag(content=content, url=url)

    def add_style_tag(self, content: Optional[str] = None, url: Optional[str] = None) -> None:
        """Add style tag to page."""
        self.page.add_style_tag(content=content, url=url)

    # Screenshot Methods

    def screenshot(
            self,
            path: Optional[Union[str, Path]] = None,
            full_page: bool = False,
            **kwargs
    ) -> bytes:
        """
        Take screenshot of page.

        Args:
            path: Path to save screenshot
            full_page: Capture full scrollable page
            **kwargs: Additional screenshot options

        Returns:
            Screenshot as bytes
        """
        return self.page.screenshot(path=str(path) if path else None, full_page=full_page, **kwargs)

    def screenshot_element(self, selector: str, path: Optional[Union[str, Path]] = None) -> bytes:
        """Take screenshot of specific element."""
        return self.page.locator(selector).screenshot(path=str(path) if path else None)

    # Keyboard & Mouse Actions

    def press_key(self, key: str, delay: int = 0) -> None:
        """Press a keyboard key."""
        self.page.keyboard.press(key, delay=delay)

    def press_keys(self, *keys: str) -> None:
        """Press multiple keys in sequence."""
        for key in keys:
            self.page.keyboard.press(key)

    def keyboard_type(self, text: str, delay: int = 0) -> None:
        """Type text using keyboard."""
        self.page.keyboard.type(text, delay=delay)

    # Dialog Handling

    def handle_dialog(self, accept: bool = True, prompt_text: Optional[str] = None) -> None:
        """
        Set up dialog handler for next dialog.

        Args:
            accept: Whether to accept or dismiss dialog
            prompt_text: Text to enter in prompt dialog
        """

        def handle(dialog):
            if prompt_text:
                dialog.accept(prompt_text)
            elif accept:
                dialog.accept()
            else:
                dialog.dismiss()

        self.page.once("dialog", handle)

    # Frame Handling

    def get_frame(self, name: str) -> Optional[Page]:
        """Get frame by name."""
        return self.page.frame(name)

    def get_frame_locator(self, selector: str) -> Locator:
        """Get frame locator for working with iframes."""
        return self.page.frame_locator(selector)

    # Cookie Methods

    def get_cookies(self) -> list[dict]:
        """Get all cookies."""
        return self.page.context.cookies()

    def add_cookies(self, cookies: list[dict]) -> None:
        """Add cookies to browser context."""
        self.page.context.add_cookies(cookies)

    def clear_cookies(self) -> None:
        """Clear all cookies."""
        self.page.context.clear_cookies()

    # Storage Methods

    def get_local_storage(self, key: str) -> Optional[str]:
        """Get item from localStorage."""
        return self.page.evaluate(f"() => localStorage.getItem('{key}')")

    def set_local_storage(self, key: str, value: str) -> None:
        """Set item in localStorage."""
        self.page.evaluate(f"() => localStorage.setItem('{key}', '{value}')")

    def clear_local_storage(self) -> None:
        """Clear localStorage."""
        self.page.evaluate("() => localStorage.clear()")

    # Utility Methods

    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()

    def bring_to_front(self) -> None:
        """Bring page to front (activate tab)."""
        self.page.bring_to_front()

    def close(self) -> None:
        """Close the page."""
        self.page.close()

    def pause(self) -> None:
        """Pause test execution for debugging (opens Playwright Inspector)."""
        self.page.pause()