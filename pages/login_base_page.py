from abc import abstractmethod
from pages.base_page import BasePage


class LoginBasePage(BasePage):
    """
    Abstract base class for login pages demonstrating:
    - Inheritance: Inherits from BasePage
    - Abstraction: Defines common login interface
    - Polymorphism: Child classes implement login() differently
    """
    
    @abstractmethod
    async def login(self, username: str, password: str) -> None:
        """
        Abstract login method - each login page implements this differently.
        This demonstrates Polymorphism: same method name, different implementations.
        """
        pass
    
    @abstractmethod
    async def get_error_message(self) -> str:
        """Abstract method to get login error messages."""
        pass
    
    async def assert_login_successful(self) -> None:
        """Common assertion for successful login."""
        await self.wait_for_page_load()
        current_url = await self.get_current_url()
        assert "login" not in current_url.lower(), "Still on login page after login attempt"
    
    async def assert_login_failed(self) -> None:
        """Common assertion for failed login."""
        error_message = await self.get_error_message()
        assert len(error_message) > 0, "No error message displayed for failed login"
