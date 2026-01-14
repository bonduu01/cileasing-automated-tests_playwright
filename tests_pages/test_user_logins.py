"""
Tests for User Login functionality.
"""

import pytest

from config import settings
from pages import HomePage, LoginPage


class TestUserLogins:
    """Test suite for User Login functionalities."""

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_go_to_home_page_with_pom(self, home_page: HomePage) -> None:
        """Verify home page loads correctly with Page Object Model."""
        home_page.go_to_home_page()
        home_page.verify_home_page_loads()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_valid_credentials_with_pom(self, login_page: LoginPage) -> None:
        """Verify successful login with valid credentials using POM."""
        login_page.go_to_login_page()
        login_page.login_user(
            email=settings.test_username,
            password=settings.test_password
        )
        login_page.verify_login_successful_load_companies()
        # Displays the Default Company
        self_service_page = login_page.click_default_company_link()
        self_service_page.wait(5000)

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_wrong_username(self, login_page: LoginPage) -> None:
        """Verify login with explicitly provided credentials."""
        login_page.go_to_login_page()
        login_page.enter_email(settings.test_wrong_username)
        login_page.enter_password(settings.test_password)
        login_page.click_login_button()
        login_page.verify_error_message()
        login_page.verify_error_toast_visible()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_wrong_password(self, login_page: LoginPage) -> None:
        """Verify login with explicitly provided credentials."""
        login_page.go_to_login_page()
        login_page.enter_email(settings.test_username)
        login_page.enter_password(settings.test_wrong_password)
        login_page.click_login_button()
        login_page.verify_error_message()
        login_page.verify_error_toast_visible()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_no_password(self, login_page: LoginPage) -> None:
        """Verify login with explicitly provided credentials."""
        login_page.go_to_login_page()
        login_page.enter_email(settings.test_wrong_username)
        #login_page.enter_password(settings.test_wrong_password)
        login_page.click_login_button()
        login_page.verify_password_blank_error()
        login_page.is_password_blank_error_visible()

    @pytest.mark.smoke
    @pytest.mark.login
    @pytest.mark.regression
    def test_login_with_no_username(self, login_page: LoginPage) -> None:
        """Verify login with explicitly provided credentials."""
        login_page.go_to_login_page()
        # login_page.enter_email(settings.test_wrong_username)
        # login_page.enter_password(settings.test_wrong_password)
        login_page.click_login_button()
        login_page.verify_username_blank_error()
        login_page.is_username_blank_error_visible()
        login_page.is_password_blank_error_visible()
# Function-based tests (alternative style)


# @pytest.mark.smoke
# def test_home_page_loads(home_page: HomePage) -> None:
#     """Verify home page loads correctly."""
#     home_page.go_to_home_page()
#     home_page.verify_home_page_loads()
#
#
# @pytest.mark.smoke
# @pytest.mark.login
# def test_login_page_navigation(home_page: HomePage) -> None:
#     """Verify login functionality."""
#     home_page.go_to_home_page()
#     home_page.verify_home_page_loads()
#     home_page.login_user()
