from playwright_setup import launch_browser
from pages.metamask_page import MetaMaskPage
from pages.project_page import ProjectPage
from config.config import (METAMASK_PASSWORD,ETHEREARL_URL,METAMASK_URL,SEED_WORDS1, SEED_WORDS2, SEED_WORDS3, SEED_WORDS4, SEED_WORDS5, SEED_WORDS6, SEED_WORDS7, SEED_WORDS8, SEED_WORDS9, SEED_WORDS10, SEED_WORDS11, SEED_WORDS12, SEED_WORDS13, SEED_WORDS14, SEED_WORDS15, SEED_WORDS16, SEED_WORDS17, SEED_WORDS18, SEED_WORDS19, SEED_WORDS20, SEED_WORDS21, SEED_WORDS22, SEED_WORDS23, SEED_WORDS24, SEED_WORDS25, SEED_WORDS26, SEED_WORDS27, SEED_WORDS28, SEED_WORDS29, SEED_WORDS30, SEED_WORDS31, SEED_WORDS32, SEED_WORDS33, SEED_WORDS34, SEED_WORDS35, SEED_WORDS36, SEED_WORDS37, SEED_WORDS38, SEED_WORDS39, SEED_WORDS40, SEED_WORDS41, SEED_WORDS42, SEED_WORDS43, SEED_WORDS44, SEED_WORDS45, SEED_WORDS46, SEED_WORDS47, SEED_WORDS48, SEED_WORDS49, SEED_WORDS50, SEED_WORDS51, SEED_WORDS52, SEED_WORDS53, SEED_WORDS54, SEED_WORDS55, SEED_WORDS56, SEED_WORDS57, SEED_WORDS58, SEED_WORDS59, SEED_WORDS60, SEED_WORDS61, SEED_WORDS62, SEED_WORDS63, SEED_WORDS64, SEED_WORDS65, SEED_WORDS66, SEED_WORDS67, SEED_WORDS68, SEED_WORDS69, SEED_WORDS70, SEED_WORDS71, SEED_WORDS72, SEED_WORDS73, SEED_WORDS74, SEED_WORDS75,SEED_WORDS76, SEED_WORDS77, SEED_WORDS78, SEED_WORDS79, SEED_WORDS80,SEED_WORDS81, SEED_WORDS82, SEED_WORDS83, SEED_WORDS84, SEED_WORDS85,SEED_WORDS86, SEED_WORDS87, SEED_WORDS88, SEED_WORDS89, SEED_WORDS90,SEED_WORDS91, SEED_WORDS92, SEED_WORDS93, SEED_WORDS94, SEED_WORDS95,SEED_WORDS96, SEED_WORDS97, SEED_WORDS98, SEED_WORDS99, SEED_WORDS100,SEED_WORDS101, SEED_WORDS102, SEED_WORDS103, SEED_WORDS104, SEED_WORDS105,SEED_WORDS106, SEED_WORDS107, SEED_WORDS108, SEED_WORDS109, SEED_WORDS110,SEED_WORDS111, SEED_WORDS112, SEED_WORDS113, SEED_WORDS114, SEED_WORDS115,SEED_WORDS116, SEED_WORDS117, SEED_WORDS118, SEED_WORDS119, SEED_WORDS120,SEED_WORDS121, SEED_WORDS122, SEED_WORDS123, SEED_WORDS124, SEED_WORDS125,SEED_WORDS126, SEED_WORDS127, SEED_WORDS128, SEED_WORDS129, SEED_WORDS130,SEED_WORDS131, SEED_WORDS132, SEED_WORDS133, SEED_WORDS134, SEED_WORDS135,SEED_WORDS136, SEED_WORDS137, SEED_WORDS138, SEED_WORDS139, SEED_WORDS140,SEED_WORDS141, SEED_WORDS142, SEED_WORDS143, SEED_WORDS144, SEED_WORDS145,SEED_WORDS146, SEED_WORDS147, SEED_WORDS148, SEED_WORDS149, SEED_WORDS150,SEED_WORDS151, SEED_WORDS152, SEED_WORDS153, SEED_WORDS154, SEED_WORDS155,SEED_WORDS156, SEED_WORDS157, SEED_WORDS158, SEED_WORDS159, SEED_WORDS160,SEED_WORDS161, SEED_WORDS162, SEED_WORDS163, SEED_WORDS164, SEED_WORDS165,SEED_WORDS166, SEED_WORDS167, SEED_WORDS168, SEED_WORDS169, SEED_WORDS170,SEED_WORDS171, SEED_WORDS172, SEED_WORDS173, SEED_WORDS174, SEED_WORDS175,SEED_WORDS176, SEED_WORDS177, SEED_WORDS178, SEED_WORDS179, SEED_WORDS180)

