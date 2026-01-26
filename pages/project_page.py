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
        time.sleep(2)
        popup = self.page.context.wait_for_event("page")
        popup.wait_for_load_state()
        popup.wait_for_selector("//*[@data-testid='confirm-btn']", timeout=50000)
        popup.get_by_test_id("confirm-btn").click()
        popup.close()

    def wallet_confirmation_pop(self):
         time.sleep(2)
         # Confirm MetaMask transaction
         popup = self.page.context.wait_for_event("page")
         popup.wait_for_load_state()
         popup.wait_for_selector("[data-testid='confirm-footer-button']", timeout=50000)
         popup.locator("[data-testid='confirm-footer-button']").click()
         popup.close()

    def wallet_confirmation_next_pop(self):
         # Confirm MetaMask transaction
         time.sleep(2)
         popup = self.page.context.wait_for_event("page")
         popup.wait_for_load_state()
         popup.wait_for_selector("[data-testid='page-container-footer-next']", timeout=50000)
         popup.locator("[data-testid='page-container-footer-next']").click()
         popup.close()

    def wallet_approve_pop(self):
         # Handle transaction confirmation popup
         time.sleep(2)
         popup = self.page.context.wait_for_event("page")
         popup.wait_for_selector("[data-testid='confirmation-submit-button']", timeout=100000)
         popup.locator("[data-testid='confirmation-submit-button']").click()

    def ethereal_trade(self):
        """Click Connect and select MetaMask."""
        # Click Connect > MetaMask to trigger wallet popup
        self.page.locator(ethereal.CONNECT_BTN).nth(1).click()
        self.page.locator(ethereal.METAMASK_BTN).click()
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        # Handle transaction approve popup
        self.wallet_approve_pop()
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
        #self.page.get_by_role("link", name="Launch App").click()
        self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(1).click()
        # Swap Amount
        amount_input = self.page.get_by_placeholder("0.00").first
        expect(amount_input).to_be_visible(timeout=30000)
        amount_input.fill("0.01")
        time.sleep(2)
        self.page.evaluate("window.scrollBy(0, 500)")
        time.sleep(2)
        approve_eurc = self.page.get_by_role("button", name="Approve EURC")
        if approve_eurc.is_visible():
            self.page.get_by_role("button", name="Approve EURC").click()
            time.sleep(2)
            self.wallet_confirmation_pop()
            self.page.get_by_role("button", name="Swap").click()
            self.wallet_confirmation_pop()
        else:
            self.page.get_by_role("button", name="Swap").click()
            time.sleep(2)
            self.wallet_confirmation_pop()
        print("Swap successful")
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
        print("Pools Added Successful")
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
        print("Bridge Successful")
        # Vault
        self.page.get_by_role("link", name="Vault").click()
        self.page.get_by_role("button", name="Deposit USDC").click()
        self.page.get_by_placeholder("0.00").click()
        self.page.get_by_placeholder("0.00").fill("0.001")
        approve_usdc = self.page.get_by_role("button", name="Approve USDC")
        if approve_usdc.is_visible():
            approve_usdc.click()
            print("Add Amount")
            # Handle transaction approve popup
            self.wallet_confirmation_pop()
            time.sleep(5)
            self.page.get_by_role("button", name="Deposit", exact=True).click()
            # Handle transaction approve popup
            self.wallet_confirmation_pop()
        else:
            print("Add Amount")
            self.page.get_by_role("button", name="Deposit", exact=True).click()
            # Handle transaction approve popup
            self.wallet_confirmation_pop()
        print("Vault Successful")

    def testnet_hotstuff_trade(self):
        time.sleep(1)
        self.page.get_by_role("button", name="Connect Wallet").click()
        self.page.get_by_role("button", name="MetaMask-icon MetaMask").click()
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        time.sleep(2)
        already_ref = self.page.locator("// *[text() = 'You are already using a referral code and cannot change it.']")
        if already_ref.is_visible():
            self.page.locator("//*[text()='Continue to Trading']").click()
            time.sleep(1)
        join_Code = self.page.get_by_role("button", name="Join with Code")
        if join_Code.is_visible():
           self.page.get_by_role("button", name="Join with Code").click()
           time.sleep(1)
        self.page.get_by_role("button", name="Faucet").first.click()
        self.page.get_by_role("button", name="Claim Testnet Tokens").click()
        self.page.get_by_role("button", name="Faucet").first.click()
        self.page.get_by_role("combobox").click()
        self.page.get_by_role("option", name="USDT USDT").click()
        self.page.get_by_role("button", name="Claim Testnet Tokens").click()
        self.page.get_by_role("tab", name="Market").click()
        self.page.get_by_role("textbox").first.click()
        self.page.get_by_role("textbox").first.fill("1000")
        self.page.get_by_role("button", name="Enable Trading").click()
        time.sleep(2)
        self.page.get_by_role("button", name="Confirm").click()
        # Handle transaction approve popup
        self.wallet_confirmation_pop()
        if self.page.get_by_role("button", name="Claim Testnet Tokens").is_visible():
            self.page.get_by_role("button", name="Claim Testnet Tokens").click()
            time.sleep(1)
        self.page.get_by_role("button", name="Buy/Long").click()
        self.page.get_by_role("button", name="Buy / Long").click()
        self.page.get_by_role("button", name="Sell/Short").click()
        self.page.get_by_role("button", name="Sell / Short").click()
        self.page.get_by_role("button", name="BTC-PERP BTC-PERP 50x").click()
        self.page.get_by_label("BTC-PERP50x").get_by_text("ETH-PERP25x").click()
        self.page.get_by_role("textbox").first.click()
        self.page.get_by_role("textbox").first.fill("1000")
        self.page.get_by_role("button", name="Buy/Long").click()
        self.page.get_by_role("button", name="Buy / Long").click()
        self.page.get_by_role("button", name="Sell/Short").click()
        self.page.get_by_role("button", name="Sell / Short").click()
        self.page.get_by_role("button", name="ETH-PERP ETH-PERP 25x").click()
        self.page.get_by_label("ETH-PERP25x").get_by_text("HYPE-PERP").click()
        self.page.get_by_role("textbox").first.click()
        self.page.get_by_role("textbox").first.fill("10")
        self.page.get_by_role("button", name="Buy/Long").click()
        self.page.get_by_role("button", name="Buy / Long").click()
        self.page.get_by_role("button", name="Sell/Short").click()
        self.page.get_by_role("button", name="Sell / Short").click()
        print("Swap Successful")
        self.page.get_by_role("button", name="Vaults").click()
        self.page.locator("div").filter(has_text=re.compile(r"^Deposit$")).nth(1).click()
        self.page.get_by_role("spinbutton").click()
        self.page.get_by_role("spinbutton").fill("100")
        self.page.get_by_role("button", name="Deposit").click()
        print("Deposit Successful")

    def testnet_x1ecochain(self):
        time.sleep(2)
        self.page.get_by_role("button", name="Connect").click()
        self.page.get_by_test_id("rk-wallet-option-metaMask").click()
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        time.sleep(2)
        # Handle transaction approve popup
        self.wallet_confirmation_pop()
        time.sleep(2)
        # Handle transaction approve popup
        self.wallet_approve_pop()
        time.sleep(2)
        self.page.get_by_role("button", name="Get ECO Points").click()
        time.sleep(1)
        self.page.evaluate("window.scrollBy(0, 800)")
        time.sleep(2)
        self.page.locator("//*[contains(@class,'Quest') and .//*[text()='Daily Login']]//button[normalize-space()='Claim']").click()
        time.sleep(2)
        self.page.locator(
            "div:nth-child(4) > .QuestsContent > .Quests > div:nth-child(2) > .Quest > .Content > .BottomContent > .ButtonElement").click()
        time.sleep(2)
        self.page.get_by_role("button", name="Request").click()
        time.sleep(2)
        self.page.locator(".Cross > path").click()
        self.page.locator("//*[contains(@class,'Quest') and .//*[text()='Claim Faucet']]//button[normalize-space()='Claim']").click()
        time.sleep(2)
        self.page.locator(
            "div:nth-child(4) > .QuestsContent > .Quests > div > .Quest > .Content > .BottomContent > .ButtonElement").click()
        time.sleep(1)
        self.page.get_by_role("button", name="1,0 X1T").click()
        time.sleep(1)
        self.page.get_by_role("button", name="Random Address").click()
        time.sleep(1)
        self.page.get_by_role("button", name="Send X1T Coins").click()
        time.sleep(1)
        # Handle transaction approve popup
        self.wallet_confirmation_pop()
        time.sleep(1)
        self.page.locator(".Cross").click()
        time.sleep(1)
        self.page.locator("//*[contains(@class,'Quest') and .//*[text()='Send X1T']]//button[normalize-space()='Claim']").click()

    def test_fhenix(self):
        self.page.get_by_role("button", name="Connect Wallet", exact=True).click()
        self.page.get_by_role("button", name="MetaMask MetaMask").click()
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        self.page.get_by_role("button", name="Switch network").click()
        self.page.get_by_role("button", name="Sepolia icon Sepolia").click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_next_pop()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        if self.page.locator("[data-testid='confirm-footer-button']").is_visible():
            # Confirm MetaMask transaction
            self.wallet_confirmation_pop()
        self.page.get_by_role("button", name="Go back").click()
        self.page.get_by_role("spinbutton").click()
        self.page.get_by_role("spinbutton").fill("0.01")
        self.page.get_by_role("button", name="ENCRYPT").click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_text("Encrypt 0.01 ETH complete!")
        locator.wait_for(state="visible", timeout=60000)
        self.page.get_by_text("Decrypt").click()
        time.sleep(30)
        btn = self.page.get_by_role("button", name="DECRYPT eETH")
        btn.wait_for(state="visible")
        expect(btn).to_be_enabled()
        btn.click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_role("button", name="CLAIM ETH")
        locator.wait_for(state="visible", timeout=60000)
        self.page.get_by_role("button", name="CLAIM ETH").click()

        self.page.goto("https://shieldedmode.fhenix.io/")
        self.page.get_by_role("button", name="Connect").click()
        self.page.get_by_test_id("rk-wallet-option-metaMask").click()
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        self.page.get_by_role("button", name="ADD CONFIDENTIALITY").click()
        self.page.get_by_role("button", name="DEPLOY CONTRACT").click()
        self.page.get_by_role("button", name="Deploy", exact=True).click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_text("Deployment Successful!")
        locator.wait_for(state="visible", timeout=60000)
        self.page.get_by_role("button", name="View Tokens").click()
        self.page.get_by_role("button", name="Generate Permit", exact=True).click()
        self.page.get_by_role("button", name="Generate Permit").nth(2).click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        self.page.get_by_role("button").filter(has_text=re.compile(r"^$")).nth(3).click()
        self.page.get_by_text("Fhenix USD (FUSD)ShieldedAddress:").click()
        self.page.get_by_role("button", name="Mint Tokens").click()
        self.page.get_by_placeholder("0.00").click()
        self.page.locator("div").filter(has_text=re.compile(r"^Mint Tokens$")).click()
        self.page.get_by_placeholder("0.00").click()
        self.page.get_by_placeholder("0.00").fill("0.1")
        self.page.get_by_role("button", name="Mint Tokens").nth(1).click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_text("Tokens minted successfully!")
        locator.wait_for(state="visible", timeout=60000)
        self.page.get_by_role("button", name="Close").click()
        self.page.get_by_role("button", name="Mint Tokens").click()
        self.page.get_by_role("button", name="Private").click()
        self.page.get_by_placeholder("0.00").click()
        self.page.get_by_placeholder("0.00").fill("0.1")
        self.page.get_by_role("button", name="Mint Shielded Tokens").click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_text("Tokens minted successfully!")
        locator.wait_for(state="visible", timeout=60000)
        self.page.get_by_role("button", name="Close").click()
        self.page.get_by_role("button", name="Shield / Unshield").click()
        self.page.get_by_placeholder("0.00").click()
        self.page.get_by_placeholder("0.00").fill("0.01")
        self.page.get_by_role("button", name="Shield Tokens").click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_text("Tokens shielded successfully!")
        locator.wait_for(state="visible", timeout=100000)
        self.page.get_by_role("button", name="Close").click()
        self.page.get_by_role("button", name="Shield / Unshield").click()
        self.page.get_by_role("button", name="Unshield", exact=True).click()
        self.page.get_by_text("Unshield Tokens", exact=True).click()
        self.page.locator(".lucide.lucide-arrow-up-from-line.w-4.h-4.text-primary").click()
        self.page.get_by_role("button", name="Reveal Balance").click()
        self.page.get_by_placeholder("0.00").click()
        self.page.get_by_placeholder("0.00").fill("0.01")
        self.page.get_by_role("button", name="Request Unshield").click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_text("Decryption complete! Amount")
        locator.wait_for(state="visible", timeout=60000)
        self.page.get_by_role("button", name="Claim Tokens").click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        self.page.get_by_text("Tokens claimed successfully!").click()
        self.page.get_by_role("button", name="Close").click()
        self.page.get_by_role("button", name="Use This Token").click()
        self.page.get_by_role("textbox", name="0x...").click()
        self.page.get_by_role("textbox", name="0x...").fill("0x34af06a24c7de574de5ebdc5f16d9f5a2299029a")
        self.page.get_by_placeholder("0.00").click()
        self.page.get_by_placeholder("0.00").fill("0.01")
        self.page.get_by_role("button", name="Transfer").click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_text("Transfer successful!")
        locator.wait_for(state="visible", timeout=60000)
        self.page.get_by_role("button", name="Private").click()
        self.page.get_by_role("button", name="Reveal Balance").click()
        self.page.get_by_role("button", name="Fhenix USD(FUSD)").click()
        self.page.get_by_role("button", name="Fhenix USD(FUSD)Shielded").click()
        self.page.get_by_role("textbox", name="0x...").click()
        self.page.get_by_role("textbox", name="0x...").fill("0x34af06a24c7de574de5ebdc5f16d9f5a2299029a")
        self.page.get_by_role("button", name="Max: 0.10 FUSD").click()
        self.page.get_by_role("button", name="Confidential Transfer").click()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        locator = self.page.get_by_text("Transfer successful!")
        locator.wait_for(state="visible", timeout=60000)

    def test_skale(self):
        time.sleep(2)
        self.page.get_by_label("").get_by_text("Connect Wallet").click()
        self.page.locator("a").filter(has_text="Connect with Ethereum").click()
        self.page.get_by_text("MetaMaskInstalled").click()
        # Handle MetaMask connection popup
        self.wallet_connect_pop()
        # Confirm MetaMask transaction
        self.wallet_confirmation_pop()
        self.page.evaluate("window.scrollBy(0, 1000)")
        time.sleep(5)
        self.page.get_by_role("button", name="Check in ").click()
        time.sleep(2)
        if self.page.locator("[data-testid='confirm-footer-button']").is_visible():
            # Confirm MetaMask transaction
            self.wallet_confirmation_pop()
            time.sleep(1)
            self.page.get_by_role("button", name="Check in ").click()
        locator = self.page.get_by_text("Congrats on the successful")
        locator.wait_for(state="visible", timeout=60000)
        self.page.get_by_role("button", name="Close").click()

