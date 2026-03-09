from pages.login_base_page import LoginBasePage


class ClientLoginPage(LoginBasePage):
    """
    Client Login Page demonstrating:
    - Polymorphism: Implements login() differently than AdminLoginPage
    - Encapsulation: Different private selectors than admin login
    - Inheritance: Shares common behavior from LoginBasePage
    """
    
    # Encapsulation: Private selectors specific to client login
    _CLIENT_EMAIL_INPUT = "#client-email"
    _CLIENT_PASSWORD_INPUT = "#client-password"
    _CLIENT_REMEMBER_ME_CHECKBOX = "#remember-me"
    _CLIENT_LOGIN_BUTTON = "button[type='submit'][data-test='client-login']"
    _CLIENT_ERROR_MESSAGE = ".client-error-message"
    _CLIENT_PROFILE_ICON = ".client-profile-icon"
    
    async def navigate(self) -> None:
        """Navigate to client login page."""
        await self._page.goto(f"{self._base_url}/login")
        await self.wait_for_page_load()
    
    async def login(self, username: str, password: str, remember_me: bool = False) -> None:
        """
        Polymorphism: Client-specific login implementation.
        Client login uses email and password, with optional remember-me.
        Different signature and behavior than AdminLoginPage.login()
        """
        await self.fill_input(self._CLIENT_EMAIL_INPUT, username)
        await self.fill_input(self._CLIENT_PASSWORD_INPUT, password)
        
        if remember_me:
            await self.click_element(self._CLIENT_REMEMBER_ME_CHECKBOX)
        
        await self.click_element(self._CLIENT_LOGIN_BUTTON)
        await self.wait_for_page_load()
    
    async def get_error_message(self) -> str:
        """Get client-specific error message."""
        if await self.is_visible(self._CLIENT_ERROR_MESSAGE):
            return await self.get_text(self._CLIENT_ERROR_MESSAGE)
        return ""
    
    async def assert_profile_icon_visible(self) -> None:
        """Assertion: Validate client profile icon is visible after login."""
        await self.assert_element_visible(self._CLIENT_PROFILE_ICON)
    
    async def assert_on_client_login_page(self) -> None:
        """Assertion: Validate we're on the client login page."""
        await self.assert_url_contains("/login")
        await self.assert_element_visible(self._CLIENT_EMAIL_INPUT)
