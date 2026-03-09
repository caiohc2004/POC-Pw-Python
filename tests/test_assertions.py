import pytest
from pages.home_page import HomePage
from pages.dashboard_page import DashboardPage
from pages.checkout_page import CheckoutPage


class TestAssertions:
    """
    Tests demonstrating ASSERTIONS:
    - toHaveURL() via assert_url_contains()
    - toBeVisible() via assert_element_visible()
    - toHaveText() via assert_element_has_text()
    - toContainText() via assert_element_contains_text()
    - toHaveAttribute() via assert_element_has_attribute()
    - toHaveCount() via assert_element_count()
    """
    
    @pytest.mark.smoke
    async def test_url_assertions(self, home_page: HomePage):
        """Demonstrates URL assertions (toHaveURL)."""
        await home_page.navigate()
        
        # Assert URL contains expected path
        await home_page.assert_url_contains("example.com")
        
        # Navigate to different section
        await home_page.search_product("Phone")
        await home_page.assert_url_contains("search")
    
    @pytest.mark.smoke
    async def test_visibility_assertions(self, home_page: HomePage):
        """Demonstrates visibility assertions (toBeVisible, toBeHidden)."""
        await home_page.navigate()
        
        # Assert element is visible
        await home_page.assert_element_visible(".cart-icon")
        
        # Assert menu is initially hidden
        await home_page.assert_menu_hidden()
        
        # Open menu and assert it's visible
        await home_page.open_menu()
        await home_page.assert_menu_visible()
    
    @pytest.mark.regression
    async def test_text_assertions(self, dashboard_page: DashboardPage):
        """Demonstrates text assertions (toHaveText, toContainText)."""
        await dashboard_page.navigate()
        await dashboard_page.wait_for_dashboard_load()
        
        # Assert element has exact text
        await dashboard_page.assert_element_has_text(".dashboard-title", "Dashboard")
        
        # Assert element contains text (partial match)
        await dashboard_page.assert_element_contains_text(".dashboard-title", "Dash")
    
    @pytest.mark.regression
    async def test_attribute_assertions(self, checkout_page: CheckoutPage):
        """Demonstrates attribute assertions (toHaveAttribute)."""
        await checkout_page.navigate()
        
        # Select shipping method
        await checkout_page.select_shipping_method("express")
        
        # Assert radio button has checked attribute
        await checkout_page.assert_shipping_method_selected("express")
        
        # Assert input has specific attribute
        await checkout_page.assert_element_has_attribute(
            "#first-name",
            "type",
            "text"
        )
    
    @pytest.mark.regression
    async def test_count_assertions(self, home_page: HomePage):
        """Demonstrates count assertions (toHaveCount)."""
        await home_page.navigate()
        
        # Assert number of product cards
        await home_page.assert_element_count(".product-card", 12)
        
        # Filter by category
        await home_page.filter_by_category("Electronics")
        
        # Assert filtered count
        await home_page.assert_element_count(".product-card", 5)
    
    @pytest.mark.smoke
    async def test_combined_assertions(self, home_page: HomePage):
        """Demonstrates multiple assertion types in one test."""
        await home_page.navigate()
        
        # URL assertion
        await home_page.assert_url_contains("/")
        
        # Visibility assertions
        await home_page.assert_element_visible("#search-input")
        await home_page.assert_element_visible(".cart-icon")
        
        # Add product to cart
        await home_page.add_product_to_cart("Laptop")
        
        # Text assertion - cart count
        await home_page.assert_cart_count(1)
        
        # Element count assertion
        product_count = 12
        await home_page.assert_element_count(".product-card", product_count)
    
    @pytest.mark.regression
    async def test_custom_page_assertions(self, dashboard_page: DashboardPage):
        """Demonstrates custom assertion methods in page objects."""
        await dashboard_page.navigate()
        
        # Custom assertion for dashboard
        await dashboard_page.assert_on_dashboard()
        
        # Custom assertion for metrics
        await dashboard_page.assert_metric_exists("Total Sales")
        await dashboard_page.assert_metric_value("Total Sales", "$10,000")
        
        # Custom assertion for charts
        await dashboard_page.assert_charts_loaded()
