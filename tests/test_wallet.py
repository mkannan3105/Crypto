import os
import shutil
import time
from playwright.sync_api import sync_playwright
EXTENSION_PATH = r"C:\Users\mkann\Downloads\metamask-chrome-12.20.1"
USER_DATA_DIR = os.path.join(os.getcwd(), "playwright_profile")

for run_id in range(260, 1001):
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
        context.wait_for_event("serviceworker")
        background = context.service_workers
        if not background:
            raise Exception("No service worker found. MetaMask not loaded.")
        extension_url = background[0].url
        extension_id = extension_url.split("/")[2]
        # Open MetaMask UI
        page = context.new_page()
        time.sleep(5)
        context.pages[0].close()
        time.sleep(15)
        page.goto(f"chrome-extension://{extension_id}/home.html")
        time.sleep(2)
        context.pages[1].close()
        time.sleep(1)
        page.wait_for_selector("#onboarding__terms-checkbox", timeout=60000)
        page.locator("#onboarding__terms-checkbox").click()
        page.locator("//button[contains(text(), 'Create a new wallet')]").click()
        page.locator("//*[@class='mm-checkbox__input-wrapper']").click()
        page.locator("//button[contains(text(), 'I agree')]").click()
        page.locator("[data-testid='create-password-new']").type("password")
        page.locator("[data-testid='create-password-confirm']").type("password")
        page.locator("[data-testid='create-password-terms']").click()
        page.locator("//button[contains(text(), 'Create a new wallet')]").click()
        # click secure wallet
        page.locator("[data-testid='secure-wallet-recommended']").click()
        # reveal seed phrase
        page.locator("[data-testid='recovery-phrase-reveal']").click()
        # wait for chips container
        page.wait_for_selector("[data-testid='recovery-phrase-chips']")
        # seed words
        seed_locator = page.locator("[data-testid^='recovery-phrase-chip-']")
        count = seed_locator.count()
        seed_words = []
        for i in range(count):
            word = seed_locator.nth(i).inner_text().strip()
            seed_words.append(word)
        seed_phrase = " ".join(seed_words)
        formatted_words = ", ".join(f'"{word}"' for word in seed_words)
        # click Next
        page.get_by_role("button", name="Next").click()
        # Wait for confirm screen inputs
        page.wait_for_selector("input[data-testid^='recovery-phrase-input-']")
        # Get all confirm input fields
        inputs = page.locator("input[data-testid^='recovery-phrase-input-']")
        count = inputs.count()
        for i in range(count):
            input_box = inputs.nth(i)
            test_id = input_box.get_attribute("data-testid")
            position = int(test_id.split("-")[-1])
            correct_word = seed_words[position]
            input_box.fill(correct_word)
        time.sleep(1)
        # Click Confirm
        page.get_by_role("button", name="Confirm").click()
        locator = page.locator("//*[text()='Congratulations!']")
        locator.wait_for(state="visible", timeout=40000)
        print(f'SEED_WORDS{run_id} = [ {formatted_words} ]')
        context.close()  # ✅ important to avoid memory leak