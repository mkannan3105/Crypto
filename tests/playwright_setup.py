from playwright.sync_api import sync_playwright
from config.config import EXTENSION_PATH, USER_DATA_DIR
import os
import shutil

def launch_browser():
    """Launch Chromium with MetaMask extension loaded."""

    # Clean profile for fresh launch
    if os.path.exists(USER_DATA_DIR):
        shutil.rmtree(USER_DATA_DIR, ignore_errors=True)

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        viewport={"width": 1500, "height": 800},
        args=[
            "--start-maximized",
            f"--disable-extensions-except={EXTENSION_PATH}",
            "--disable-popup-blocking"
            "--disable-web-security",
            "--allow-file-access-from-files",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            f"--load-extension={EXTENSION_PATH}",
        ],
    )
    return playwright, browser