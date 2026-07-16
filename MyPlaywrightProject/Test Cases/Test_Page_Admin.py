import pytest
from pages.admin_login_page import AdminLoginPage
from pages.system_users_page import SystemUsersPage


class TestSystemUsers:
    """
    OrangeHRM System Users Page tests using Page Object pattern.
    Tests admin user management functionality.
    """

    @pytest.mark.smoke
    async def test_navigate_to_system_users_page(
        self,
        admin_login_page: AdminLoginPage,
        admin_credentials: dict,
        base_url: str
    ):
        """Test navigation to System Users page after login."""
        # Login first
        await admin_login_page.login(admin_credentials["username"],
                                     admin_credentials["password"])
        await admin_login_page.assert_dashboard_visible()
        
        # Create SystemUsersPage with same page instance
        system_users_page = SystemUsersPage(admin_login_page.page, base_url)
        await system_users_page.navigate()
        await system_users_page.assert_on_system_users_page()

    @pytest.mark.smoke
    async def test_search_user_by_username(
        self,
        admin_login_page: AdminLoginPage,
        admin_credentials: dict,
        base_url: str
    ):
        """Test searching for a user by username."""
        # Login
        await admin_login_page.login(admin_credentials["username"],
                                     admin_credentials["password"])
        
        # Navigate to System Users
        system_users_page = SystemUsersPage(admin_login_page.page, base_url)
        await system_users_page.navigate()
        
        # Search for Admin user
        await system_users_page.search_by_username("Admin")
        await system_users_page.assert_specific_user_visible("Admin")

    @pytest.mark.regression
    async def test_search_nonexistent_user(
        self,
        admin_login_page: AdminLoginPage,
        admin_credentials: dict,
        base_url: str
    ):
        """Test searching for non-existent user shows no records."""
        await admin_login_page.login(admin_credentials["username"],
                                     admin_credentials["password"])
        
        system_users_page = SystemUsersPage(admin_login_page.page, base_url)
        await system_users_page.navigate()
        await system_users_page.search_by_username("NonExistentUser12345")
        await system_users_page.assert_no_records_found()

    @pytest.mark.regression
    async def test_add_button_visible(
        self,
        admin_login_page: AdminLoginPage,
        admin_credentials: dict,
        base_url: str
    ):
        """Test that Add button is visible on System Users page."""
        await admin_login_page.login(admin_credentials["username"],
                                     admin_credentials["password"])
        
        system_users_page = SystemUsersPage(admin_login_page.page, base_url)
        await system_users_page.navigate()
        await system_users_page.assert_add_button_visible()


        