import time

def setup(i=0, multiple=True):
    """Setup browser and import wallet."""
    playwright, browser = launch_browser()
    # Wait for MetaMask tab to open automatically
    metamask_tab = browser.wait_for_event("page")
    if "chrome-extension://" not in metamask_tab.url:
        raise Exception("MetaMask extension did not load. Check EXTENSION_PATH!")

    #print("MetaMask Loaded:", metamask_tab.url)
    page = browser.new_page()
    # Open MetaMask onboarding page
    #page.goto(METAMASK_URL)
    # Close initial default tabs if open
    for idx in range(min(2, len(browser.pages))):
        time.sleep(1)
        browser.pages[idx].close()
    metamask_tab.reload()
    page = metamask_tab
    # Import wallet
    metamask = MetaMaskPage(page)
    SEED_WORDS_LIST = [SEED_WORDS1, SEED_WORDS2, SEED_WORDS3, SEED_WORDS4, SEED_WORDS5,SEED_WORDS6, SEED_WORDS7, SEED_WORDS8, SEED_WORDS9, SEED_WORDS10,SEED_WORDS11, SEED_WORDS12, SEED_WORDS13, SEED_WORDS14, SEED_WORDS15,SEED_WORDS16, SEED_WORDS17, SEED_WORDS18, SEED_WORDS19, SEED_WORDS20,SEED_WORDS21, SEED_WORDS22, SEED_WORDS23, SEED_WORDS24, SEED_WORDS25,SEED_WORDS26, SEED_WORDS27, SEED_WORDS28, SEED_WORDS29, SEED_WORDS30,SEED_WORDS31, SEED_WORDS32, SEED_WORDS33, SEED_WORDS34, SEED_WORDS35,SEED_WORDS36, SEED_WORDS37, SEED_WORDS38, SEED_WORDS39, SEED_WORDS40,SEED_WORDS41, SEED_WORDS42, SEED_WORDS43, SEED_WORDS44, SEED_WORDS45,SEED_WORDS46, SEED_WORDS47, SEED_WORDS48, SEED_WORDS49, SEED_WORDS50,SEED_WORDS51, SEED_WORDS52, SEED_WORDS53, SEED_WORDS54, SEED_WORDS55,SEED_WORDS56, SEED_WORDS57, SEED_WORDS58, SEED_WORDS59, SEED_WORDS60,SEED_WORDS61, SEED_WORDS62, SEED_WORDS63, SEED_WORDS64, SEED_WORDS65,SEED_WORDS66, SEED_WORDS67, SEED_WORDS68, SEED_WORDS69, SEED_WORDS70,SEED_WORDS71, SEED_WORDS72, SEED_WORDS73, SEED_WORDS74, SEED_WORDS75,SEED_WORDS76, SEED_WORDS77, SEED_WORDS78, SEED_WORDS79, SEED_WORDS80,SEED_WORDS81, SEED_WORDS82, SEED_WORDS83, SEED_WORDS84, SEED_WORDS85,SEED_WORDS86, SEED_WORDS87, SEED_WORDS88, SEED_WORDS89, SEED_WORDS90,SEED_WORDS91, SEED_WORDS92, SEED_WORDS93, SEED_WORDS94, SEED_WORDS95,SEED_WORDS96, SEED_WORDS97, SEED_WORDS98, SEED_WORDS99, SEED_WORDS100,SEED_WORDS101, SEED_WORDS102, SEED_WORDS103, SEED_WORDS104, SEED_WORDS105,SEED_WORDS106, SEED_WORDS107, SEED_WORDS108, SEED_WORDS109, SEED_WORDS110,SEED_WORDS111, SEED_WORDS112, SEED_WORDS113, SEED_WORDS114, SEED_WORDS115,SEED_WORDS116, SEED_WORDS117, SEED_WORDS118, SEED_WORDS119, SEED_WORDS120,SEED_WORDS121, SEED_WORDS122, SEED_WORDS123, SEED_WORDS124, SEED_WORDS125,SEED_WORDS126, SEED_WORDS127, SEED_WORDS128, SEED_WORDS129, SEED_WORDS130,SEED_WORDS131, SEED_WORDS132, SEED_WORDS133, SEED_WORDS134, SEED_WORDS135,SEED_WORDS136, SEED_WORDS137, SEED_WORDS138, SEED_WORDS139, SEED_WORDS140,SEED_WORDS141, SEED_WORDS142, SEED_WORDS143, SEED_WORDS144, SEED_WORDS145,SEED_WORDS146, SEED_WORDS147, SEED_WORDS148, SEED_WORDS149, SEED_WORDS150,SEED_WORDS151, SEED_WORDS152, SEED_WORDS153, SEED_WORDS154, SEED_WORDS155,SEED_WORDS156, SEED_WORDS157, SEED_WORDS158, SEED_WORDS159, SEED_WORDS160,SEED_WORDS161, SEED_WORDS162, SEED_WORDS163, SEED_WORDS164, SEED_WORDS165,SEED_WORDS166, SEED_WORDS167, SEED_WORDS168, SEED_WORDS169, SEED_WORDS170,SEED_WORDS171, SEED_WORDS172, SEED_WORDS173, SEED_WORDS174, SEED_WORDS175,SEED_WORDS176, SEED_WORDS177, SEED_WORDS178, SEED_WORDS179, SEED_WORDS180]
    print(SEED_WORDS_LIST[i])
    #try:
    #     if multiple:
    #        metamask.import_wallet(SEED_WORDS_LIST[i], METAMASK_PASSWORD)
    #        wallet_address = metamask.get_wallet_address()
    #        print("Wallet Address:", wallet_address)
    #except:
    #      print("Wallet failed", i)
    if multiple:
       #metamask.import_wallet(SEED_WORDS1, METAMASK_PASSWORD)
       #metamask.import_wallet(f'SEED_WORDS{i}', METAMASK_PASSWORD)
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
    for i in range(134, 180):
        playwright, browser, page = setup(i)
        project = ProjectPage(page)
        try:
           # Navigate to Page
           #page.goto("https://faucet.circle.com/")
           #page.pause()
           page.goto("https://www.xylonet.xyz/points?ref=REF6AC9B3A6")
           project.testnet_arc_network()
           print("-----Completed Wallet------>", i)
           teardown(playwright, browser)
        except:
           print("Wallet is failed", i)
           teardown(playwright, browser)

