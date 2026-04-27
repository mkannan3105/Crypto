import os
import shutil
import time
from playwright.sync_api import sync_playwright

EXTENSION_PATH = r"C:\Users\mkann\Downloads\metamask-chrome-12.20.1"
USER_DATA_DIR = os.path.join(os.getcwd(), "playwright_profile")

failed_wallets = []

for run_id in range(1000, 2000):
    #print(f"\n🚀 Starting wallet {run_id}")

    context = Nones
    try:
        # ✅ ALWAYS clean profile for fresh wallet
        clean_profile = True
        if clean_profile and os.path.exists(USER_DATA_DIR):
            shutil.rmtree(USER_DATA_DIR, ignore_errors=True)

        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=False,
                args=[
                    f"--disable-extensions-except={EXTENSION_PATH}",
                    f"--load-extension={EXTENSION_PATH}",
                ],
            )
            metamask_tab = context.wait_for_event("page")
            if "chrome-extension://" not in metamask_tab.url:
                raise Exception("MetaMask extension did not load")
            for p in context.pages[:-1]:
                time.sleep(1)
                p.close()
            metamask_tab.reload()
            page = metamask_tab
            # ===== ONBOARDING =====
            page.wait_for_selector("#onboarding__terms-checkbox", timeout=60000)
            page.locator("#onboarding__terms-checkbox").click()

            page.locator("//button[contains(text(), 'Create a new wallet')]").click()
            page.locator("//*[@class='mm-checkbox__input-wrapper']").click()
            page.locator("//button[contains(text(), 'I agree')]").click()

            page.locator("[data-testid='create-password-new']").fill("password")
            page.locator("[data-testid='create-password-confirm']").fill("password")
            page.locator("[data-testid='create-password-terms']").click()
            page.locator("//button[contains(text(), 'Create a new wallet')]").click()

            # Secure wallet
            page.locator("[data-testid='secure-wallet-recommended']").click()

            # Reveal seed phrase
            page.locator("[data-testid='recovery-phrase-reveal']").click()
            page.wait_for_selector("[data-testid='recovery-phrase-chips']")

            # ===== CAPTURE SEED =====
            seed_locator = page.locator("[data-testid^='recovery-phrase-chip-']")
            count = seed_locator.count()

            seed_words = []
            for i in range(count):
                word = seed_locator.nth(i).inner_text().strip()
                seed_words.append(word)

            formatted_words = ", ".join(f'"{word}"' for word in seed_words)

            # Next
            page.get_by_role("button", name="Next").click()

            # ===== CONFIRM SEED =====
            page.wait_for_selector("input[data-testid^='recovery-phrase-input-']")
            inputs = page.locator("input[data-testid^='recovery-phrase-input-']")
            count = inputs.count()

            for i in range(count):
                input_box = inputs.nth(i)
                test_id = input_box.get_attribute("data-testid")
                position = int(test_id.split("-")[-1])
                correct_word = seed_words[position]
                input_box.fill(correct_word)

            time.sleep(1)

            # Confirm
            page.get_by_role("button", name="Confirm").click()
            page.locator("//*[text()='Congratulations!']").wait_for(
                state="visible", timeout=40000
            )

            #print(f"🎉 Wallet {run_id} created successfully")
            print(f'SEED_WORDS{run_id} = [ {formatted_words} ]')

            context.close()

    except Exception as e:
        print(f"❌ Wallet {run_id} FAILED: {e}")
        failed_wallets.append(run_id)

        try:
            if context:
                context.close()
        except:
            pass

        continue


# ===== SUMMARY =====
print("\n==============================")
print("FAILED WALLETS:", failed_wallets)
print("TOTAL FAILED:", len(failed_wallets))
print("==============================")


