from pages.base_page import BasePage


class HomePage(BasePage):
    """
    Home Page demonstrating:
    - Encapsulation: Menu interaction logic is hidden
    - Abstraction: High-level methods like add_to_cart hide complex steps
    - Clean Code: Clear method names and single responsibilities
    """
    
    # Encapsulation: Private selectors
    _MENU_BUTTON = "#menu-button"
    _MENU_DROPDOWN = ".menu-dropdown"
    _PRODUCT_CARD = ".product-card"
    _ADD_TO_CART_BUTTON = "button[data-action='add-to-cart']"
    _CART_ICON = ".cart-icon"
    _CART_BADGE = ".cart-badge"
    _SEARCH_INPUT = "#search-input"
    _SEARCH_BUTTON = "#search-button"
    _CATEGORY_FILTER = ".category-filter"
    
    async def navigate(self) -> None:
        """Navigate to home page."""
        await self._page.goto(f"{self._base_url}/")
        await self.wait_for_page_load()
    
    async def open_menu(self) -> None:
        """
        Encapsulation: Test doesn't know about internal selectors.
        This method hides the implementation details.
        """
        await self.click_element(self._MENU_BUTTON)
        await self.wait_for_selector(self._MENU_DROPDOWN, state="visible")
    
    async def close_menu(self) -> None:
        """Close the menu."""
        if await self.is_visible(self._MENU_DROPDOWN):
            await self.click_element(self._MENU_BUTTON)
            await self.wait_for_selector(self._MENU_DROPDOWN, state="hidden")
    
    async def select_menu_item(self, item_name: str) -> None:
        """Select a specific menu item by name."""
        await self.open_menu()
        await self.click_element(f"{self._MENU_DROPDOWN} >> text={item_name}")
        await self.wait_for_page_load()
    
    async def search_product(self, product_name: str) -> None:
        """
        Abstraction: High-level action that hides multiple steps.
        """
        await self.fill_input(self._SEARCH_INPUT, product_name)
        await self.click_element(self._SEARCH_BUTTON)
        await self.wait_for_page_load()
    
    async def add_product_to_cart(self, product_name: str) -> None:
        """
        Abstraction: Encapsulates the logic to add a product to cart.
        Test only needs to call this method without knowing the steps.
        """
        product_card = f"{self._PRODUCT_CARD}:has-text('{product_name}')"
        await self.wait_for_selector(product_card)
        add_button = f"{product_card} {self._ADD_TO_CART_BUTTON}"
        await self.click_element(add_button)
        await self.wait_for_timeout(500)
    
    async def get_cart_item_count(self) -> int:
        """Get the number of items in the cart."""
        badge_text = await self.get_text(self._CART_BADGE)
        return int(badge_text) if badge_text.isdigit() else 0
    
    async def open_cart(self) -> None:
        """Open the shopping cart."""
        await self.click_element(self._CART_ICON)
        await self.wait_for_page_load()
    
    async def filter_by_category(self, category: str) -> None:
        """Filter products by category."""
        await self.click_element(f"{self._CATEGORY_FILTER} >> text={category}")
        await self.wait_for_page_load()
    
    async def assert_menu_visible(self) -> None:
        """Assertion: Validate menu is visible."""
        await self.assert_element_visible(self._MENU_DROPDOWN)
    
    async def assert_menu_hidden(self) -> None:
        """Assertion: Validate menu is hidden."""
        await self.assert_element_hidden(self._MENU_DROPDOWN)
    
    async def assert_product_exists(self, product_name: str) -> None:
        """Assertion: Validate product card exists on the page."""
        product_selector = f"{self._PRODUCT_CARD}:has-text('{product_name}')"
        await self.assert_element_visible(product_selector)
    
    async def assert_cart_count(self, expected_count: int) -> None:
        """Assertion: Validate cart badge shows expected count."""
        await self.assert_element_has_text(self._CART_BADGE, str(expected_count))
