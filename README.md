# Playwright Python Automation Framework

A comprehensive Playwright automation framework demonstrating advanced OOP principles and best practices.

## 🎯 OOP Principles Demonstrated

### 1. **Polymorphism**
Same method name, different behaviors across pages.
- `AdminLoginPage.login()` - requires username, password, and domain
- `ClientLoginPage.login()` - requires email, password, and optional remember_me

**Example:**
```python
# Admin login
await admin_login_page.login(username, password, domain="admin")

# Client login  
await client_login_page.login(email, password, remember_me=True)
```

### 2. **Encapsulation**
Selectors and internal logic are hidden inside page classes.
- Private selectors (prefixed with `_`)
- Internal implementation details hidden from tests
- Tests only call public methods

**Example:**
```python
# Test doesn't know about internal selectors
await home_page.open_menu()  # Selector is hidden inside the class
```

### 3. **Abstraction**
High-level methods that represent complex actions.
- `complete_checkout()` - performs multiple internal steps
- `add_product_to_cart()` - encapsulates product selection logic

**Example:**
```python
await checkout_page.complete_checkout(shipping_info, payment_info)
# Internally handles: form filling, method selection, validation, submission
```

### 4. **Inheritance**
Base classes provide common functionality to child classes.
- `BasePage` - common methods for all pages
- `LoginBasePage` - common login functionality
- All pages inherit `wait_for_page_load()`, assertions, etc.

**Example:**
```python
class HomePage(BasePage):  # Inherits all BasePage methods
    async def navigate(self):
        await self._page.goto(f"{self._base_url}/")
        await self.wait_for_page_load()  # Inherited method
```

### 5. **Design Patterns - Page Object Model (POM)**
Tests interact with page objects, not directly with UI elements.
- `LoginPage`, `HomePage`, `CheckoutPage`, `DashboardPage`
- Clean separation between test logic and page logic

**Example:**
```python
# Test uses page objects
await home_page.search_product("Laptop")
await home_page.add_to_cart("Laptop")
# NOT: await page.click("#search-button")
```

### 6. **Fixtures / Dependency Injection**
Playwright auto-injects fixtures; custom fixtures provide page objects.
- Built-in: `page`, `context`, `browser`
- Custom: `home_page`, `admin_login_page`, `logged_in_admin`

**Example:**
```python
async def test_example(home_page: HomePage):  # Injected by fixture
    await home_page.navigate()
```

### 7. **Asynchronous Programming**
All Playwright operations are async.
- `async def` for test methods and page methods
- `await` for all Playwright operations

**Example:**
```python
async def test_async_flow(self, home_page: HomePage):
    await home_page.navigate()
    await home_page.search_product("Phone")
```

### 8. **Clean Code**
Small methods, clear names, separated responsibilities.
- Single Responsibility Principle
- Descriptive method names
- Organized file structure

**Example:**
```python
# Instead of this in tests:
# await page.fill("#search", "Laptop")
# await page.click("#search-btn")
# await page.wait_for_selector(".products")

# We do this:
await home_page.search_product("Laptop")
```

### 9. **Assertions (Validations)**
Comprehensive validation methods in BasePage.
- `assert_url_contains()` - URL validation
- `assert_element_visible()` - visibility check
- `assert_element_has_text()` - exact text match
- `assert_element_contains_text()` - partial text match
- `assert_element_has_attribute()` - attribute validation
- `assert_element_count()` - element count validation

**Example:**
```python
await home_page.assert_url_contains("/home")
await home_page.assert_element_visible(".cart-icon")
await home_page.assert_cart_count(3)
```

## 📁 Project Structure

