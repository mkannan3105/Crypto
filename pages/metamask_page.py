import time
import locators.metamask_locators as mm

class MetaMaskPage:
    def __init__(self, page):
        self.page = page

    def import_wallet(self, seed_words, password):
        """Import MetaMask wallet using seed phrase and password."""
        self.page.locator(mm.TERMS_CHECKBOX).click()
        self.page.locator(mm.IMPORT_WALLET_BTN).click()
        self.page.locator(mm.I_AGREE_BTN).click()

        for i, word in enumerate(seed_words):
            self.page.locator(f"#import-srp__srp-word-{i}").type(word)

        # Confirm recovery phrase
        self.page.locator(".import-srp__confirm-button").click()
        self.page.locator(mm.PASSWORD_INPUT).type(password)
        self.page.locator(mm.CONFIRM_PASSWORD_INPUT).type(password)
        self.page.locator(mm.PASSWORD_TERMS_CHECKBOX).click()
        self.page.locator(mm.IMPORT_BTN).click()

        # Complete onboarding
        self.page.locator(mm.DONE_BTN).click()
        self.page.locator(mm.NEXT_BTN).click()
        self.page.locator(mm.DONE_PIN_BTN).click()
        self.page.locator(mm.NOT_NOW_BTN).click()
        self.page.locator(mm.CLOSE_POPUP_BTN).click()

    def get_wallet_address(self):
        """Fetch Ethereum address as a single string."""
        self.page.locator(mm.RECEIVE_BTN).click()
        raw_address = self.page.locator(mm.QR_ADDRESS).inner_text()
        lines = [line.strip() for line in raw_address.splitlines() if line.strip()]
        return "".join(lines)