def testnet_hotstuff_trade():
    """Test case for hot stuff trade."""
    for i in range(0, 180):
        playwright, browser, page = setup(i)
        project = ProjectPage(page)
        try:
           # Navigate to Page
           page.goto("https://testnet.hotstuff.trade/join/mkannan3105")
           project.testnet_hotstuff_trade()
           print("-----Completed Wallet------>", i)
           teardown(playwright, browser)
        except:
           print("Wallet is failed", i)
           teardown(playwright, browser)

def testnet_x1ecochain():
    """Test case for x1ecochain"""
    for i in range(22, 180):
        playwright, browser, page = setup(i)
        project = ProjectPage(page)
        try:
           # Navigate to Page
           page.goto("https://t.x1.one/?rcode=9Jd82wqL")
           project.testnet_x1ecochain()
           print("-----Completed Wallet------>", i)
           teardown(playwright, browser)
        except:
           print("Wallet is failed", i)
           teardown(playwright, browser)

def testnet_aixcrypto():
    """Test case for x1ecochain"""
    for i in range(1, 180):
        playwright, browser, page = setup(i)
        project = ProjectPage(page)
        try:
           # Navigate to Page
           page.goto("https://hub.aixcrypto.ai/?ref=04443264-f475-4b94-9b28-11db44ac57d7")
           project.testnet_aixcrypto()
           page.pause()
           print("-----Completed Wallet------>", i)
           teardown(playwright, browser)
        except:
           print("Wallet is failed", i)
           teardown(playwright, browser)

if __name__ == "__main__":
    #testnet_ethereal_trade()
    #testnet_rise()
    testnet_arc_network()
    #testnet_hotstuff_trade()
    #testnet_x1ecochain()
    #testnet_aixcrypto()

