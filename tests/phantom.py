from playwright.sync_api import sync_playwright
import time

PHANTOM_PATH = r"C:\Users\mkann\AppData\Local\Google\Chrome\User Data\Default\Extensions\bfnaelmomeimhlpmgjnjophhpkkoljpa\26.6.1_0"


def launch_phantom(profile_name="phantom_profile", headless=False):
    p = sync_playwright().start()

    context = p.chromium.launch_persistent_context(
        user_data_dir=profile_name,
        headless=headless,
        args=[
            f"--disable-extensions-except={PHANTOM_PATH}",
            f"--load-extension={PHANTOM_PATH}",
            "--start-maximized",
        ],
    )

    # 🔥 WAIT for service worker (THIS is key for MV3)
    service_worker = None

    for _ in range(15):
        workers = context.service_workers
        if workers:
            service_worker = workers[0]
            break
        time.sleep(1)

    if not service_worker:
        raise Exception("Phantom service worker not found")

    # ✅ get extension id dynamically
    extension_id = service_worker.url.split("/")[2]
    print("✅ Phantom extension id:", extension_id)

    # 🔥 OPEN Phantom UI manually (CRITICAL)
    phantom_page = context.new_page()
    phantom_page.goto(f"chrome-extension://{extension_id}/popup.html")

    phantom_page.wait_for_load_state("domcontentloaded")

    return p, context, phantom_page

if __name__ == "__main__":
    p, context, phantom = launch_phantom()

    print("🔥 Phantom ready:", phantom.url)

    input("Press Enter to close...")
    context.close()
    p.stop()