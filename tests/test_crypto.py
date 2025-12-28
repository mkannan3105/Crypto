from playwright_setup import launch_browser
from pages.metamask_page import MetaMaskPage
from pages.project_page import ProjectPage
from config.config import SEED_WORDS, METAMASK_PASSWORD, ETHEREARL_URL, METAMASK_URL
import time

def setup():
    """Setup browser and import wallet."""
    playwright, browser = launch_browser()
    # Wait for MetaMask tab to open automatically
    metamask_tab = browser.wait_for_event("page")
    if "chrome-extension://" not in metamask_tab.url:
        raise Exception("MetaMask extension did not load. Check EXTENSION_PATH!")

    print("MetaMask Loaded:", metamask_tab.url)
    page = browser.new_page()
    # Open MetaMask onboarding page
    #page.goto(METAMASK_URL)
    # Close initial default tabs if open
    for i in range(min(2, len(browser.pages))):
        time.sleep(1)
        browser.pages[i].close()
    metamask_tab.reload()
    page = metamask_tab
    # Import wallet
    metamask = MetaMaskPage(page)
    metamask.import_wallet(SEED_WORDS, METAMASK_PASSWORD)
    wallet_address = metamask.get_wallet_address()
    print("Wallet Address:", wallet_address)
    # page.pause()
    return playwright, browser, page

def teardown(playwright, browser):
    """Cleanup resources."""
    browser.close()
    playwright.stop()

def testnet_ethereal_trade():
    """Test case for Project-1 flow."""
    playwright, browser, page = setup()

    # Navigate to Project-1
    page.goto(ETHEREARL_URL)
    project1 = ProjectPage(page)
    project1.ethereal_trade()
    teardown(playwright, browser)

if __name__ == "__main__":
    testnet_ethereal_trade()