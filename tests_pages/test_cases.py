# """
# Additional test cases for the CAndILeasing application.
# """
#
# import pytest
#
# from pages import HomePage, LoginPage
#
#
# class TestHomePageCases:
#     """Test cases for Home Page functionality."""
#
#     @pytest.mark.smoke
#     def test_home_page_title(self, home_page: HomePage) -> None:
#         """Verify home page displays correct title."""
#         home_page.go_to_home_page()
#         home_page.verify_home_page_loads()
#
#     def test_login_form_is_displayed(self, home_page: HomePage) -> None:
#         """Verify login form elements are visible."""
#         home_page.go_to_home_page()
#         home_page.verify_login_form_visible()
#
#     def test_password_field_initially_disabled(self, home_page: HomePage) -> None:
#         """Verify password field is disabled before email entry."""
#         home_page.go_to_home_page()
#         home_page.verify_home_page_loads()
#
#
# class TestLoginPageCases:
#     """Test cases for Login Page functionality."""
#
#     @pytest.mark.login
#     def test_navigate_to_login_page(self, login_page: LoginPage) -> None:
#         """Verify navigation to login page."""
#         login_page.go_to_login_page()
#
#     @pytest.mark.login
#     def test_login_with_default_credentials(self, login_page: LoginPage) -> None:
#         """Verify login with default credentials from .env."""
#         login_page.go_to_login_page()
#         login_page.login_user()
