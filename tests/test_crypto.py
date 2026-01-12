from playwright_setup import launch_browser
from pages.metamask_page import MetaMaskPage
from pages.project_page import ProjectPage
from config.config import METAMASK_PASSWORD, ETHEREARL_URL, METAMASK_URL, SEED_WORDS1, SEED_WORDS2, SEED_WORDS3, SEED_WORDS4, SEED_WORDS5, SEED_WORDS6, SEED_WORDS7, SEED_WORDS8, SEED_WORDS9, SEED_WORDS10, SEED_WORDS11
import time

def setup(i=0, multiple=True):
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
    for idx in range(min(2, len(browser.pages))):
        time.sleep(1)
        browser.pages[idx].close()
    metamask_tab.reload()
    page = metamask_tab
    #page.pause()
    # Import wallet
    metamask = MetaMaskPage(page)
    SEED_WORDS_LIST = [
        SEED_WORDS1,
        SEED_WORDS2,
        SEED_WORDS3,
        SEED_WORDS4,
        SEED_WORDS5,
        SEED_WORDS6,
        SEED_WORDS7,
        SEED_WORDS8,
        SEED_WORDS9,
        SEED_WORDS10,
        SEED_WORDS11,
    ]
    print(SEED_WORDS_LIST[i])
    if multiple:
       print("Muliple")
       #metamask.import_wallet(SEED_WORDS1, METAMASK_PASSWORD)
       #metamask.import_wallet(f'SEED_WORDS{i}', METAMASK_PASSWORD)
       print(SEED_WORDS_LIST[i])
       metamask.import_wallet(SEED_WORDS_LIST[i], METAMASK_PASSWORD)
       wallet_address = metamask.get_wallet_address()
       print("Wallet Address:", wallet_address)
    else:
       print("Not Muliple")
       #metamask.import_wallet(METAMASK_PASSWORD, SEED_WORDS=seed_words)
       metamask.import_wallet(SEED_WORDS_LIST[0], METAMASK_PASSWORD)
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

def testnet_rise():
    """Test case for Project-2 flow."""
    playwright, browser, page = setup()
    project2 = ProjectPage(page)
    # Navigate to Project-1
    page.goto("https://gaspump.network/swap")
    project2.testnet_rise()
    teardown(playwright, browser)

def testnet_arc_network():
    """Test case for Arc Network flow."""

    for i in range(0, 11):
        print(i)
        playwright, browser, page = setup(i)
        project = ProjectPage(page)
        # Navigate to Page
        #page.goto("https://faucet.circle.com/")
        #page.pause()
        page.goto("https://www.xylonet.xyz/")
        project.testnet_arc_network()
        print("-----Completed Wallet------>", i)
        teardown(playwright, browser)

if __name__ == "__main__":
    #testnet_ethereal_trade()
    #testnet_rise()
    testnet_arc_network()