```
playwright-python-automation/
├── pages/
│   ├── __init__.py
│   ├── base_page.py              # Base class with common methods
│   ├── login_base_page.py        # Abstract login base class
│   ├── admin_login_page.py       # Admin-specific login
│   ├── client_login_page.py      # Client-specific login
│   ├── home_page.py              # Home page object
│   ├── checkout_page.py          # Checkout page object
│   └── dashboard_page.py         # Dashboard page object
├── tests/
│   ├── __init__.py
│   ├── test_login_polymorphism.py       # Polymorphism examples
│   ├── test_encapsulation_abstraction.py # Encapsulation & Abstraction
│   ├── test_inheritance.py              # Inheritance examples
│   ├── test_assertions.py               # Assertion examples
│   ├── test_fixtures.py                 # Fixture examples
│   ├── test_async_programming.py        # Async examples
│   └── test_end_to_end.py              # Complete E2E flows
├── conftest.py                   # Pytest fixtures
├── pytest.ini                    # Pytest configuration
├── requirements.txt              # Dependencies
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env`:
```
BASE_URL=https://your-app-url.com
ADMIN_USERNAME=admin@example.com
ADMIN_PASSWORD=admin123
CLIENT_USERNAME=client@example.com
CLIENT_PASSWORD=client123
TIMEOUT=30000
```

## 🧪 Running Tests

### Run all tests:
```bash
pytest
```

### Run specific test file:
```bash
pytest tests/test_login_polymorphism.py
```

### Run with specific markers:
```bash
pytest -m smoke           # Run only smoke tests
pytest -m regression      # Run only regression tests
pytest -m admin          # Run only admin tests
```

### Run in headless mode:
```bash
pytest --headed=false
```

### Run with different browser:
```bash
pytest --browser=firefox
pytest --browser=webkit
```

### Run with HTML report:
```bash
pytest --html=report.html --self-contained-html
```

## 📝 Test Examples

### Polymorphism Example
```python
# Admin login requires domain
await admin_login_page.login(username, password, domain="admin")

# Client login has remember_me option
await client_login_page.login(email, password, remember_me=True)
```

### Abstraction Example
```python
# One method call completes entire checkout
await checkout_page.complete_checkout(
    shipping_info=shipping_data,
    payment_info=payment_data,
    shipping_method="express"
)
```

### Fixture Injection Example
```python
async def test_with_logged_in_user(logged_in_admin: AdminLoginPage):
    # User is already logged in via fixture
    await logged_in_admin.assert_login_successful()
```

### Assertions Example
```python
await home_page.assert_url_contains("/home")
await home_page.assert_element_visible(".product-card")
await home_page.assert_cart_count(3)
await checkout_page.assert_order_successful()
```

## 🎓 Learning Points

1. **Polymorphism**: Look at `AdminLoginPage` vs `ClientLoginPage` - same `login()` method, different implementations
2. **Encapsulation**: Check how selectors are private (`_SELECTOR`) and tests never access them directly
3. **Abstraction**: See `complete_checkout()` - one method hides complex multi-step process
4. **Inheritance**: All pages inherit from `BasePage`, getting common methods for free
5. **POM**: Tests use page objects (`home_page.add_to_cart()`) instead of direct selectors
6. **Fixtures**: Tests receive ready-to-use objects via dependency injection
7. **Async**: All operations use `async`/`await` properly
8. **Clean Code**: Small, focused methods with clear names
9. **Assertions**: Built-in validation methods for all common checks

## 📚 Key Files to Study

1. **`pages/base_page.py`** - Understand inheritance and common methods
2. **`pages/login_base_page.py`** - See abstract base class for polymorphism
3. **`pages/admin_login_page.py` & `pages/client_login_page.py`** - Polymorphism in action
4. **`pages/checkout_page.py`** - Abstraction with `complete_checkout()`
5. **`conftest.py`** - Fixture definitions and dependency injection
6. **`tests/test_end_to_end.py`** - All principles working together

## 🔧 Customization

To adapt this framework for your application:

1. Update selectors in page objects to match your app's HTML
2. Modify `.env` with your application URL and credentials
3. Add new page objects following the existing pattern
4. Extend `BasePage` with additional common methods
5. Create fixtures for your specific test scenarios

## 📖 Best Practices

✅ **DO:**
- Keep page objects focused on single pages
- Use descriptive method names
- Leverage inheritance for common functionality
- Write small, focused methods
- Use assertions to validate behavior
- Inject dependencies via fixtures

❌ **DON'T:**
- Access selectors directly in tests
- Put test logic in page objects
- Create large, monolithic methods
- Hardcode test data
- Skip assertions

## 🤝 Contributing

This is a reference implementation. Feel free to adapt and extend for your needs!

## 📄 License

MIT License - feel free to use and modify.
