import pytest
from pages.admin_login_page import AdminLoginPage
from pages.client_login_page import ClientLoginPage
from pages.home_page import HomePage
from playwright.async_api import Page


class TestFixtures:
    """
    Tests demonstrating FIXTURES and DEPENDENCY INJECTION:
    - Playwright auto-injects page, context, browser
    - Custom fixtures inject page objects
    - Fixtures for logged-in states
    """
    
    @pytest.mark.smoke
    async def test_page_fixture_injection(self, page: Page):
        """
        Demonstrates built-in Playwright fixture injection.
        The 'page' object is automatically injected by Playwright.
        """
        # page is injected automatically - no manual instantiation needed
        await page.goto("https://example.com")
        title = await page.title()
        assert len(title) > 0
    
    @pytest.mark.smoke
    async def test_custom_page_object_fixture(self, home_page: HomePage):
        """
        Demonstrates custom fixture injection.
        home_page is injected via our custom fixture in conftest.py
        """
        # home_page is ready to use - fixture handled initialization
        await home_page.navigate()
        await home_page.assert_url_contains("example.com")
    
    @pytest.mark.regression
    async def test_multiple_page_fixtures(self, admin_login_page: AdminLoginPage,
                                          client_login_page: ClientLoginPage):
        """
        Demonstrates multiple fixture injection.
        Both page objects are injected and ready to use.
        """
        # Both pages are initialized via fixtures
        await admin_login_page.assert_on_admin_login_page()
        await client_login_page.navigate()
        await client_login_page.assert_on_client_login_page()
    
    @pytest.mark.smoke
    async def test_credentials_fixture(self, admin_credentials: dict, client_credentials: dict):
        """
        Demonstrates data fixture injection.
        Credentials are loaded from fixtures/env variables.
        """
        # Credentials are injected as dictionaries
        assert "username" in admin_credentials
        assert "password" in admin_credentials
        assert admin_credentials["username"] == "admin@example.com"
        
        assert "username" in client_credentials
        assert "password" in client_credentials
    
    @pytest.mark.regression
    async def test_logged_in_admin_fixture(self, logged_in_admin: AdminLoginPage):
        """
        Demonstrates state fixture injection.
        The fixture handles login, test starts with user already logged in.
        """
        # User is already logged in via fixture
        await logged_in_admin.assert_login_successful()
        await logged_in_admin.assert_url_contains("/admin/dashboard")
    
    @pytest.mark.regression
    async def test_logged_in_client_fixture(self, logged_in_client: ClientLoginPage):
        """
        Demonstrates state fixture injection for client.
        Test receives a page with client already authenticated.
        """
        # Client is already logged in via fixture
        await logged_in_client.assert_login_successful()
        await logged_in_client.assert_profile_icon_visible()
    
    @pytest.mark.smoke
    async def test_base_url_fixture(self, base_url: str, home_page: HomePage):
        """
        Demonstrates configuration fixture injection.
        base_url is loaded from environment/fixture.
        """
        # base_url is injected from fixture
        assert "example.com" in base_url
        
        # Page objects use the injected base_url
        await home_page.navigate()
        current_url = await home_page.get_current_url()
        assert base_url in current_url
    
    @pytest.mark.regression
    async def test_fixture_composition(self, logged_in_admin: AdminLoginPage,
                                       home_page: HomePage):
        """
        Demonstrates fixture composition.
        logged_in_admin uses admin_login_page + admin_credentials fixtures.
        """
        # Start with logged-in state from fixture
        await logged_in_admin.assert_login_successful()
        
        # Navigate to home using different page object
        await home_page.navigate()
        await home_page.assert_url_contains("/")
        
        # User should still be authenticated
        await home_page.assert_element_visible(".user-menu")
