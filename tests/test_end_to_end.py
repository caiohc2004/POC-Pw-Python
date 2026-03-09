import pytest
from pages.client_login_page import ClientLoginPage
from pages.home_page import HomePage
from pages.checkout_page import CheckoutPage


class TestEndToEnd:
    """
    End-to-end tests demonstrating ALL principles together:
    - Polymorphism, Encapsulation, Abstraction, Inheritance
    - Design Patterns (POM), Fixtures, Async, Clean Code, Assertions
    """
    
    @pytest.mark.smoke
    async def test_complete_shopping_flow(self,
                                          client_login_page: ClientLoginPage,
                                          client_credentials: dict,
                                          home_page: HomePage,
                                          checkout_page: CheckoutPage):
        """
        Complete e2e test demonstrating all OOP principles:
        1. Login (Polymorphism - client-specific login)
        2. Search & Add to Cart (Abstraction - high-level methods)
        3. Checkout (Encapsulation - hidden complexity)
        4. Assertions (Validation at each step)
        All using async/await and clean code practices.
        """
        # 1. Login using polymorphic login method
        await client_login_page.login(
            client_credentials["username"],
            client_credentials["password"],
            remember_me=True
        )
        await client_login_page.assert_login_successful()
        await client_login_page.assert_profile_icon_visible()
        
        # 2. Navigate to home (inherited method)
        await home_page.navigate()
        await home_page.wait_for_page_load()
        
        # 3. Search for product (abstraction)
        await home_page.search_product("Laptop")
        await home_page.assert_product_exists("Gaming Laptop")
        
        # 4. Add to cart (encapsulated complexity)
        await home_page.add_product_to_cart("Gaming Laptop")
        await home_page.assert_cart_count(1)
        
        # 5. Add another item
        await home_page.add_product_to_cart("Wireless Mouse")
        await home_page.assert_cart_count(2)
        
        # 6. Navigate to checkout
        await home_page.open_cart()
        await checkout_page.navigate()
        await checkout_page.assert_on_checkout_page()
        
        # 7. Complete checkout (high-level abstraction)
        shipping_info = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "address": "456 Oak Avenue",
            "city": "Los Angeles",
            "zip_code": "90001",
            "country": "USA"
        }
        
        payment_info = {
            "card_number": "5555555555554444",
            "expiry": "03/26",
            "cvv": "456"
        }
        
        await checkout_page.complete_checkout(
            shipping_info=shipping_info,
            payment_info=payment_info,
            shipping_method="express",
            payment_method="credit-card"
        )
        
        # 8. Verify order success (assertions)
        await checkout_page.assert_order_successful()
        success_message = await checkout_page.get_success_message()
        assert "success" in success_message.lower()
        await checkout_page.assert_url_contains("/order-confirmation")
    
    @pytest.mark.regression
    async def test_guest_checkout_flow(self, home_page: HomePage, 
                                       checkout_page: CheckoutPage):
        """
        E2E test for guest checkout (no login required).
        Demonstrates clean separation of concerns.
        """
        # Skip login, go directly to shopping
        await home_page.navigate()
        
        # Browse and add products
        await home_page.filter_by_category("Electronics")
        await home_page.add_product_to_cart("Smartphone")
        await home_page.assert_cart_count(1)
        
        # Proceed to checkout
        await home_page.open_cart()
        await checkout_page.navigate()
        
        # Complete checkout as guest
        shipping_info = {
            "first_name": "Guest",
            "last_name": "User",
            "email": "guest@example.com",
            "address": "789 Pine Street",
            "city": "Chicago",
            "zip_code": "60601",
            "country": "USA"
        }
        
        payment_info = {
            "card_number": "4111111111111111",
            "expiry": "12/25",
            "cvv": "789"
        }
        
        await checkout_page.complete_checkout(
            shipping_info=shipping_info,
            payment_info=payment_info
        )
        
        await checkout_page.assert_order_successful()
    
    @pytest.mark.regression
    async def test_multiple_items_checkout(self, logged_in_client: ClientLoginPage,
                                           home_page: HomePage,
                                           checkout_page: CheckoutPage):
        """
        E2E test with logged-in user (using fixture).
        Demonstrates dependency injection.
        """
        # User is already logged in via fixture
        await logged_in_client.assert_login_successful()
        
        # Navigate home
        await home_page.navigate()
        
        # Add multiple items
        products = ["Laptop", "Mouse", "Keyboard", "Monitor"]
        for product in products:
            await home_page.add_product_to_cart(product)
        
        # Verify cart count
        await home_page.assert_cart_count(len(products))
        
        # Checkout
        await home_page.open_cart()
        await checkout_page.navigate()
        
        shipping_info = {
            "first_name": "Bulk",
            "last_name": "Buyer",
            "email": "bulk@example.com",
            "address": "321 Elm Street",
            "city": "Houston",
            "zip_code": "77001",
            "country": "USA"
        }
        
        payment_info = {
            "card_number": "378282246310005",
            "expiry": "06/27",
            "cvv": "1234"
        }
        
        await checkout_page.complete_checkout(
            shipping_info=shipping_info,
            payment_info=payment_info,
            shipping_method="overnight"
        )
        
        await checkout_page.assert_order_successful()
