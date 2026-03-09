import pytest
from pages.admin_login_page import AdminLoginPage
from pages.client_login_page import ClientLoginPage


class TestLoginPolymorphism:
    """
    Tests demonstrating POLYMORPHISM:
    - Same method name (login) behaves differently for Admin and Client
    - Both inherit from LoginBasePage but implement login() differently
    """
    
    @pytest.mark.smoke
    @pytest.mark.admin
    async def test_admin_login_requires_domain(self, admin_login_page: AdminLoginPage, 
                                               admin_credentials: dict):
        """
        Test admin login - demonstrates polymorphism.
        Admin login() requires username, password, AND domain.
        """
        await admin_login_page.assert_on_admin_login_page()
        
        await admin_login_page.login(
            admin_credentials["username"],
            admin_credentials["password"],
            domain="admin"
        )
        
        await admin_login_page.assert_login_successful()
        await admin_login_page.assert_url_contains("/admin/dashboard")
    
    @pytest.mark.smoke
    @pytest.mark.client
    async def test_client_login_with_remember_me(self, client_login_page: ClientLoginPage,
                                                  client_credentials: dict):
        """
        Test client login - demonstrates polymorphism.
        Client login() uses email, password, and optional remember_me flag.
        DIFFERENT signature and behavior than admin login.
        """
        await client_login_page.assert_on_client_login_page()
        
        await client_login_page.login(
            client_credentials["username"],
            client_credentials["password"],
            remember_me=True
        )
        
        await client_login_page.assert_login_successful()
        await client_login_page.assert_profile_icon_visible()
    
    @pytest.mark.regression
    async def test_polymorphic_login_behavior(self, admin_login_page: AdminLoginPage,
                                              client_login_page: ClientLoginPage,
                                              admin_credentials: dict,
                                              client_credentials: dict):
        """
        Demonstrates polymorphism: same method name, different behaviors.
        Both pages have login(), but they work completely differently.
        """
        # Admin login - requires domain
        await admin_login_page.login(
            admin_credentials["username"],
            admin_credentials["password"],
            domain="admin"
        )
        await admin_login_page.assert_login_successful()
        
        # Navigate to client login in same test
        await client_login_page.navigate()
        
        # Client login - no domain, but has remember_me
        await client_login_page.login(
            client_credentials["username"],
            client_credentials["password"],
            remember_me=False
        )
        await client_login_page.assert_login_successful()
