import shutil
import sys, os
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright.sync_api import sync_playwright
import config.config as cfg

path_to_extension = r"C:\Users\mkann\AppData\Local\Google\Chrome\User Data\Default\Extensions\bfnaelmomeimhlpmgjnjophhpkkoljpa\26.7.1_0"

class TestPhantomRun:
    SEED_WORDS_LIST = [getattr(cfg, f"SEED_WORDS{i}") for i in range(51)]

    def setup(self, i=8,clean_profile=True):
        context = None
        try:
            profile_path = os.path.join(path_to_extension, "profile_0")
            # ✅ clean browser history per wallet
            if clean_profile and os.path.exists(profile_path):
                shutil.rmtree(profile_path, ignore_errors=True)
            #user_data_dir = f"phantom-profile-{i}"
            context = sync_playwright().start().chromium.launch_persistent_context(
                user_data_dir=profile_path,
                headless=False,
                args=[
                    f"--disable-extensions-except={path_to_extension}",
                    f"--load-extension={path_to_extension}",
                ],
            )

            page = context.pages[0]
            page.goto("chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/onboarding.html")

            # Import wallet
            seed_words = self.SEED_WORDS_LIST[i]

            page.get_by_role("button", name="I Already Have a Wallet").click()
            page.get_by_role("button", name="Import Recovery Phrase").click()

            # 🔥 Fill 12 words
            for idx, word in enumerate(seed_words):
                page.get_by_test_id(f"secret-recovery-phrase-word-input-{idx}").fill(word)
            time.sleep(1)
            page.get_by_test_id("onboarding-form-submit-button").click()
            time.sleep(1)
            page.get_by_test_id("onboarding-form-submit-button").click()

            # Continue
            #page.get_by_test_id("onboarding-form-submit-button").click()

            # Set password
            set_pass = page.locator("//*[text()='Create a password']")
            set_pass.wait_for(state="visible", timeout=20000)
            page.get_by_test_id("onboarding-form-password-input").fill("12345678")
            page.get_by_test_id("onboarding-form-confirm-password-input").fill("12345678")
            page.get_by_test_id("onboarding-form-terms-of-service-checkbox").check()
            page.get_by_test_id("onboarding-form-submit-button").click()

            page.get_by_role("button", name="Continue").click()
            page.goto("https://early.bulk.trade/")
            page.get_by_role("button", name="Login").click()
            page.get_by_role("button", name="Phantom").click()
            popup = page.context.wait_for_event("page")
            popup.wait_for_load_state()
            popup.get_by_test_id("primary-button").click()
            popup.close()
            page.get_by_role("button", name="Continue without Ledger").click()
            popup = page.context.wait_for_event("page")
            popup.wait_for_load_state()
            popup.get_by_test_id("primary-button").click()
            popup.close()
            time.sleep(4)
            close = page.locator("[aria-label='Close']")
            if close.is_visible():
               close.wait_for(state="visible", timeout=20000)
               close.click()
            page.locator('//*[@class="inline-flex items-center justify-center focus:outline-none focus-visible:ring-2 focus-visible:ring-opacity-75 transition-all duration-200 bg-[var(--background)] hover:opacity-80 active:bg-[color-mix(in_oklab,var(--background),#000_10%)] text-[var(--text-secondary)] border border-[var(--background-secondary)] rounded-[8px] shadow-[0px_1px_2px_0px_rgba(198,182,186,0.20)] cursor-pointer px-4 py-2 h-8"]').click()
            page.get_by_role("button", name="Claim USDC").click()
            popup = page.context.wait_for_event("page")
            popup.wait_for_load_state()
            popup.get_by_test_id("primary-button").click()
            popup.close()
            page.get_by_role("heading", name="Received 10,000 mock USDC").click()
            page.get_by_role("textbox").click()
            page.get_by_role("textbox").fill("1000")
            page.get_by_role("button", name="Buy / Long").click()
            time.sleep(2)
            page.get_by_role("textbox").click()
            page.get_by_role("textbox").fill("1000")
            page.get_by_role("button", name="Sell / Short").click()
            time.sleep(2)
            page.get_by_role("heading", name="BTC-USD").click()
            page.get_by_text("ETH-USD").nth(1).click()
            page.get_by_role("textbox").click()
            page.get_by_role("textbox").fill("1000")
            page.get_by_role("button", name="Buy / Long").click()
            time.sleep(2)
            page.get_by_role("textbox").click()
            page.get_by_role("textbox").fill("1000")
            page.get_by_role("button", name="Sell / Short").click()
            time.sleep(2)
            page.get_by_role("heading", name="ETH-USD").click()
            page.get_by_text("SOL-USD").nth(1).click()
            page.get_by_role("textbox").click()
            page.get_by_role("textbox").fill("1000")
            page.get_by_role("button", name="Buy / Long").click()
            time.sleep(2)
            page.get_by_role("textbox").click()
            page.get_by_role("textbox").fill("1000")
            page.get_by_role("button", name="Sell / Short").click()
            time.sleep(2)
            return context, page

        except Exception as e:
            print(f"❌ Phantom Wallet {i} setup failed: {e}")
            try:
                if context:
                    context.close()
            except:
                pass
            return None, None

    def teardown(self, context):
        try:
            if context:
                context.close()
        except:
            pass

if __name__ == "__main__":
    test = TestPhantomRun()

    context, page = test.setup()   # 👈 THIS LINE WAS MISSING

    if page:
        print("✅ Browser opened successfully")
    else:
        print("❌ Failed to open browser")

    test.teardown(context)