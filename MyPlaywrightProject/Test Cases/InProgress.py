import os
from dotenv import load_dotenv
from playwright.sync_api import Page, expect
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

# Load environment variables from .env file
# Get the path to the .env file (located at the root of Pw_Python_FromZero)
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

# Get credentials from environment variables
username = os.getenv('SR_USERNAME')
password = os.getenv('SR_PASSWORD')


# Debug: print to verify credentials are loaded
print(f"Loaded username: {username}")
#print(f"Loaded password: {password}")

#def test_login_with_env(page: Page):

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://front.serverest.dev/login")
    
    page.wait_for_timeout(500)
    page.get_by_placeholder('Digite seu email').fill(username)
    page.get_by_placeholder('Digite sua senha').fill(password)
    page.get_by_text('Entrar').click()
    
    
    
    
    page.pause()
    
    
    
