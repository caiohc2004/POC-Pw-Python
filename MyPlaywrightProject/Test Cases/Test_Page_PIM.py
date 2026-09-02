import os
import pytest
from pages.admin_login_page import AdminLoginPage
from pages.pim_page import PIMPage


class TestPIMOrangeHRM:
    """
    OrangeHRM PIM (Employee List) tests using Page Object pattern.
    Demonstrates Encapsulation, Inheritance, and Polymorphism.
    """

    @pytest.mark.smoke
    async def test_navigate_to_pim_page(
        self,
        admin_login_page: AdminLoginPage,
        admin_credentials: dict,
        base_url: str
    ):
        """Test navigation to PIM Employee List page after login."""
        await admin_login_page.login(admin_credentials["username"],
                                     admin_credentials["password"])
        await admin_login_page.assert_dashboard_visible()

        pim_page = PIMPage(admin_login_page.page, base_url)
        await pim_page.navigate()
        await pim_page.assert_on_pim_page()
        if not os.getenv("CI"):
            await admin_login_page.page.pause()

    @pytest.mark.smoke
    async def test_search_employee_by_name(
        self,
        admin_login_page: AdminLoginPage,
        admin_credentials: dict,
        base_url: str
    ):
        """Test searching the employee list by name returns results."""
        await admin_login_page.login(admin_credentials["username"],
                                     admin_credentials["password"])

        pim_page = PIMPage(admin_login_page.page, base_url)
        await pim_page.navigate()

        await pim_page.search_by_employee_name("a")
        await pim_page.assert_records_found()
        if not os.getenv("CI"):
            await admin_login_page.page.pause()

    @pytest.mark.regression
    async def test_search_nonexistent_employee(
        self,
        admin_login_page: AdminLoginPage,
        admin_credentials: dict,
        base_url: str
    ):
        """Test searching for a non-existent employee shows no records."""
        await admin_login_page.login(admin_credentials["username"],
                                     admin_credentials["password"])

        pim_page = PIMPage(admin_login_page.page, base_url)
        await pim_page.navigate()
        await pim_page.search_by_employee_name("ZZNonExistentEmployee99999")
        await pim_page.assert_no_records_found()
        if not os.getenv("CI"):
            await admin_login_page.page.pause()

    @pytest.mark.regression
    async def test_add_employee_button_visible(
        self,
        admin_login_page: AdminLoginPage,
        admin_credentials: dict,
        base_url: str
    ):
        """Test that Add button is visible on the PIM Employee List page."""
        await admin_login_page.login(admin_credentials["username"],
                                     admin_credentials["password"])

        pim_page = PIMPage(admin_login_page.page, base_url)
        await pim_page.navigate()
        await pim_page.assert_add_button_visible()
        if not os.getenv("CI"):
            await admin_login_page.page.pause() 
