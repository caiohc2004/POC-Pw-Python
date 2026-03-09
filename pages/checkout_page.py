from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """
    Checkout Page demonstrating:
    - Abstraction: complete_checkout() hides multiple complex steps
    - Encapsulation: Form filling logic is internal
    - Clean Code: Each method has a single, clear purpose
    """
    
    # Encapsulation: Private selectors
    _FIRST_NAME_INPUT = "#first-name"
    _LAST_NAME_INPUT = "#last-name"
    _EMAIL_INPUT = "#email"
    _ADDRESS_INPUT = "#address"
    _CITY_INPUT = "#city"
    _ZIP_CODE_INPUT = "#zip-code"
    _COUNTRY_SELECT = "#country"
    _CARD_NUMBER_INPUT = "#card-number"
    _CARD_EXPIRY_INPUT = "#card-expiry"
    _CARD_CVV_INPUT = "#card-cvv"
    _PLACE_ORDER_BUTTON = "button[data-test='place-order']"
    _ORDER_SUMMARY = ".order-summary"
    _ORDER_TOTAL = ".order-total"
    _SUCCESS_MESSAGE = ".success-message"
    _SHIPPING_METHOD_RADIO = "input[name='shipping-method']"
    _PAYMENT_METHOD_RADIO = "input[name='payment-method']"
    
    async def navigate(self) -> None:
        """Navigate to checkout page."""
        await self._page.goto(f"{self._base_url}/checkout")
        await self.wait_for_page_load()
    
    async def fill_shipping_information(self, first_name: str, last_name: str, 
                                        email: str, address: str, 
                                        city: str, zip_code: str, country: str) -> None:
        """
        Abstraction: Groups related fields into one high-level action.
        """
        await self.fill_input(self._FIRST_NAME_INPUT, first_name)
        await self.fill_input(self._LAST_NAME_INPUT, last_name)
        await self.fill_input(self._EMAIL_INPUT, email)
        await self.fill_input(self._ADDRESS_INPUT, address)
        await self.fill_input(self._CITY_INPUT, city)
        await self.fill_input(self._ZIP_CODE_INPUT, zip_code)
        await self._page.select_option(self._COUNTRY_SELECT, country)
    
    async def select_shipping_method(self, method: str) -> None:
        """Select shipping method (e.g., 'standard', 'express', 'overnight')."""
        await self.click_element(f"{self._SHIPPING_METHOD_RADIO}[value='{method}']")
    
    async def select_payment_method(self, method: str) -> None:
        """Select payment method (e.g., 'credit-card', 'paypal', 'crypto')."""
        await self.click_element(f"{self._PAYMENT_METHOD_RADIO}[value='{method}']")
    
    async def fill_payment_information(self, card_number: str, expiry: str, cvv: str) -> None:
        """
        Abstraction: Encapsulates payment form filling.
        """
        await self.fill_input(self._CARD_NUMBER_INPUT, card_number)
        await self.fill_input(self._CARD_EXPIRY_INPUT, expiry)
        await self.fill_input(self._CARD_CVV_INPUT, cvv)
    
    async def click_place_order(self) -> None:
        """Click the place order button."""
        await self.click_element(self._PLACE_ORDER_BUTTON)
        await self.wait_for_page_load()
    
    async def complete_checkout(self, shipping_info: dict, payment_info: dict,
                               shipping_method: str = "standard",
                               payment_method: str = "credit-card") -> None:
        """
        Abstraction: High-level method that completes entire checkout.
        This demonstrates how a test can call one method instead of many steps.
        
        Example usage:
            shipping = {
                "first_name": "John", "last_name": "Doe",
                "email": "john@example.com", "address": "123 Main St",
                "city": "New York", "zip_code": "10001", "country": "USA"
            }
            payment = {
                "card_number": "4111111111111111",
                "expiry": "12/25", "cvv": "123"
            }
            await checkout_page.complete_checkout(shipping, payment)
        """
        await self.fill_shipping_information(
            shipping_info["first_name"],
            shipping_info["last_name"],
            shipping_info["email"],
            shipping_info["address"],
            shipping_info["city"],
            shipping_info["zip_code"],
            shipping_info["country"]
        )
        
        await self.select_shipping_method(shipping_method)
        await self.select_payment_method(payment_method)
        
        if payment_method == "credit-card":
            await self.fill_payment_information(
                payment_info["card_number"],
                payment_info["expiry"],
                payment_info["cvv"]
            )
        
        await self.click_place_order()
    
    async def get_order_total(self) -> str:
        """Get the total order amount."""
        return await self.get_text(self._ORDER_TOTAL)
    
    async def get_success_message(self) -> str:
        """Get the success message after order placement."""
        return await self.get_text(self._SUCCESS_MESSAGE)
    
    async def assert_on_checkout_page(self) -> None:
        """Assertion: Validate we're on checkout page."""
        await self.assert_url_contains("/checkout")
        await self.assert_element_visible(self._ORDER_SUMMARY)
    
    async def assert_order_successful(self) -> None:
        """Assertion: Validate order was placed successfully."""
        await self.assert_element_visible(self._SUCCESS_MESSAGE)
        await self.assert_element_contains_text(self._SUCCESS_MESSAGE, "success")
    
    async def assert_shipping_method_selected(self, method: str) -> None:
        """Assertion: Validate shipping method is selected."""
        selector = f"{self._SHIPPING_METHOD_RADIO}[value='{method}']"
        await self.assert_element_has_attribute(selector, "checked", "")
