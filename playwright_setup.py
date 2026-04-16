import os
import shutil
from playwright.sync_api import sync_playwright
#from config.config import EXTENSION_PATH, USER_DATA_DIR, SOL_EXTENSION_PATH
from config.config import EXTENSION_PATH, USER_DATA_DIR

SOL_EXTENSION_PATH = r"C:\Users\mkann\AppData\Local\Google\Chrome\User Data\Default\Extensions\bfnaelmomeimhlpmgjnjophhpkkoljpa\26.11.0_0"
# Setup For Metamask
def launch_browser(profile_name="profile_0", clean_profile=False, headless=False):
    profile_path = os.path.join(USER_DATA_DIR, profile_name)

    # ✅ clean browser history per wallet
    if clean_profile and os.path.exists(profile_path):
        shutil.rmtree(profile_path, ignore_errors=True)

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        headless=headless,
        viewport={"width": 1500, "height": 800},
        args=[
            "--start-maximized",
            f"--disable-extensions-except={EXTENSION_PATH}",
            f"--load-extension={EXTENSION_PATH}",
            "--disable-popup-blocking"
            "--disable-web-security",
            "--allow-file-access-from-files",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    )
    return playwright, browser

# Setup For Phantom
def launch_browser_phantom(profile_name="profile_0", clean_profile=False, headless=False):
    profile_path = os.path.join(USER_DATA_DIR, profile_name)

    # ✅ clean browser history per wallet
    if clean_profile and os.path.exists(profile_path):
        shutil.rmtree(profile_path, ignore_errors=True)

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=profile_path,
        headless=headless,
        viewport={"width": 1500, "height": 800},
        args=[
            "--start-maximized",
            f"--disable-extensions-except={SOL_EXTENSION_PATH}",
            f"--load-extension={SOL_EXTENSION_PATH}",
            "--disable-popup-blocking"
            "--disable-web-security",
            "--allow-file-access-from-files",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ],
    )
    return playwright, browser