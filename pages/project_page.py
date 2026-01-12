import locators.project_locators as ethereal
import locators.project_locators as ethereal
from playwright.sync_api import expect
import time
import re

class ProjectPage:
    def __init__(self, page):
        self.page = page

    def wallet_connect_pop(self):
        # Handle MetaMask connection popup
        time.sleep(1)
        popup = self.page.context.wait_for_event("page")
        popup.wait_for_load_state()
        popup.wait_for_selector("//*[@data-testid='confirm-btn']", timeout=30000)
        popup.get_by_test_id("confirm-btn").click()
        popup.close()

    def wallet_confirmation_pop(self):
         # Confirm MetaMask transaction
         popup = self.page.context.wait_for_event("page")
         popup.wait_for_load_state()
         popup.wait_for_selector("[data-testid='confirm-footer-button']", timeout=30000)
         popup.locator("[data-testid='confirm-footer-button']").click()
         #popup.locator("//*[text()='Confirm']").click()
         popup.close()

    def wallet_confirmation_next_pop(self):
         # Confirm MetaMask transaction
         popup = self.page.context.wait_for_event("page")
         popup.wait_for_load_state()
         popup.wait_for_selector("[data-testid='page-container-footer-next']", timeout=30000)
         popup.locator("[data-testid='page-container-footer-next']").click()
         popup.close()

    def wallet_approve_pop(self):
         # Handle transaction confirmation popup
         popup = self.page.context.wait_for_event("page")
         popup.wait_for_selector("[data-testid='confirmation-submit-button']", timeout=30000)
         popup.locator("[data-testid='confirmation-submit-button']").click()
         #popup.close()

    def ethereal_trade(self):
        """Click Connect and select MetaMask."""
        # Click Connect > MetaMask to trigger wallet popup
        self.page.locator(ethereal.CONNECT_BTN).nth(1).click()
        self.page.locator(ethereal.METAMASK_BTN).click()
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        # Handle transaction approve popup
        self.wallet_approve_pop()
        # Click the first checkbox (Terms of Use)
        # page.locator("text=I confirm that I have read, understood and accepted").click()
        # Click the second checkbox (Cookies policy)
        # page.locator("text=This site uses cookies to enhance your browsing").click()
        # Now click the "Agree & Continue" button
        # page.get_by_role("button", name="Agree & Continue").click()
        for i in range(1):
            # Enter order size
            self.page.get_by_role("textbox", name="Size").click()
            self.page.get_by_role("textbox", name="Size").fill("0.0001")
            # Place Long Order
            self.page.locator(ethereal.PLACE_ORDER_BTN).click()
            self.page.locator(ethereal.CONFIRM_ORDER_BTN).click()
            # Confirm MetaMask transaction
            self.wallet_confirmation_pop()
            # Switch to Short
            self.page.locator(ethereal.SHORT_TAB).click()
            self.page.locator(ethereal.PLACE_ORDER_BTN).click()
            self.page.locator(ethereal.CONFIRM_ORDER_BTN).click()
            # Confirm MetaMask transaction
            self.wallet_confirmation_pop()
            # Switch back to Long
            self.page.locator(ethereal.LONG_BTN).click()

    def testnet_rise(self):
        #self.page.pause()
        self.page.get_by_role("button", name="Connect a wallet").click()
        self.page.get_by_role("button", name="MetaMask Installed Wallet").click()
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        time.sleep(5)
        self.page.get_by_role("button").nth(1).click()
        self.page.get_by_test_id("connect-wallet-btn").click()
        # Handle transaction approve popup
        self.wallet_approve_pop()
        #time.sleep(5)
        #self.page.pause()
        self.page.get_by_role("button", name="WETH", exact=True).click()
        self.page.get_by_role("textbox", name="Enter the token symbol or").click()
        self.page.get_by_role("textbox", name="Enter the token symbol or").fill("USDT")
        self.page.get_by_test_id("token-picker-item").click()
        self.page.get_by_role("button", name="USDC").click()
        self.page.get_by_role("textbox", name="Enter the token symbol or").click()
        self.page.get_by_role("textbox", name="Enter the token symbol or").fill("WETH")
        self.page.get_by_test_id("token-picker-item").click()
        time.sleep(10)
        self.page.get_by_role("textbox", name="0.00").first.click()
        time.sleep(5)
        self.page.get_by_role("textbox", name="0.00").first.fill("0.1")
        time.sleep(5)
        self.page.get_by_test_id("swap-review-btn").click()
        self.page.pause()
        self.page.get_by_role("button", name="Confirm swap").click()
        self.page.pause()

    def testnet_arc_network(self):
        self.page.get_by_role("banner").get_by_test_id("rk-connect-button").click()
        self.page.get_by_test_id("rk-wallet-option-io.metamask").click()
        time.sleep(2)
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        time.sleep(3)
        # Handle transaction approve popup
        self.wallet_approve_pop()
        time.sleep(2)
        self.page.get_by_role("link", name="Launch App").click()
        self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(1).click()
        # Swap Amount
        amount_input = self.page.get_by_placeholder("0.00").first
        expect(amount_input).to_be_visible(timeout=30000)
        amount_input.fill("0.001")
        time.sleep(2)
        # Swap button
        #swap = self.page.locator(ethereal.ARC_SWAP_BTN)
        #swap.wait_for(state="attached", timeout=30000)
        #time.sleep(2)
        #self.page.locator(ethereal.ARC_SWAP_BTN).click()
        #time.sleep(3)
        self.page.evaluate("window.scrollBy(0, 500)")
        time.sleep(2)
        approve_eurc = self.page.get_by_role("button", name="Approve EURC")
        if approve_eurc.is_visible():
            self.page.get_by_role("button", name="Approve EURC").click()
            self.wallet_confirmation_pop()
            time.sleep(1)
            self.page.get_by_role("button", name="Swap").click()
        else:
            self.page.get_by_role("button", name="Swap").click()
            self.wallet_confirmation_pop()
        #self.page.evaluate("() => debugger")
        #self.page.pause()
        #approve_eurc = self.page.locator(ethereal.ARC_APPROVE_EURC_BTN)
        #approve_usdc = self.page.locator(ethereal.ARC_APPROVE_USDC_BTN)
        #if approve_eurc.is_visible():
        #    approve_eurc.click()
        #else:
        #    print("Commin else")
        #    self.page.locator(ethereal.ARC_SWAP_BTN).click()
        #time.sleep(2)
        #self.wallet_confirmation_pop()
        # Add Pools
        self.page.get_by_role("link", name="Pools").click()
        self.page.get_by_role("button", name="Add").click()
        self.page.get_by_placeholder("0.00").first.click()
        self.page.get_by_placeholder("0.00").first.fill("0.001")
        time.sleep(1)
        self.page.locator(ethereal.ACRC_LIQ_EURC).first.fill("0.0001")
        time.sleep(1)
        approve_eurc = self.page.locator(ethereal.ARC_APPROVE_EURC_BTN)
        approve_usdc = self.page.locator(ethereal.ARC_APPROVE_USDC_BTN)
        if approve_eurc.is_visible():
            approve_eurc.click()
            # Handle transaction approve popup
            self.wallet_confirmation_pop()
            time.sleep(2)
            button = self.page.get_by_role("button", name="Add Liquidity")
            button.click(timeout=20000)
        elif approve_usdc.is_visible():
            approve_usdc.click()
            # Handle transaction approve popup
            self.wallet_confirmation_pop()
            time.sleep(3)
            if approve_eurc.is_visible():
                approve_eurc.click()
                # Handle transaction approve popup
                self.wallet_confirmation_pop()
            button = self.page.get_by_role("button", name="Add Liquidity")
            button.click(timeout=20000)
        else:
            print("Neither Approve EURC nor Approve USDC button is visible")
            button = self.page.get_by_role("button", name="Add Liquidity")
            button.click(timeout=20000)
        time.sleep(1)
        # Handle transaction approve popup
        self.wallet_confirmation_pop()
        time.sleep(2)
        if button.is_visible():
            self.page.locator("//*[@class='text-gray-400']").click()
        # Bridge
        self.page.get_by_role("link", name="Bridge").click()
        amount = self.page.get_by_placeholder("0.00")
        amount.click()
        amount.fill("0.0001")
        time.sleep(2)

        bridge = self.page.get_by_role(
            "button", name="Bridge to Ethereum Sepolia"
        )

        # Wait until button is actually ready
        bridge.wait_for(state="visible", timeout=30000)
        self.page.evaluate("window.scrollBy(0, 500)")
        bridge.click()
        time.sleep(1)
        self.page.locator("//*[contains(text(), 'Bridge to ')]").click()
        time.sleep(3)
        # Handle transaction approve popup
        self.wallet_confirmation_pop()
        # Handle transaction approve popup
        self.wallet_confirmation_pop()
        # Handle transaction approve popup
        self.wallet_confirmation_next_pop()
        # Handle transaction approve popup
        self.wallet_confirmation_pop()
        """
        self.page.get_by_role("link", name="Vault").click()
        self.page.get_by_role("button", name="Deposit USDC").click()
        self.page.get_by_placeholder("0.00").click()
        self.page.get_by_placeholder("0.00").fill("0.01")
        #self.page.pause()
        approve_usdc = self.page.get_by_role("button", name="Approve USDC")
        if approve_usdc.is_visible():
            approve_usdc.click()
            # Handle transaction approve popup
            self.wallet_confirmation_pop()
            self.page.get_by_role("button", name="Deposit", exact=True).click()
            # Handle transaction approve popup
            self.wallet_confirmation_pop()
        else:
            self.page.get_by_role("button", name="Deposit", exact=True).click()
            # Handle transaction approve popup
            self.wallet_confirmation_pop()
        """