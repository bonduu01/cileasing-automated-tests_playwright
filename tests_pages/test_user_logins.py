"""
Tests for User Login functionality.
"""

import pytest

from config import settings
from pages import HomePage, LoginPage


class TestUserLogins:
    """Test suite for User Login functionality."""

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



    # @pytest.mark.smoke
    # @pytest.mark.login
    # @pytest.mark.regression
    # def test_login_with_invalid_credentials(self, login_page: LoginPage) -> None:
    #     """Verify login with explicitly provided credentials."""
    #     login_page.go_to_login_page()
    #     login_page.login_user(
    #         email=settings.test_username,
    #         password=settings.test_password,
    #     )
    #
    # @pytest.mark.login
    # def test_login_form_fields_accept_input(self, home_page: HomePage) -> None:
    #     """Verify form fields accept user input."""
    #     home_page.go_to_home_page()
    #     home_page.enter_email("test@example.com")
    #     home_page.verify_element_has_value(
    #         'input[name="email"]',
    #         "test@example.com",
    #     )


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
