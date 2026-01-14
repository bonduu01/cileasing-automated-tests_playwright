"""
Pytest configuration and fixtures for Playwright tests.
Located at root directory for project-wide fixture access.
"""

from typing import Generator

import pytest
from playwright.sync_api import (
    Playwright,
    Browser,
    BrowserContext,
    Page,
    sync_playwright,
)

from config import settings
from pages import HomePage, LoginPage, SelfServicePage


# --- Core Playwright Fixtures ---


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Session-scoped Playwright instance."""
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """
    Session-scoped browser instance.
    Browser is created once and reused across all tests.
    """
    browser = playwright_instance.chromium.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Function-scoped browser context.
    Each test gets an isolated context (cookies, storage, etc.).
    """
    context_options = {
        "accept_downloads": True,
    }

    # Add video recording if enabled
    if settings.record_video:
        context_options["record_video_dir"] = settings.video_dir

    context = browser.new_context(**context_options)
    context.set_default_timeout(settings.timeout)

    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Function-scoped page instance.
    Each test gets a fresh page.
    """
    page = context.new_page()
    yield page
    page.close()


# --- Page Object Fixtures ---


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """HomePage fixture."""
    return HomePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage fixture."""
    return LoginPage(page)

@pytest.fixture
def self_service_page(page: Page) -> SelfServicePage:
    """Self Service Page fixture."""
    return SelfServicePage(page)

# --- Utility Fixtures ---


@pytest.fixture
def authenticated_page(page: Page) -> Generator[Page, None, None]:
    """
    Page fixture that is already authenticated.
    Useful for tests that require a logged-in state.
    """
    login_page = LoginPage(page)
    login_page.go_to_login_page()
    login_page.login_user()
    # Add any post-login waits or verifications here
    yield page


# --- Pytest Hooks ---


def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login-related")


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers or config."""
    pass  # Add custom logic if needed
