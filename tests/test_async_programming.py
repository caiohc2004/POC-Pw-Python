import pytest
import asyncio
from pages.home_page import HomePage
from pages.dashboard_page import DashboardPage
from playwright.async_api import Page


class TestAsyncProgramming:
    """
    Tests demonstrating ASYNCHRONOUS PROGRAMMING:
    - All Playwright operations are async
    - Using async/await properly
    - Handling async operations in tests
    """
    
    @pytest.mark.smoke
    async def test_async_navigation(self, home_page: HomePage):
        """
        Demonstrates async navigation.
        navigate() is async and must be awaited.
        """
        # All page operations are async
        await home_page.navigate()
        await home_page.wait_for_page_load()
        
        # Getting data is also async
        url = await home_page.get_current_url()
        assert "example.com" in url
    
    @pytest.mark.regression
    async def test_async_interactions(self, home_page: HomePage):
        """
        Demonstrates async user interactions.
        All clicks, fills, and actions are async.
        """
        await home_page.navigate()
        
        # Async click operation
        await home_page.open_menu()
        
        # Async search operation
        await home_page.search_product("Laptop")
        
        # Async cart operation
        await home_page.add_product_to_cart("Laptop")
        
        # Async data retrieval
        cart_count = await home_page.get_cart_item_count()
        assert cart_count == 1
    
    @pytest.mark.regression
    async def test_async_wait_operations(self, dashboard_page: DashboardPage):
        """
        Demonstrates async wait operations.
        All waits are asynchronous.
        """
        await dashboard_page.navigate()
        
        # Async wait for page load
        await dashboard_page.wait_for_page_load()
        
        # Async wait for specific element
        await dashboard_page.wait_for_selector(".dashboard-title")
        
        # Async wait for timeout
        await dashboard_page.wait_for_timeout(1000)
    
    @pytest.mark.regression
    async def test_async_assertions(self, home_page: HomePage):
        """
        Demonstrates async assertions.
        Playwright assertions are async and must be awaited.
        """
        await home_page.navigate()
        
        # All assertions are async
        await home_page.assert_url_contains("example.com")
        await home_page.assert_element_visible(".cart-icon")
        await home_page.assert_element_count(".product-card", 12)
    
    @pytest.mark.smoke
    async def test_async_data_retrieval(self, dashboard_page: DashboardPage):
        """
        Demonstrates async data retrieval.
        Getting text, attributes, etc. are all async operations.
        """
        await dashboard_page.navigate()
        await dashboard_page.wait_for_dashboard_load()
        
        # Async get text
        title = await dashboard_page.get_page_title()
        assert "Dashboard" in title
        
        # Async get metric value
        metric_value = await dashboard_page.get_metric_value("Total Sales")
        assert len(metric_value) > 0
        
        # Async get notification count
        count = await dashboard_page.get_notification_count()
        assert count >= 0
    
    @pytest.mark.regression
    async def test_async_multiple_operations(self, home_page: HomePage):
        """
        Demonstrates chaining multiple async operations.
        Shows proper async/await flow.
        """
        # All operations are async and executed sequentially
        await home_page.navigate()
        await home_page.wait_for_page_load()
        await home_page.open_menu()
        await home_page.select_menu_item("Electronics")
        await home_page.filter_by_category("Laptops")
        await home_page.add_product_to_cart("Gaming Laptop")
        
        # Verify final state
        count = await home_page.get_cart_item_count()
        assert count == 1
    
    @pytest.mark.regression
    async def test_async_error_handling(self, home_page: HomePage):
        """
        Demonstrates async error handling.
        Shows how to handle async exceptions.
        """
        await home_page.navigate()
        
        try:
            # This might timeout if element doesn't exist
            await home_page.wait_for_selector(".non-existent-element", state="visible")
            assert False, "Should have raised timeout error"
        except Exception as e:
            # Properly catch async exception
            assert "Timeout" in str(e) or "waiting" in str(e)
    
    @pytest.mark.smoke
    async def test_playwright_async_context(self, page: Page):
        """
        Demonstrates Playwright's async context.
        Shows direct use of async Playwright API.
        """
        # All Playwright page methods are async
        await page.goto("https://example.com")
        
        # Async locator operations
        title_element = page.locator("h1")
        title_text = await title_element.text_content()
        assert len(title_text) > 0
        
        # Async expect assertions
        from playwright.async_api import expect
        await expect(page).to_have_url(lambda url: "example.com" in url)
