import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, expect
from pathlib import Path

# Load environment variables from .env file
# Get the path to the .env file (located at the root of Pw_Python_FromZero)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Get credentials from environment variables
username = os.getenv('SAUCE_USERNAME')
password = os.getenv('SAUCE_PASSWORD')

# Debug: print to verify credentials are loaded
print(f"Loaded username: {username}")
print(f"Loaded password: {password}")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.saucedemo.com/")
        
        page.wait_for_timeout(500)
        page.locator("[data-test='username']").fill(username)
        page.locator("[data-test='password']").fill(password)
        page.locator("[data-test='login-button']").click()
        
        # Wait to verify login success
        page.wait_for_timeout(1000)
        
        # Verify we're on the products page
        if page.locator(".inventory_container").is_visible():
            print("Login successful!")
            products_title = page.locator(".title").text_content()
            print(f"Page title: {products_title}")
        else:
            print("Login failed!")
            if page.locator("[data-test='error']").is_visible():
                error_msg = page.locator("[data-test='error']").text_content()
                print(f"Error: {error_msg}")
        
        page.pause()
