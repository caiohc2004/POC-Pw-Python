"""
Test Suite for SauceDemo Login Functionality

This module demonstrates best practices in test automation:
- Page Object Model (POM): Separation of test logic from page interactions
- Fixture Injection: Using pytest fixtures for setup and teardown
- Data-Driven Testing: Parameterized tests for multiple scenarios
- Clear Test Organization: Grouped by functionality with descriptive names
- Proper Assertions: Using expect and custom assertions
- Environment Variables: Secure credential management
"""

import pytest
from playwright.async_api import Page, expect
from pages.saucedemo_login_page import SauceDemoLoginPage


class TestSauceDemoLogin:
    """
    Test class for SauceDemo login functionality.
    
    Best Practices Demonstrated:
    - Test isolation: Each test is independent
    - Single responsibility: Each test validates one scenario
    - Descriptive naming: Test names clearly indicate what is being tested
    - Proper use of fixtures: Page objects injected via fixtures
    - Async/await: Proper handling of asynchronous operations
    """
    
    @pytest.mark.smoke
    @pytest.mark.asyncio
    async def test_successful_login_with_valid_credentials(
        self, 
        saucedemo_login_page: SauceDemoLoginPage, 
        saucedemo_credentials: dict
    ):
        """
        Test successful login with valid credentials.
        
        Steps:
        1. Navigate to login page (done by fixture)
        2. Enter valid username and password
        3. Click login button
        4. Verify successful login
        
        Expected Result: User is logged in and redirected to products page
        """
        # Act
        await saucedemo_login_page.login(
            saucedemo_credentials["username"],
            saucedemo_credentials["password"]
        )
        
        # Assert
        await saucedemo_login_page.assert_login_successful()
        assert await saucedemo_login_page.is_login_successful()
        
        # Verify products page title
        products_title = await saucedemo_login_page.get_products_title()
        assert products_title == "Products", f"Expected 'Products' but got '{products_title}'"
    
    @pytest.mark.smoke
    @pytest.mark.asyncio
    async def test_login_with_environment_credentials(
        self, 
        saucedemo_login_page: SauceDemoLoginPage
    ):
        """
        Test login using credentials from environment variables.
        
        Best Practice: Demonstrates secure credential management using .env file
        
        Expected Result: User is logged in successfully using env credentials
        """
        # Act
        await saucedemo_login_page.login_with_env_credentials()
        
        # Assert
        await saucedemo_login_page.assert_login_successful()
        assert await saucedemo_login_page.is_login_successful()
    
    @pytest.mark.regression
    @pytest.mark.asyncio
    async def test_login_failure_with_invalid_username(
        self, 
        saucedemo_login_page: SauceDemoLoginPage
    ):
        """
        Test login failure with invalid username.
        
        Expected Result: Error message is displayed
        """
        # Act
        await saucedemo_login_page.login("invalid_user", "secret_sauce")
        
        # Assert
        await saucedemo_login_page.assert_error_message_displayed()
        assert await saucedemo_login_page.is_error_displayed()
        await saucedemo_login_page.assert_error_message_contains("Username and password do not match")
    
    @pytest.mark.regression
    @pytest.mark.asyncio
    async def test_login_failure_with_invalid_password(
        self, 
        saucedemo_login_page: SauceDemoLoginPage,
        saucedemo_credentials: dict
    ):
        """
        Test login failure with invalid password.
        
        Expected Result: Error message is displayed
        """
        # Act
        await saucedemo_login_page.login(
            saucedemo_credentials["username"],
            "wrong_password"
        )
        
        # Assert
        await saucedemo_login_page.assert_error_message_displayed()
        assert await saucedemo_login_page.is_error_displayed()
    
    @pytest.mark.regression
    @pytest.mark.asyncio
    async def test_login_failure_with_empty_credentials(
        self, 
        saucedemo_login_page: SauceDemoLoginPage
    ):
        """
        Test login failure with empty username and password.
        
        Expected Result: Error message indicating username is required
        """
        # Act
        await saucedemo_login_page.login("", "")
        
        # Assert
        await saucedemo_login_page.assert_error_message_displayed()
        await saucedemo_login_page.assert_error_message_contains("Username is required")
    
    @pytest.mark.regression
    @pytest.mark.asyncio
    async def test_login_failure_with_locked_user(
        self, 
        saucedemo_login_page: SauceDemoLoginPage
    ):
        """
        Test login failure with locked out user.
        
        SauceDemo has a specific locked_out_user for testing
        
        Expected Result: Error message indicating user is locked out
        """
        # Act
        await saucedemo_login_page.login("locked_out_user", "secret_sauce")
        
        # Assert
        await saucedemo_login_page.assert_error_message_displayed()
        await saucedemo_login_page.assert_error_message_contains("locked out")
    
    @pytest.mark.regression
    @pytest.mark.asyncio
    @pytest.mark.parametrize("username,password,expected_error", [
        ("invalid_user", "secret_sauce", "Username and password do not match"),
        ("standard_user", "wrong_password", "Username and password do not match"),
        ("", "secret_sauce", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("locked_out_user", "secret_sauce", "locked out"),
    ])
    async def test_login_failures_parameterized(
        self, 
        saucedemo_login_page: SauceDemoLoginPage,
        username: str,
        password: str,
        expected_error: str
    ):
        """
        Parameterized test for multiple login failure scenarios.
        
        Best Practice: Data-driven testing to cover multiple scenarios efficiently
        
        Args:
            username: Username to test
            password: Password to test
            expected_error: Expected error message substring
        
        Expected Result: Appropriate error message is displayed for each scenario
        """
        # Act
        await saucedemo_login_page.login(username, password)
        
        # Assert
        await saucedemo_login_page.assert_error_message_displayed()
        await saucedemo_login_page.assert_error_message_contains(expected_error)
    
    @pytest.mark.smoke
    @pytest.mark.asyncio
    async def test_login_page_elements_visibility(
        self, 
        saucedemo_login_page: SauceDemoLoginPage
    ):
        """
        Test that all required login page elements are visible.
        
        Best Practice: Verify page state before performing actions
        
        Expected Result: All login form elements are visible
        """
        # Assert - fixture already navigates to page
        await saucedemo_login_page.assert_on_login_page()
        
        # Verify page title
        page_title = await saucedemo_login_page.get_page_title()
        assert page_title == "Swag Labs", f"Expected 'Swag Labs' but got '{page_title}'"
    
    @pytest.mark.regression
    @pytest.mark.asyncio
    async def test_logged_in_user_fixture(
        self, 
        logged_in_saucedemo: SauceDemoLoginPage
    ):
        """
        Test using the logged_in_saucedemo fixture.
        
        Best Practice: Demonstrates reusable fixtures for common test setup
        This fixture logs in the user automatically, saving time in tests
        that need to start from logged-in state.
        
        Expected Result: User is already logged in via fixture
        """
        # Assert - user should already be logged in via fixture
        await logged_in_saucedemo.assert_login_successful()
        assert await logged_in_saucedemo.is_login_successful()
        
        products_title = await logged_in_saucedemo.get_products_title()
        assert products_title == "Products"


class TestSauceDemoLoginPerformance:
    """
    Performance-related tests for login functionality.
    
    Best Practice: Separate performance tests from functional tests
    """
    
    @pytest.mark.regression
    @pytest.mark.asyncio
    async def test_login_page_loads_within_timeout(
        self, 
        page: Page, 
        saucedemo_url: str
    ):
        """
        Test that login page loads within acceptable timeout.
        
        Best Practice: Performance validation
        
        Expected Result: Page loads successfully within 5 seconds
        """
        # Act & Assert
        sauce_page = SauceDemoLoginPage(page, saucedemo_url)
        await sauce_page.navigate()
        
        # Verify page loaded
        await sauce_page.assert_on_login_page()
