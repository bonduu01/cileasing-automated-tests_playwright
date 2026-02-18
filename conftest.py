from typing import Generator
import logging
import sys
import os
from datetime import datetime

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

# Create necessary directories
os.makedirs("screenshots", exist_ok=True)


def setup_logging():
    """Configure console logging for all tests."""
    # Configure root logger with console output only
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(name)-30s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Reduce noise from playwright internal logs
    logging.getLogger('playwright').setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    logger.info(f"{'=' * 80}")
    logger.info(f"🚀 TEST RUN STARTED")
    logger.info(f"   📸 Screenshots: screenshots/")
    logger.info(f"   🎥 Videos: {settings.video_dir if settings.record_video else 'disabled'}")
    logger.info(f"   🌐 Headless: {settings.headless}")
    logger.info(f"   ⏱️  Timeout: {settings.timeout}ms")
    logger.info(f"   📏 Default Viewport: {os.getenv('VIEWPORT_WIDTH', 1920)}x{os.getenv('VIEWPORT_HEIGHT', 1080)}")
    logger.info(f"{'=' * 80}\n")


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Auto-configure logging for all tests."""
    setup_logging()
    yield

    logger = logging.getLogger(__name__)
    logger.info(f"\n{'=' * 80}")
    logger.info(f"✅ TEST RUN COMPLETED")
    logger.info(f"{'=' * 80}")


# --- Core Playwright Fixtures ---


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    """Session-scoped Playwright instance."""
    logger = logging.getLogger(__name__)
    logger.info("🎭 Starting Playwright instance")

    with sync_playwright() as playwright:
        yield playwright

    logger.info("🎭 Closing Playwright instance")


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Generator[Browser, None, None]:
    """
    Session-scoped browser instance.
    Browser is created once and reused across all tests.
    """
    logger = logging.getLogger(__name__)
    logger.info(f"🌐 Launching browser (headless={settings.headless}, slow_mo={settings.slow_mo})")

    browser = playwright_instance.chromium.launch(
        headless=settings.headless,
        slow_mo=settings.slow_mo,
        args=['--start-maximized']
    )

    logger.info(f"   ✅ Browser launched: {browser.browser_type.name}")

    yield browser

    logger.info("🌐 Closing browser")
    browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    """
    Function-scoped browser context.
    Each test gets an isolated context (cookies, storage, etc.).
    """
    logger = logging.getLogger(__name__)
    logger.info("📋 Creating new browser context")

    # Get viewport settings from environment variables (for CI/CD)
    viewport_width = int(os.getenv("VIEWPORT_WIDTH", 1920))
    viewport_height = int(os.getenv("VIEWPORT_HEIGHT", 1080))

    logger.info(f"   📏 Setting viewport to: {viewport_width}x{viewport_height}")

    context_options = {
        "accept_downloads": True,
        "viewport": {
            "width": viewport_width,
            "height": viewport_height,
        }
    }

    # Add video recording if enabled
    if settings.record_video:
        context_options["record_video_dir"] = settings.video_dir
        logger.info(f"   🎥 Video recording enabled: {settings.video_dir}")

    context = browser.new_context(**context_options)
    context.set_default_timeout(settings.timeout)

    logger.info(f"   ✅ Context created (timeout={settings.timeout}ms)")

    yield context

    logger.info("📋 Closing browser context")
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """
    Function-scoped page instance.
    Each test gets a fresh page.
    """
    logger = logging.getLogger(__name__)
    logger.info("📄 Creating new page")

    page = context.new_page()

    # Verify viewport is set correctly
    viewport = page.viewport_size
    logger.info(f"   📏 Verified viewport: {viewport['width']}x{viewport['height']}")
    logger.info(f"   📍 Initial URL: {page.url}")

    yield page

    logger.info(f"📄 Closing page (final URL: {page.url})")
    page.close()


# --- Page Object Fixtures ---


@pytest.fixture
def home_page(page: Page) -> HomePage:
    """HomePage fixture."""
    logger = logging.getLogger(__name__)
    logger.info("🏗️ Creating HomePage fixture")
    return HomePage(page)


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """LoginPage fixture."""
    logger = logging.getLogger(__name__)
    logger.info("🏗️ Creating LoginPage fixture")
    return LoginPage(page)


@pytest.fixture
def self_service_page(authenticated_page: Page) -> SelfServicePage:
    """Self Service Page fixture."""
    logger = logging.getLogger(__name__)
    logger.info("🏗️ Creating SelfServicePage fixture")
    return SelfServicePage(authenticated_page)


# --- Utility Fixtures ---


@pytest.fixture
def authenticated_page(page: Page) -> Generator[Page, None, None]:
    """
    Page fixture that is already authenticated.
    Useful for tests that require a logged-in state.
    """
    logger = logging.getLogger(__name__)
    logger.info("\n" + "=" * 60)
    logger.info("🔐 AUTHENTICATION SETUP")
    logger.info("=" * 60)

    try:
        login_page = LoginPage(page)

        logger.info("📋 Step 1: Navigate to login page")
        login_page.go_to_login_page()

        logger.info("📋 Step 2: Perform login")
        login_page.login_user(
            email=settings.test_username,
            password=settings.test_password
        )

        logger.info("📋 Step 3: Verify login successful")
        login_page.verify_login_successful_load_companies()

        logger.info("📋 Step 4: Click default company link")
        self_service_page = login_page.click_default_company_link()

        logger.info("📋 Step 5: Verify self-service page loads")
        self_service_page.verify_self_service_page_loads()

        logger.info("✅ Authentication successful")
        logger.info("=" * 60 + "\n")

        yield page

        # Teardown (logout)
        logger.info("\n" + "=" * 60)
        logger.info("🔐 AUTHENTICATION TEARDOWN")
        logger.info("=" * 60)
        logger.info("📋 Logging out...")

        self_service_page.click_to_logout()

        logger.info("✅ Logout successful")
        logger.info("=" * 60 + "\n")

    except Exception as e:
        logger.error(f"❌ Authentication setup failed: {e}")

        # Take screenshot on failure
        try:
            timestamp = int(datetime.now().timestamp())
            screenshot_path = f"screenshots/auth_error_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            logger.error(f"   📸 Error screenshot: {screenshot_path}")
        except:
            pass

        raise


# --- Pytest Hooks ---


def pytest_configure(config):
    """Configure custom pytest markers."""
    logger = logging.getLogger(__name__)
    logger.info("⚙️ Configuring pytest markers")

    config.addinivalue_line("markers", "smoke: mark test as smoke test")
    config.addinivalue_line("markers", "regression: mark test as regression test")
    config.addinivalue_line("markers", "login: mark test as login-related")


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on markers or config."""
    logger = logging.getLogger(__name__)
    logger.info(f"📊 Collected {len(items)} test(s)")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to log test results."""
    outcome = yield
    report = outcome.get_result()

    logger = logging.getLogger(__name__)

    if report.when == "call":
        if report.passed:
            logger.info(f"✅ TEST PASSED: {item.nodeid}")
        elif report.failed:
            logger.error(f"❌ TEST FAILED: {item.nodeid}")
            logger.error(f"   Failure reason: {report.longreprtext[:200]}...")
        elif report.skipped:
            logger.warning(f"⏭️ TEST SKIPPED: {item.nodeid}")


@pytest.fixture(autouse=True)
def log_test_info(request):
    """Automatically log test start and end for each test."""
    logger = logging.getLogger(__name__)
    test_name = request.node.name

    logger.info(f"\n{'#' * 80}")
    logger.info(f"🧪 STARTING TEST: {test_name}")
    logger.info(f"{'#' * 80}\n")

    yield

    logger.info(f"\n{'#' * 80}")
    logger.info(f"🏁 FINISHED TEST: {test_name}")
    logger.info(f"{'#' * 80}\n")