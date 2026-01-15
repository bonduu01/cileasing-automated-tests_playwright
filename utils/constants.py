"""
Page selectors and UI constants.
Credentials and URLs should be loaded from .env via config/settings.py
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class HomePageSelectors:
    """Selectors for the Home Page."""
    TITLE: str = "CAndILeasing"


@dataclass(frozen=True)
class LoginPageSelectors:
    """Selectors for the Login Page."""
    EMAIL_INPUT: str = 'input[name="email"]'
    PASSWORD_INPUT: str = 'input[name="password"]'
    SUBMIT_BUTTON: str = 'button[type="submit"][buttontype="primary"]'
    PASSWORD_DISABLED: str = "input[name='password'][type='password']"
    # DEFAULT_COMPANY: str = 'div.space-y-4 div.uppercase:text-is("DEFAULT")'
    DEFAULT_COMPANY: str = "div.uppercase:has-text('DEFAULT')"
    FLOUR_MILLS_COMPANY: str = 'div.space-y-4 div.uppercase:text-is("FLOUR MILLS NIGERIA LIMITED GOLDEN NOODLES & PASTA IGANMU")'
    ERROR_TOAST: str = 'div[role="alert"]'
    PASSWORD_BLANK_ERROR = 'p.text-xs.mt-1:has-text("Password cannot be blank")'
    VALIDATION_ERROR = 'p.text-xs.mt-1'
    ERROR_PASSWORD_BLANK = "Password cannot be blank"
    ERROR_USERNAME_BLANK = "Email cannot be blank"
    ERROR_INVALID_CREDENTIALS = "Invalid username or password"
    DEFAULT_LINK: str = 'text="DEFAULT"'


@dataclass(frozen=True)
class SelfServicePageSelectors:
    """Selectors for the Self-Service Page."""
    PERSONAL_NAME: str = "span.text-dark0b.font-\\[400\\].text-\\[14px\\]"
    MM_PROFILE: str = "span.ant-avatar-string:has-text('MM')"
    LOGOUT_LINK: str = "p.text-danger:has-text('Logout')"
    EDIT_LINK: str = "button:has-text('Edit')"
    EDIT_SUBMIT_BUTTON: str = "button:has-text('Submit')"
    ADD_BANK_DETAIL_BUTTON: str = "button:has-text('Bank Details')"


@dataclass(frozen=True)
class EditSelfServicePageSelectors:
    """Selectors for the Edit Personnel Self-Service Page."""
    OTHER_NAME: str = "input[name='otherName']"
    JOB_TITLE: str = 'input[name="jobTitle"]'
    EDIT_SUBMIT_BUTTON: str = "button:has-text('Submit')"



# Create singleton instances
HOME_PAGE = HomePageSelectors()
LOGIN_PAGE = LoginPageSelectors()
SELF_SERVICE_PAGE = SelfServicePageSelectors()
EDIT_SELF_SERVICE_PAGE = EditSelfServicePageSelectors()
