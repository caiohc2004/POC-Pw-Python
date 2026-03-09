import os
from pathlib import Path
from dotenv import load_dotenv
from pages.login_base_page import LoginBasePage

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)


class AdminLoginPage(LoginBasePage):
    """
    Admin Login Page demonstrating:
    - Polymorphism: Implements login() differently than ClientLoginPage
    - Encapsulation: Selectors are private and hidden from tests
    - Inheritance: Inherits common behavior from LoginBasePage
    """
    
    # Encapsulation: Private selectors hidden from outside
    _ADMIN_USERNAME_INPUT = "#admin-username"
    _ADMIN_PASSWORD_INPUT = "#admin-password"
    _ADMIN_DOMAIN_INPUT = "#admin-domain"
    _ADMIN_LOGIN_BUTTON = "button[type='submit'][data-test='admin-login']"
    _ADMIN_ERROR_MESSAGE = ".admin-error-message"
    _ADMIN_WELCOME_MESSAGE = ".admin-welcome"
    
    async def navigate(self) -> None:
        """Navigate to admin login page."""
        await self._page.goto(f"{self._base_url}/admin/login")
        await self.wait_for_page_load()
    
    @staticmethod
    def get_credentials_from_env() -> dict:
        """
        Load admin credentials from environment variables.
        Returns a dictionary with username and password.
        """
        username = os.getenv('ADMIN_USERNAME')
        password = os.getenv('ADMIN_PASSWORD')
        return {
            'username': username,
            'password': password
        }
    
    async def login(self, username: str, password: str, domain: str = "admin") -> None:
        """
        Polymorphism: Admin-specific login implementation.
        Admin login requires username, password, AND domain.
        """
        await self.fill_input(self._ADMIN_USERNAME_INPUT, username)
        await self.fill_input(self._ADMIN_PASSWORD_INPUT, password)
        await self.fill_input(self._ADMIN_DOMAIN_INPUT, domain)
        await self.click_element(self._ADMIN_LOGIN_BUTTON)
        await self.wait_for_page_load()
    
    async def get_error_message(self) -> str:
        """Get admin-specific error message."""
        if await self.is_visible(self._ADMIN_ERROR_MESSAGE):
            return await self.get_text(self._ADMIN_ERROR_MESSAGE)
        return ""
    
    async def assert_welcome_message_visible(self) -> None:
        """Assertion: Validate admin welcome message is visible."""
        await self.assert_element_visible(self._ADMIN_WELCOME_MESSAGE)
    
    async def assert_on_admin_login_page(self) -> None:
        """Assertion: Validate we're on the admin login page."""
        await self.assert_url_contains("/admin/login")
        await self.assert_element_visible(self._ADMIN_DOMAIN_INPUT)
