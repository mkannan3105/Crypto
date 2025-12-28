import locators.project_locators as ethereal
import time

class ProjectPage:
    def __init__(self, page):
        self.page = page

    def wallet_connect_pop(self):
        # Handle MetaMask connection popup
        time.sleep(1)
        popup = self.page.context.wait_for_event("page")
        popup.wait_for_load_state()
        popup.get_by_test_id("confirm-btn").click()
        popup.close()

    def wallet_confirmation_pop(self):
         # Confirm MetaMask transaction
         popup = self.page.context.wait_for_event("page")
         popup.wait_for_load_state()
         popup.wait_for_selector("[data-testid='confirm-footer-button']", timeout=20000)
         popup.locator("[data-testid='confirm-footer-button']").click()
         popup.close()

    def wallet_approve_pop(self):
         # Handle transaction confirmation popup
         popup = self.page.context.wait_for_event("page")
         popup.wait_for_selector("[data-testid='confirmation-submit-button']", timeout=20000)
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
