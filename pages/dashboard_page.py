from pages.base_page import BasePage
from typing import List, Dict


class DashboardPage(BasePage):
    """
    Dashboard Page demonstrating:
    - Clean Code: Well-organized methods with clear purposes
    - Encapsulation: Internal widget and metric handling
    - Abstraction: High-level dashboard operations
    """
    
    # Encapsulation: Private selectors
    _DASHBOARD_TITLE = "h1.dashboard-title"
    _WIDGET_CONTAINER = ".widget-container"
    _METRIC_CARD = ".metric-card"
    _CHART_ELEMENT = ".chart"
    _NOTIFICATION_BADGE = ".notification-badge"
    _USER_MENU = ".user-menu"
    _LOGOUT_BUTTON = "#logout-button"
    _SETTINGS_LINK = "a[href='/settings']"
    _REFRESH_BUTTON = "#refresh-dashboard"
    _DATE_RANGE_SELECTOR = "#date-range"
    _EXPORT_BUTTON = "#export-data"
    
    async def navigate(self) -> None:
        """Navigate to dashboard page."""
        await self._page.goto(f"{self._base_url}/dashboard")
        await self.wait_for_page_load()
    
    async def wait_for_dashboard_load(self) -> None:
        """
        Abstraction: Wait for all dashboard components to load.
        Hides the complexity of waiting for multiple elements.
        """
        await self.wait_for_selector(self._DASHBOARD_TITLE)
        await self.wait_for_selector(self._WIDGET_CONTAINER)
        await self.wait_for_page_load()
    
    async def get_metric_value(self, metric_name: str) -> str:
        """
        Get value of a specific metric card.
        Encapsulation: Hides selector complexity.
        """
        metric_selector = f"{self._METRIC_CARD}:has-text('{metric_name}') .metric-value"
        return await self.get_text(metric_selector)
    
    async def get_all_metrics(self) -> List[Dict[str, str]]:
        """
        Get all metrics from dashboard.
        Demonstrates working with collections.
        """
        metrics = []
        metric_elements = await self._page.query_selector_all(self._METRIC_CARD)
        
        for element in metric_elements:
            name = await element.query_selector(".metric-name")
            value = await element.query_selector(".metric-value")
            
            if name and value:
                metrics.append({
                    "name": await name.text_content(),
                    "value": await value.text_content()
                })
        
        return metrics
    
    async def refresh_dashboard(self) -> None:
        """
        Refresh dashboard data.
        Abstraction: Simple method call hides refresh logic.
        """
        await self.click_element(self._REFRESH_BUTTON)
        await self.wait_for_page_load()
        await self.wait_for_dashboard_load()
    
    async def select_date_range(self, range_option: str) -> None:
        """Select date range for dashboard data."""
        await self._page.select_option(self._DATE_RANGE_SELECTOR, range_option)
        await self.wait_for_page_load()
    
    async def export_dashboard_data(self) -> None:
        """Export dashboard data."""
        async with self._page.expect_download() as download_info:
            await self.click_element(self._EXPORT_BUTTON)
        download = await download_info.value
        return download
    
    async def open_user_menu(self) -> None:
        """Open user menu."""
        await self.click_element(self._USER_MENU)
        await self.wait_for_timeout(300)
    
    async def logout(self) -> None:
        """
        Logout user from dashboard.
        Abstraction: Combines multiple steps into one action.
        """
        await self.open_user_menu()
        await self.click_element(self._LOGOUT_BUTTON)
        await self.wait_for_page_load()
    
    async def navigate_to_settings(self) -> None:
        """Navigate to settings page."""
        await self.click_element(self._SETTINGS_LINK)
        await self.wait_for_page_load()
    
    async def get_notification_count(self) -> int:
        """Get number of unread notifications."""
        if await self.is_visible(self._NOTIFICATION_BADGE):
            badge_text = await self.get_text(self._NOTIFICATION_BADGE)
            return int(badge_text) if badge_text.isdigit() else 0
        return 0
    
    async def assert_on_dashboard(self) -> None:
        """Assertion: Validate we're on dashboard page."""
        await self.assert_url_contains("/dashboard")
        await self.assert_element_visible(self._DASHBOARD_TITLE)
    
    async def assert_metric_exists(self, metric_name: str) -> None:
        """Assertion: Validate specific metric card exists."""
        metric_selector = f"{self._METRIC_CARD}:has-text('{metric_name}')"
        await self.assert_element_visible(metric_selector)
    
    async def assert_metric_value(self, metric_name: str, expected_value: str) -> None:
        """Assertion: Validate metric has expected value."""
        metric_selector = f"{self._METRIC_CARD}:has-text('{metric_name}') .metric-value"
        await self.assert_element_has_text(metric_selector, expected_value)
    
    async def assert_charts_loaded(self) -> None:
        """Assertion: Validate all charts are loaded."""
        charts = self._page.locator(self._CHART_ELEMENT)
        count = await charts.count()
        assert count > 0, "No charts found on dashboard"
        await self.assert_element_visible(self._CHART_ELEMENT)
