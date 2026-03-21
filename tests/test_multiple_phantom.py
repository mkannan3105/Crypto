# Create Multiple Phantom Wallet
from playwright.sync_api import sync_playwright

path_to_extension = r"C:\Users\mkann\AppData\Local\Google\Chrome\User Data\Default\Extensions\bfnaelmomeimhlpmgjnjophhpkkoljpa\26.7.1_0"

TOTAL_WALLETS = 1000   # change to 1000 if needed

all_seeds = []

with sync_playwright() as p:
    for i in range(TOTAL_WALLETS):
        #print(f"\n🚀 Creating Wallet {i}...")
        user_data_dir = f"user-data-{i}"
        context = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False,
            args=[
                f"--disable-extensions-except={path_to_extension}",
                f"--load-extension={path_to_extension}",
            ],
        )
        page = context.pages[0]
        page.goto("chrome-extension://bfnaelmomeimhlpmgjnjophhpkkoljpa/onboarding.html")

        # Create wallet
        page.get_by_role("button", name="Create a New Wallet").click()
        page.get_by_test_id("create-manual-seed-phrase").click()

        # Password
        page.get_by_test_id("onboarding-form-password-input").fill("12345678")
        page.get_by_test_id("onboarding-form-confirm-password-input").fill("12345678")
        page.get_by_test_id("onboarding-form-terms-of-service-checkbox").check()
        page.get_by_test_id("onboarding-form-submit-button").click()

        # Wait for recovery phrase
        page.wait_for_selector('[data-testid^="secret-recovery-phrase-word-input-"]')
        inputs = page.locator('[data-testid^="secret-recovery-phrase-word-input-"]')
        words = [inputs.nth(j).input_value() for j in range(inputs.count())]
        #print(f"✅ Wallet {i} Seed:", words)
        print(f"SOL_SEED_WORDS{i} =", words)

        all_seeds.append(words)

        # Continue flow
        page.get_by_test_id("onboarding-form-saved-secret-recovery-phrase-checkbox").click()
        page.get_by_test_id("onboarding-form-submit-button").click()

        context.close()

# ---- Save in required format ----
with open("seeds.py", "w") as f:
    for idx, seed in enumerate(all_seeds):
        f.write(f'SEED_WORDS{idx} = {seed}\n')

print("\n🎉 All wallets created and saved to seeds.py")