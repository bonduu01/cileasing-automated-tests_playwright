from playwright.sync_api import sync_playwright, expect

from utils.constants import BASE_URL


def test_logins_without_poms():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        try:
            page.goto(BASE_URL, wait_until="domcontentloaded")
            password_input = page.locator('input[name="password"]')
            # Wait for the input to appear in the DOM
            password_input.wait_for(state="attached", timeout=10000)
            # Then assert it's disabled
            expect(password_input).to_be_disabled()
        finally:
            page.close()
            context.close()
            browser.close()
