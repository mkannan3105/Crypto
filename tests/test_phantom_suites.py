import sys, os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

# ✅ Proper path setup
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from playwright_setup import launch_browser_phantom
from pages.phantom_page import PhantomPage
from pages.project_page import ProjectPage
import config.config as cfg

TOTAL_WALLETS = 1000
MAX_PARALLEL = 2


class TestPhantomRun:
    SEED_WORDS_LIST = [getattr(cfg, f"SEED_WORDS{i}") for i in range(1000)]

    # =========================================================
    # 🔹 SETUP
    # =========================================================
    def setup(self, i=0, clean_profile=True):
        profile_name = f"profile_{i}"
        playwright = None
        browser = None

        try:
            # 🔥 stagger launch
            time.sleep((i % MAX_PARALLEL) * 3)

            playwright, browser = launch_browser_phantom(
                profile_name=profile_name,
                clean_profile=clean_profile,
                headless=False
            )

            time.sleep(4)  # extension load time

            phantom_tab = None

            # ✅ Detect extension popup (same as MetaMask)
            for attempt in range(2):
                try:
                    page = browser.wait_for_event("page", timeout=15000)
                    if "chrome-extension://" in page.url:
                        phantom_tab = page
                        break
                except:
                    time.sleep(1)

            # 🔥 fallback scan
            if not phantom_tab:
                for p in browser.pages:
                    if "chrome-extension://" in p.url:
                        phantom_tab = p
                        break

            if not phantom_tab:
                raise Exception("Phantom extension not loaded")

            # ✅ Close unwanted tabs
            for p in list(browser.pages):
                if p != phantom_tab:
                    try:
                        p.close()
                    except:
                        pass

            phantom_tab.bring_to_front()
            phantom_tab.wait_for_load_state("domcontentloaded")

            page = phantom_tab

            # ================================
            # ✅ Import wallet
            # ================================
            phantom = PhantomPage(page)
            phantom.import_wallet(
                self.SEED_WORDS_LIST[i]
            )

            return playwright, browser, page

        except Exception as e:
            print(f"❌ Wallet {i} - Phantom setup failed: {type(e).__name__}: {e}")

            try:
                if browser:
                    browser.close()
            except:
                pass

            try:
                if playwright:
                    playwright.stop()
            except:
                pass

            return None, None, None

    # =========================================================
    # 🔹 TEARDOWN
    # =========================================================
    def teardown(self, playwright, browser):
        try:
            if browser:
                browser.close()
        except:
            pass

        try:
            if playwright:
                playwright.stop()
        except:
            pass


# =============================================================
# 🔥 PARALLEL WORKER
# =============================================================
def run_wallet_flow(i: int, flow_name: str):
    test = TestPhantomRun()

    playwright, browser, page = test.setup(i)

    if not page:
        print(f"❌ Setup failed for wallet {i}")
        return

    try:
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)

        project = ProjectPage(page)

        if flow_name == "test_early_bulk_trade":
            page.goto("https://early.bulk.trade/")
            project.test_early_bulk_trade()

        print(f"✅ Completed wallet {i} [{flow_name}]")

    except Exception as e:
        print(f"❌ Wallet failed {i} [{flow_name}]: {e}")

    finally:
        test.teardown(playwright, browser)
        time.sleep(2)


# =============================================================
# 🚀 MASTER PARALLEL RUNNER
# =============================================================
def run_parallel(flow_name: str, start_index=0, end_index=TOTAL_WALLETS):
    print(f"🚀 Starting Phantom run: {flow_name} [{start_index} → {end_index}]")

    with ProcessPoolExecutor(max_workers=MAX_PARALLEL) as executor:
        futures = [
            executor.submit(run_wallet_flow, i, flow_name)
            for i in range(start_index, end_index)
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("❌ Worker crashed:", e)


# =============================================================
# ▶️ MAIN
# =============================================================
if __name__ == "__main__":
    run_parallel("test_early_bulk_trade", 0, 1000)