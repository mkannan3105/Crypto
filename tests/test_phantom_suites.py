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

TOTAL_WALLETS = 10000
MAX_PARALLEL = 2

class TestPhantomRun:
    SEED_WORDS_LIST = [getattr(cfg, f"SEED_WORDS{i}") for i in range(10000)]

    # =========================================================
    # 🔹 SETUP
    # =========================================================
    def setup(self, i=450, clean_profile=True):
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

            time.sleep(6)  # extension load time

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
# =============================================================
# 🔥 PARALLEL WORKER (Retry once if wallet flow fails)
# =============================================================
def run_wallet_flow(i: int, flow_name: str, retry_count: int = 4):
    attempt = 0

    while attempt <= retry_count:
        test = TestPhantomRun()

        playwright, browser, page = test.setup(i)

        if not page:
            print(f"❌ Setup failed for wallet {i} | Attempt {attempt + 1}/{retry_count + 1}")

            if attempt < retry_count:
                attempt += 1
                print(f"🔄 Retrying wallet {i} setup... ({attempt + 1}/{retry_count + 1})")
                time.sleep(5)
                continue

            print(f"🚫 Wallet {i} setup permanently failed after {retry_count + 1} attempts")
            return

        try:
            page.wait_for_load_state("domcontentloaded")
            time.sleep(2)

            project = ProjectPage(page)

            if flow_name == "test_early_bulk_trade":
                page.goto("https://early.bulk.trade/")
                project.test_early_bulk_trade()

            print(f"✅ Completed wallet {i} [{flow_name}]")
            return

        except Exception as e:
            print(
                f"❌ Wallet failed {i} [{flow_name}] | "
                f"Attempt {attempt + 1}/{retry_count + 1}: {e}"
            )

            if attempt < retry_count:
                attempt += 1
                print(f"🔄 Retrying wallet {i}... ({attempt + 1}/{retry_count + 1})")
                time.sleep(5)

            else:
                print(f"🚫 Wallet {i} permanently failed after {retry_count + 1} attempts")

        finally:
            test.teardown(playwright, browser)
            time.sleep(2)

# =============================================================
# 🚀 MASTER PARALLEL RUNNER
# =============================================================
def run_parallel(flow_name: str, start_index: int, end_index: int, max_parallel: int):
    print(f"🚀 Starting Phantom run: {flow_name} [{start_index} → {end_index}] | Workers: {max_parallel}")

    with ProcessPoolExecutor(max_workers=max_parallel) as executor:
        futures = [
            executor.submit(run_wallet_flow, i, flow_name)
            for i in range(start_index, end_index)
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print("❌ Worker crashed:", e)

def run_batched(flow_name: str, batch_size=200, cooldown=900, max_parallel=2,
                start_index=0, end_index=TOTAL_WALLETS):

    for start in range(start_index, end_index, batch_size):
        end = min(start + batch_size, end_index)

        print(f"\n🚀 Running batch: {start} → {end} | Flow: {flow_name}")
        run_parallel(flow_name, start, end, max_parallel)

        if end < end_index:
            print(f"🧊 Cooling for {cooldown // 60} minutes...")
            time.sleep(cooldown)

    print(f"✅ Completed wallets {start_index} → {end_index} for flow: {flow_name}")

# =============================================================
# ▶️ MAIN
# =============================================================
if __name__ == "__main__":
    BATCH_SIZE = 50     # smaller batch (Phantom is heavier)
    COOL_DOWN = 600       # 10 mins
    MAX_PARALLEL = 2

    START = 0
    END = 10000

    run_batched(
        "test_early_bulk_trade",
        batch_size=BATCH_SIZE,
        cooldown=COOL_DOWN,
        max_parallel=MAX_PARALLEL,
        start_index=2830,
        end_index=3001
    )