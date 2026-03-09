import pytest
from pages.home_page import HomePage
from pages.checkout_page import CheckoutPage


class TestEncapsulationAndAbstraction:
    """
    Tests demonstrating ENCAPSULATION and ABSTRACTION:
    - Tests don't know about internal selectors (encapsulation)
    - Tests call high-level methods that hide complexity (abstraction)
    """
    
    @pytest.mark.smoke
    async def test_menu_encapsulation(self, home_page: HomePage):
        """
        Demonstrates ENCAPSULATION:
        - Test doesn't know which selector is used for the menu
        - All selector logic is hidden inside the HomePage class
        """
        await home_page.navigate()
        
        # We call openMenu() without knowing the internal selector
        await home_page.open_menu()
        await home_page.assert_menu_visible()
        
        await home_page.close_menu()
        await home_page.assert_menu_hidden()
    
    @pytest.mark.regression
    async def test_search_and_add_to_cart_abstraction(self, home_page: HomePage):
        """
        Demonstrates ABSTRACTION:
        - search_product() hides multiple internal steps
        - add_product_to_cart() encapsulates complex product selection logic
        """
        await home_page.navigate()
        
        # High-level method hides search implementation
        await home_page.search_product("Laptop")
        await home_page.assert_product_exists("Laptop")
        
        # High-level method hides cart addition complexity
        await home_page.add_product_to_cart("Laptop")
        await home_page.assert_cart_count(1)
        
        await home_page.add_product_to_cart("Laptop")
        await home_page.assert_cart_count(2)
    
    @pytest.mark.smoke
    async def test_complete_checkout_abstraction(self, checkout_page: CheckoutPage):
        """
        Demonstrates ABSTRACTION at its best:
        - complete_checkout() performs MANY internal steps
        - Test only calls one method with data
        - All complexity is hidden inside the page object
        """
        await checkout_page.navigate()
        await checkout_page.assert_on_checkout_page()
        
        shipping_info = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "address": "123 Main Street",
            "city": "New York",
            "zip_code": "10001",
            "country": "USA"
        }
        
        payment_info = {
            "card_number": "4111111111111111",
            "expiry": "12/25",
            "cvv": "123"
        }
        
        # One method call completes entire checkout process
        # This is abstraction: hiding complexity behind a simple interface
        await checkout_page.complete_checkout(
            shipping_info=shipping_info,
            payment_info=payment_info,
            shipping_method="express",
            payment_method="credit-card"
        )
        
        await checkout_page.assert_order_successful()
    
    @pytest.mark.regression
    async def test_encapsulated_selectors_not_exposed(self, home_page: HomePage):
        """
        Demonstrates ENCAPSULATION:
        - Test cannot access private selectors
        - All interactions go through public methods
        """
        await home_page.navigate()
        
        # These methods hide the selectors completely
        await home_page.select_menu_item("Electronics")
        await home_page.filter_by_category("Laptops")
        
        # The test doesn't need to know:
        # - What selector is used for menu
        # - What selector is used for category filter
        # - How the filtering mechanism works
        # All of that is ENCAPSULATED in the page object
