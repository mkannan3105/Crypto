import time

class PhantomPage:
    def __init__(self, page):
        self.page = page

    def import_wallet(self, seed_words):
        self.page.get_by_role("button", name="I Already Have a Wallet").click()
        self.page.get_by_role("button", name="Import Recovery Phrase").click()

        # 🔥 Fill 12 words
        for idx, word in enumerate(seed_words):
             self.page.get_by_test_id(f"secret-recovery-phrase-word-input-{idx}").fill(word)
        time.sleep(1)
        self.page.get_by_test_id("onboarding-form-submit-button").click()
        time.sleep(1)
        self.page.get_by_test_id("onboarding-form-submit-button").click()

        # Set password
        set_pass = self.page.locator("//*[text()='Create a password']")
        set_pass.wait_for(state="visible", timeout=20000)
        self.page.get_by_test_id("onboarding-form-password-input").fill("12345678")
        self.page.get_by_test_id("onboarding-form-confirm-password-input").fill("12345678")
        self.page.get_by_test_id("onboarding-form-terms-of-service-checkbox").check()
        self.page.get_by_test_id("onboarding-form-submit-button").click()

        self.page.get_by_role("button", name="Continue").click()