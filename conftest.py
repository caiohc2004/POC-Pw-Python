import pytest
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from pages.admin_login_page import AdminLoginPage
from pages.client_login_page import ClientLoginPage
from pages.home_page import HomePage
from pages.checkout_page import CheckoutPage
from pages.dashboard_page import DashboardPage
# from pages.saucedemo_login_page import SauceDemoLoginPage  # Temporarily disabled
from dotenv import load_dotenv
import os

load_dotenv()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Fixture providing the base URL for the application."""
    return os.getenv("BASE_URL", "https://opensource-demo.orangehrmlive.com")


@pytest.fixture(scope="session")
def admin_credentials() -> dict:
    """Fixture providing OrangeHRM admin credentials."""
    return {
        "username": os.getenv("ORANGE_USERNAME", "Admin"),
        "password": os.getenv("ORANGE_PASSWORD", "admin123")
    }


@pytest.fixture(scope="session")
def client_credentials() -> dict:
    """Fixture providing client credentials."""
    return {
        "username": os.getenv("CLIENT_USERNAME", "client@example.com"),
        "password": os.getenv("CLIENT_PASSWORD", "client123")
    }


@pytest.fixture
async def async_page():
    """Async browser page fixture that replaces pytest-playwright's sync page."""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=False, slow_mo=500)
        context = await browser.new_context()
        page = await context.new_page()
        yield page
        await context.close()
        await browser.close()


@pytest.fixture
async def admin_login_page(async_page: Page, base_url: str) -> AdminLoginPage:
    """Fixture providing an initialized AdminLoginPage instance."""
    admin_page = AdminLoginPage(async_page, base_url)
    await admin_page.navigate()
    return admin_page


@pytest.fixture
async def client_login_page(async_page: Page, base_url: str) -> ClientLoginPage:
    """Fixture providing an initialized ClientLoginPage instance."""
    client_page = ClientLoginPage(async_page, base_url)
    await client_page.navigate()
    return client_page


@pytest.fixture
async def home_page(async_page: Page, base_url: str) -> HomePage:
    """Fixture providing an initialized HomePage instance."""
    return HomePage(async_page, base_url)


@pytest.fixture
async def checkout_page(page: Page, base_url: str) -> CheckoutPage:
    """Fixture providing an initialized CheckoutPage instance."""
    return CheckoutPage(page, base_url)


@pytest.fixture
async def dashboard_page(page: Page, base_url: str) -> DashboardPage:
    """Fixture providing an initialized DashboardPage instance."""
    return DashboardPage(page, base_url)


@pytest.fixture
async def logged_in_admin(admin_login_page: AdminLoginPage, admin_credentials: dict) -> AdminLoginPage:
    """Fixture that provides a page with admin already logged in."""
    await admin_login_page.login(admin_credentials["username"], admin_credentials["password"])
    await admin_login_page.wait_for_page_load()
    return admin_login_page


@pytest.fixture
async def logged_in_client(client_login_page: ClientLoginPage, client_credentials: dict) -> ClientLoginPage:
    """Fixture that provides a page with client already logged in."""
    await client_login_page.login(client_credentials["username"], client_credentials["password"])
    await client_login_page.wait_for_page_load()
    return client_login_page


@pytest.fixture(scope="session")
def saucedemo_url() -> str:
    """Fixture providing the SauceDemo URL."""
    return os.getenv("SAUCEDEMO_URL", "https://www.saucedemo.com")


@pytest.fixture(scope="session")
def saucedemo_credentials() -> dict:
    """Fixture providing SauceDemo credentials."""
    return {
        "username": os.getenv("SAUCE_USERNAME", "standard_user"),
        "password": os.getenv("SAUCE_PASSWORD", "secret_sauce")
    }


# @pytest.fixture
# async def saucedemo_login_page(page: Page, saucedemo_url: str) -> SauceDemoLoginPage:
#     """Fixture providing an initialized SauceDemoLoginPage instance."""
#     sauce_page = SauceDemoLoginPage(page, saucedemo_url)
#     await sauce_page.navigate()
#     return sauce_page


# @pytest.fixture
# async def logged_in_saucedemo(saucedemo_login_page: SauceDemoLoginPage, saucedemo_credentials: dict) -> SauceDemoLoginPage:
#     """Fixture that provides a page with user already logged into SauceDemo."""
#     await saucedemo_login_page.login(saucedemo_credentials["username"], saucedemo_credentials["password"])
#     await saucedemo_login_page.assert_login_successful()
#     return saucedemo_login_page
