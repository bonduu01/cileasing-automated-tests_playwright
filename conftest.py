from typing import Any, Generator

import pytest
from playwright.sync_api import Playwright, Page, Browser, BrowserContext, sync_playwright


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, Any, None]:
    """Session-scoped Playwright instance ."""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, Any, None]:
    """Session-scoped browser fixture. Browser is created once and reused across all tests_pages."""
    browser = playwright_instance.chromium.launch(headless=True)
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, Any, None]:
    """Function-scoped context fixture. New context for each test (isolated cookies, storage, etc.)."""
    context = browser.new_context(accept_downloads=True)
    # context = browser.new_context(record_video_dir="videos/", record_har_path="trace.har")
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, Any, None]:
    """Function-scoped page fixture. New page for each test."""
    page = context.new_page()
    yield page
    page.close()
