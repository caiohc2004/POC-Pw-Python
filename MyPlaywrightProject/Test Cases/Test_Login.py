import os
import pytest
from pages.admin_login_page import AdminLoginPage


class TestLoginOrangeHRM:
    """
    OrangeHRM Login tests using Page Object pattern.
    Demonstrates Encapsulation, Inheritance, and Polymorphism.
    """

    @pytest.mark.smoke
    async def test_login_valid_credentials(self, admin_login_page: AdminLoginPage,
                                           admin_credentials: dict):
        """Test login with valid credentials navigates to Dashboard."""
        await admin_login_page.login(admin_credentials["username"],
            admin_credentials["password"]
        )
        await admin_login_page.assert_dashboard_visible()
        if not os.getenv("CI"):
            await admin_login_page.page.pause()  # opens Playwright Inspector; click "Resume" to continue

    @pytest.mark.regression
    async def test_login_invalid_username(self, admin_login_page: AdminLoginPage,
                                          admin_credentials: dict):
        """Test login with wrong username shows error message."""
        await admin_login_page.login("wrongusername", admin_credentials["password"])
        await admin_login_page.assert_invalid_credentials_visible()
        if not os.getenv("CI"):
            await admin_login_page.page.pause()

    @pytest.mark.regression
    async def test_login_invalid_password(self, admin_login_page: AdminLoginPage,
                                          admin_credentials: dict):
        """Test login with wrong password shows error message."""
        await admin_login_page.login(admin_credentials["username"], "wrongpassword")
        await admin_login_page.assert_invalid_credentials_visible()

    @pytest.mark.regression
    async def test_login_message_empty_fields(self, admin_login_page: AdminLoginPage):
        """Test that empty fields show 'Required' validation messages."""
        await admin_login_page.click_element("button[type='submit']")
        await admin_login_page.assert_required_fields_visible()
        
        