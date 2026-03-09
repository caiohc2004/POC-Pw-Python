import os
from dotenv import load_dotenv
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path, override=True)

username = os.getenv('SR_USERNAME')
password = os.getenv('SR_PASSWORD')

def test_login_valid_credentials(): 
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://front.serverest.dev/login")

        page.get_by_placeholder('Digite seu email').fill(username)
        page.get_by_placeholder('Digite sua senha').fill(password)
        page.get_by_text('Entrar').click()

        # Expect some element that indicates successful login
        expect(page.get_by_text("Serverest Store")).to_be_visible()
        
        page.wait_for_timeout(5000)
        
        browser.close()

def test_login_invalid_username():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://front.serverest.dev/login")

        page.get_by_placeholder('Digite seu email').fill("wrong@example.com")
        page.get_by_placeholder('Digite sua senha').fill(password)
        page.get_by_text('Entrar').click()

        # Expect error message
        expect(page.get_by_text("Email e/ou senha inválidos")).to_be_visible()
        
        page.wait_for_timeout(5000)
        
        browser.close()

def test_login_invalid_password():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://front.serverest.dev/login")

        page.get_by_placeholder('Digite seu email').fill(username)
        page.get_by_placeholder('Digite sua senha').fill("wrongpassword")
        page.get_by_text('Entrar').click()

        expect(page.get_by_text("Email e/ou senha inválidos")).to_be_visible()
        
        page.wait_for_timeout(5000)
        
        browser.close()

def test_login_message_empty_fields():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://front.serverest.dev/login")

        page.get_by_text('Entrar').click()
        
        
        # Expect validation message
        expect(page.get_by_text("Email não pode ficar em branco")).to_be_visible()
        expect(page.get_by_text("Password não pode ficar em branco")).to_be_visible()
        
        page.wait_for_timeout(5000)
        
        browser.close()