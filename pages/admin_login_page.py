import os
from pathlib import Path
from dotenv import load_dotenv
from pages.login_base_page import LoginBasePage

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)


class AdminLoginPage(LoginBasePage):
    """
    OrangeHRM Admin Login Page demonstrating:
    - Polymorphism: Implements login() differently than ClientLoginPage
    - Encapsulation: Selectors are private and hidden from tests
    - Inheritance: Inherits common behavior from LoginBasePage
    """

    # Encapsulation: Private selectors for OrangeHRM login page
    _USERNAME_INPUT = "input[name='username']"
    _PASSWORD_INPUT = "input[name='password']"
    _LOGIN_BUTTON = "button[type='submit']"
    _INVALID_CREDENTIALS_MSG = "text=Invalid credentials"
    _REQUIRED_MSG = "text=Required"
    _DASHBOARD_HEADING = "h6:has-text('Dashboard')"

    async def navigate(self) -> None:
        """Navigate to OrangeHRM login page."""
        await self._page.goto(f"{self._base_url}/web/index.php/auth/login")
        await self.wait_for_page_load()

    @staticmethod
    def get_credentials_from_env() -> dict:
        """
        Load admin credentials from environment variables.
        Returns a dictionary with username and password.
        """
        username = os.getenv('ORANGE_USERNAME')
        password = os.getenv('ORANGE_PASSWORD')
        return {
            'username': username,
            'password': password
        }

    async def login(self, username: str, password: str) -> None:
        """
        Polymorphism: OrangeHRM admin login implementation.
        Fills username, password and clicks login.
        """
        await self.fill_input(self._USERNAME_INPUT, username)
        await self.fill_input(self._PASSWORD_INPUT, password)
        await self.click_element(self._LOGIN_BUTTON)
        await self.wait_for_page_load()

    async def get_error_message(self) -> str:
        """Get login error message (Invalid credentials)."""
        if await self.is_visible(self._INVALID_CREDENTIALS_MSG):
            return await self.get_text(self._INVALID_CREDENTIALS_MSG)
        return ""

    async def assert_dashboard_visible(self) -> None:
        """Assertion: Validate Dashboard heading is visible after login."""
        await self.assert_element_visible(self._DASHBOARD_HEADING)

    async def assert_invalid_credentials_visible(self) -> None:
        """Assertion: Validate 'Invalid credentials' message is visible."""
        await self.assert_element_visible(self._INVALID_CREDENTIALS_MSG)

    async def assert_required_fields_visible(self) -> None:
        """Assertion: Validate 'Required' messages are visible for empty fields."""
        elements = self._page.locator(self._REQUIRED_MSG)
        count = await elements.count()
        assert count >= 2, f"Expected at least 2 'Required' messages, found {count}"

    async def assert_on_login_page(self) -> None:
        """Assertion: Validate we're on the OrangeHRM login page."""
        await self.assert_url_contains("/auth/login")
        await self.assert_element_visible(self._LOGIN_BUTTON)
