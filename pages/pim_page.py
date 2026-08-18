from pages.base_page import BasePage
from playwright.async_api import Page


class PIMPage(BasePage):
    """
    OrangeHRM PIM (Employee List) Page demonstrating:
    - Encapsulation: Private selectors hidden from tests
    - Inheritance: Inherits common methods from BasePage
    - Reusable page actions for the Employee List
    """

    # Encapsulation: Private selectors for the PIM Employee List page
    _PAGE_HEADING = "h5:has-text('Employee Information')"
    _ADD_BUTTON = ".orangehrm-header-container button"
    _FILTER_AREA = ".oxd-table-filter-area"
    _FILTER_TOGGLE_BUTTON = ".oxd-table-filter-header-options button"
    # Scoped by the field's label since both "Employee Name" and "Supervisor
    # Name" share the same "Type for hints..." placeholder on this form.
    _EMPLOYEE_NAME_INPUT = f"{_FILTER_AREA} .oxd-input-group:has(label:has-text('Employee Name')) input"
    _SEARCH_BUTTON = f"{_FILTER_AREA} button[type='submit']"
    _RESET_BUTTON = f"{_FILTER_AREA} button:has-text('Reset')"

    # Table selectors
    _RECORDS_TABLE = ".oxd-table-body"
    _TABLE_ROWS = f"{_RECORDS_TABLE} .oxd-table-row"
    _NO_RECORDS_MESSAGE = "span:has-text('No Records'), .orangehrm-horizontal-padding span"

    async def navigate(self) -> None:
        """Navigate to PIM Employee List page (requires authentication)."""
        await self._page.goto(f"{self._base_url}/web/index.php/pim/viewEmployeeList")
        await self.wait_for_page_load()
        await self._page.wait_for_timeout(2000)  # Additional wait for dynamic content

    async def ensure_filter_area_expanded(self) -> None:
        """Expand the search filter panel if it's currently collapsed."""
        if not await self.is_visible(self._FILTER_AREA):
            await self.click_element(self._FILTER_TOGGLE_BUTTON)
            await self.wait_for_selector(self._FILTER_AREA)

    async def search_by_employee_name(self, name: str) -> None:
        """Search the employee list by (partial) employee name."""
        await self.ensure_filter_area_expanded()
        await self.fill_input(self._EMPLOYEE_NAME_INPUT, name)
        await self.click_element(self._SEARCH_BUTTON)
        await self.wait_for_page_load()

    async def click_add_button(self) -> None:
        """Click the Add button to create a new employee."""
        await self.click_element(self._ADD_BUTTON)
        await self.wait_for_page_load()

    async def get_records_count(self) -> int:
        """Get the number of employee records displayed in the table."""
        rows = self._page.locator(self._TABLE_ROWS)
        return await rows.count()

    # Assertions
    async def assert_on_pim_page(self) -> None:
        """Assertion: Validate we're on the PIM Employee List page."""
        await self.assert_url_contains("/pim/viewEmployeeList")
        await self.assert_element_visible(self._PAGE_HEADING)

    async def assert_add_button_visible(self) -> None:
        """Assertion: Validate Add button is visible."""
        await self.assert_element_visible(self._ADD_BUTTON)

    async def assert_records_found(self) -> None:
        """Assertion: Validate that employee records are displayed."""
        # Wait for a row to render before counting, since the table can be
        # momentarily empty right after a search while results are loading.
        await self.wait_for_selector(self._TABLE_ROWS)
        count = await self.get_records_count()
        assert count > 0, f"Expected records to be found, but got {count}"

    async def assert_no_records_found(self) -> None:
        """Assertion: Validate 'No Records Found' message is displayed."""
        await self.assert_element_visible(self._NO_RECORDS_MESSAGE)
