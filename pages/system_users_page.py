from pages.base_page import BasePage
from playwright.async_api import Page


class SystemUsersPage(BasePage):
    """
    OrangeHRM Admin System Users Page demonstrating:
    - Encapsulation: Private selectors hidden from tests
    - Inheritance: Inherits common methods from BasePage
    - Reusable page actions for CRUD operations on system users
    """

    # Encapsulation: Private selectors for System Users page
    _PAGE_HEADING = "h6:has-text('User Management')"
    _ADD_BUTTON = ".orangehrm-header-container button"
    _SEARCH_USERNAME_INPUT = "input[placeholder*='Username'], input.oxd-input"
    _SEARCH_BUTTON = "button[type='submit']"
    _RESET_BUTTON = "button:has-text('Reset'), button.oxd-button--ghost"
    
    # Dropdown selectors
    _USER_ROLE_DROPDOWN = "div.oxd-select-text:near(label:has-text('User Role'))"
    _STATUS_DROPDOWN = "div.oxd-select-text:near(label:has-text('Status'))"
    _EMPLOYEE_NAME_INPUT = "input[placeholder='Type for hints...']"
    
    # Table selectors
    _RECORDS_TABLE = ".oxd-table-body"
    _TABLE_ROWS = ".oxd-table-card"
    _NO_RECORDS_MESSAGE = "span:has-text('No Records'), .orangehrm-horizontal-padding span"
    _RECORD_COUNT_TEXT = ".orangehrm-horizontal-padding span"
    
    # Action buttons in table
    _EDIT_BUTTON = "button i.bi-pencil-fill"
    _DELETE_BUTTON = "button i.bi-trash"
    
    # Toast/Success messages
    _SUCCESS_MESSAGE = ".oxd-toast-content--success"
    _DELETE_CONFIRMATION_DIALOG = "div[role='document']"
    _CONFIRM_DELETE_BUTTON = "button:has-text('Yes, Delete')"

    async def navigate(self) -> None:
        """Navigate to System Users page (requires authentication)."""
        await self._page.goto(f"{self._base_url}/web/index.php/admin/viewSystemUsers")
        await self.wait_for_page_load()
        await self._page.wait_for_timeout(2000)  # Additional wait for dynamic content

    async def click_add_button(self) -> None:
        """Click the Add button to create a new user."""
        await self.click_element(self._ADD_BUTTON)
        await self.wait_for_page_load()

    async def search_by_username(self, username: str) -> None:
        """Search for a user by username."""
        await self.fill_input(self._SEARCH_USERNAME_INPUT, username)
        await self.click_element(self._SEARCH_BUTTON)
        await self.wait_for_page_load()

    async def select_user_role(self, role: str) -> None:
        """Select user role from dropdown (Admin or ESS)."""
        await self.click_element(self._USER_ROLE_DROPDOWN)
        await self._page.click(f"text={role}")

    async def select_status(self, status: str) -> None:
        """Select user status from dropdown (Enabled or Disabled)."""
        await self.click_element(self._STATUS_DROPDOWN)
        await self._page.click(f"text={status}")

    async def fill_employee_name(self, name: str) -> None:
        """Fill employee name autocomplete field."""
        await self.fill_input(self._EMPLOYEE_NAME_INPUT, name)
        await self._page.wait_for_timeout(1000)  # Wait for autocomplete

    async def click_reset_button(self) -> None:
        """Click Reset button to clear search filters."""
        await self.click_element(self._RESET_BUTTON)
        await self.wait_for_page_load()

    async def get_records_count(self) -> int:
        """Get the number of user records displayed in the table."""
        rows = self._page.locator(self._TABLE_ROWS)
        return await rows.count()

    async def click_edit_first_record(self) -> None:
        """Click edit button on the first user record."""
        edit_buttons = self._page.locator(self._EDIT_BUTTON)
        await edit_buttons.first.click()
        await self.wait_for_page_load()

    async def click_delete_first_record(self) -> None:
        """Click delete button on the first user record."""
        delete_buttons = self._page.locator(self._DELETE_BUTTON)
        await delete_buttons.first.click()

    async def confirm_delete(self) -> None:
        """Confirm deletion in the confirmation dialog."""
        await self.wait_for_selector(self._DELETE_CONFIRMATION_DIALOG)
        await self.click_element(self._CONFIRM_DELETE_BUTTON)
        await self.wait_for_page_load()

    # Assertions
    async def assert_on_system_users_page(self) -> None:
        """Assertion: Validate we're on the System Users page."""
        await self.assert_url_contains("/admin/viewSystemUsers")
        await self.assert_element_visible(self._PAGE_HEADING)

    async def assert_add_button_visible(self) -> None:
        """Assertion: Validate Add button is visible."""
        await self.assert_element_visible(self._ADD_BUTTON)

    async def assert_no_records_found(self) -> None:
        """Assertion: Validate 'No Records Found' message is displayed."""
        await self.assert_element_visible(self._NO_RECORDS_MESSAGE)

    async def assert_records_found(self) -> None:
        """Assertion: Validate that user records are displayed."""
        count = await self.get_records_count()
        assert count > 0, f"Expected records to be found, but got {count}"

    async def assert_success_message_visible(self) -> None:
        """Assertion: Validate success toast message is visible."""
        await self.assert_element_visible(self._SUCCESS_MESSAGE)

    async def assert_specific_user_visible(self, username: str) -> None:
        """Assertion: Validate specific username appears in the table."""
        # Look for username in table rows, not just anywhere
        await self.assert_element_visible(f".oxd-table-card:has-text('{username}')")
