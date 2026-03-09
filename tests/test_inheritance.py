import pytest
from pages.admin_login_page import AdminLoginPage
from pages.client_login_page import ClientLoginPage
from pages.home_page import HomePage
from pages.dashboard_page import DashboardPage


class TestInheritance:
    """
    Tests demonstrating INHERITANCE:
    - All pages inherit from BasePage
    - All login pages inherit from LoginBasePage
    - Common methods like wait_for_page_load() are inherited
    """
    
    @pytest.mark.smoke
    async def test_inherited_wait_for_page_load(self, home_page: HomePage):
        """
        Demonstrates INHERITANCE:
        - wait_for_page_load() is inherited from BasePage
        - All page objects can use it without reimplementing
        """
        await home_page.navigate()
        
        # This method is inherited from BasePage
        await home_page.wait_for_page_load()
        
        # All pages have this method because they inherit from BasePage
        title = await home_page.get_page_title()
        assert len(title) > 0
    
    @pytest.mark.regression
    async def test_inherited_assertion_methods(self, admin_login_page: AdminLoginPage):
        """
        Demonstrates INHERITANCE:
        - Assertion methods are inherited from BasePage
        - All pages can use assert_url_contains, assert_element_visible, etc.
        """
        await admin_login_page.navigate()
        
        # These assertion methods are inherited from BasePage
        await admin_login_page.assert_url_contains("/admin/login")
        await admin_login_page.assert_element_visible("#admin-username")
    
    @pytest.mark.regression
    async def test_inherited_login_assertions(self, client_login_page: ClientLoginPage,
                                              client_credentials: dict):
        """
        Demonstrates INHERITANCE:
        - Login pages inherit from LoginBasePage
        - assert_login_successful() is inherited
        """
        await client_login_page.login(
            client_credentials["username"],
            client_credentials["password"]
        )
        
        # This method is inherited from LoginBasePage
        await client_login_page.assert_login_successful()
    
    @pytest.mark.smoke
    async def test_all_pages_inherit_common_methods(self, home_page: HomePage,
                                                     dashboard_page: DashboardPage):
        """
        Demonstrates INHERITANCE:
        - Multiple page objects share common inherited methods
        - Shows the power of inheritance for code reuse
        """
        # Both pages inherit from BasePage and have the same methods
        await home_page.navigate()
        home_url = await home_page.get_current_url()
        assert "example.com" in home_url
        
        await dashboard_page.navigate()
        dashboard_url = await dashboard_page.get_current_url()
        assert "dashboard" in dashboard_url
        
        # Both can use inherited reload_page()
        await dashboard_page.reload_page()
        
        # Both can use inherited assertion methods
        await dashboard_page.assert_url_contains("/dashboard")
