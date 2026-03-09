from playwright.async_api import Page, expect
from abc import ABC, abstractmethod
import os


class BasePage(ABC):
    """
    Base Page class demonstrating:
    - Inheritance: All pages inherit from this class
    - Encapsulation: Common methods and properties are hidden here
    - Abstraction: Abstract methods force child classes to implement specific behavior
    """
    
    def __init__(self, page: Page, base_url: str):
        self._page = page
        self._base_url = base_url
        self._timeout = int(os.getenv("TIMEOUT", "30000"))
    
    @property
    def page(self) -> Page:
        """Encapsulated page object."""
        return self._page
    
    @abstractmethod
    async def navigate(self) -> None:
        """Abstract method - each page must implement its own navigation."""
        pass
    
    async def wait_for_page_load(self) -> None:
        """Common method inherited by all pages."""
        await self._page.wait_for_load_state("networkidle")
        await self._page.wait_for_load_state("domcontentloaded")
    
    async def get_page_title(self) -> str:
        """Get the current page title."""
        return await self._page.title()
    
    async def get_current_url(self) -> str:
        """Get the current page URL."""
        return self._page.url
    
    async def wait_for_timeout(self, timeout: int) -> None:
        """Wait for a specific timeout."""
        await self._page.wait_for_timeout(timeout)
    
    async def take_screenshot(self, path: str) -> None:
        """Take a screenshot of the current page."""
        await self._page.screenshot(path=path)
    
    async def reload_page(self) -> None:
        """Reload the current page."""
        await self._page.reload()
        await self.wait_for_page_load()
    
    async def go_back(self) -> None:
        """Navigate back in browser history."""
        await self._page.go_back()
        await self.wait_for_page_load()
    
    async def click_element(self, selector: str) -> None:
        """Click an element with encapsulated error handling."""
        await self._page.click(selector, timeout=self._timeout)
    
    async def fill_input(self, selector: str, value: str) -> None:
        """Fill an input field with encapsulated behavior."""
        await self._page.fill(selector, value, timeout=self._timeout)
    
    async def get_text(self, selector: str) -> str:
        """Get text content of an element."""
        return await self._page.text_content(selector)
    
    async def is_visible(self, selector: str) -> bool:
        """Check if element is visible."""
        return await self._page.is_visible(selector)
    
    async def wait_for_selector(self, selector: str, state: str = "visible") -> None:
        """Wait for a selector to reach a specific state."""
        await self._page.wait_for_selector(selector, state=state, timeout=self._timeout)
    
    async def assert_url_contains(self, expected_url_part: str) -> None:
        """Assertion: Validate URL contains expected text."""
        await expect(self._page).to_have_url(lambda url: expected_url_part in url, timeout=self._timeout)
    
    async def assert_title_contains(self, expected_title: str) -> None:
        """Assertion: Validate page title contains expected text."""
        await expect(self._page).to_have_title(lambda title: expected_title in title, timeout=self._timeout)
    
    async def assert_element_visible(self, selector: str) -> None:
        """Assertion: Validate element is visible."""
        element = self._page.locator(selector)
        await expect(element).to_be_visible(timeout=self._timeout)
    
    async def assert_element_hidden(self, selector: str) -> None:
        """Assertion: Validate element is hidden."""
        element = self._page.locator(selector)
        await expect(element).to_be_hidden(timeout=self._timeout)
    
    async def assert_element_has_text(self, selector: str, expected_text: str) -> None:
        """Assertion: Validate element has exact text."""
        element = self._page.locator(selector)
        await expect(element).to_have_text(expected_text, timeout=self._timeout)
    
    async def assert_element_contains_text(self, selector: str, expected_text: str) -> None:
        """Assertion: Validate element contains text."""
        element = self._page.locator(selector)
        await expect(element).to_contain_text(expected_text, timeout=self._timeout)
    
    async def assert_element_has_attribute(self, selector: str, attribute: str, value: str) -> None:
        """Assertion: Validate element has specific attribute value."""
        element = self._page.locator(selector)
        await expect(element).to_have_attribute(attribute, value, timeout=self._timeout)
    
    async def assert_element_count(self, selector: str, count: int) -> None:
        """Assertion: Validate number of elements matching selector."""
        elements = self._page.locator(selector)
        await expect(elements).to_have_count(count, timeout=self._timeout)
