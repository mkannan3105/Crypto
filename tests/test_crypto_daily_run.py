import sys, os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playwright_setup import launch_browser
from pages.metamask_page import MetaMaskPage
from pages.project_page import ProjectPage
import config.config as cfg

TOTAL_WALLETS = 1000
MAX_PARALLEL = 2  # 🔥 adjust based on your machine

class TestCryptoDailyRun:
    SEED_WORDS_LIST = [getattr(cfg, f"SEED_WORDS{i}") for i in range(1000)]
    # =========================================================
    # 🔹 SETUP
    # =========================================================
    def setup(self, i=0, clean_profile=True):
        profile_name = f"profile_{i}"
        playwright = None
        browser = None
        try:
            # 🔥 stagger launch to reduce burst load
            time.sleep((i % MAX_PARALLEL) * 3)
            playwright, browser = launch_browser(
                profile_name=profile_name,
                clean_profile=clean_profile,
                headless=False
            )
            # 🔥 give MV3 extension cold start time
            time.sleep(4)
            metamask_tab = None
            # ================================
            # ✅ robust popup detection
            # ================================
            for attempt in range(1):
                try:
                    page = browser.wait_for_event("page", timeout=30000)
                    if page and "chrome-extension://" in page.url:
                        metamask_tab = page
                        break
                except Exception:
                    print(f"⚠️ Wallet {i} - retry MetaMask ({attempt + 1}/4)")
                    #time.sleep(3)
                    time.sleep(1)
            # 🔥 fallback scan (VERY IMPORTANT)
            if not metamask_tab:
                for p in browser.pages:
                    if "chrome-extension://" in p.url:
                        metamask_tab = p
                        break
            if not metamask_tab:
                raise Exception("MetaMask extension did not load")
            # ================================
            # ✅ close garbage tabs
            # ================================
            for p in list(browser.pages):
                if p != metamask_tab:
                    try:
                        p.close()
                    except:
                        pass
            metamask_tab.bring_to_front()
            #metamask_tab.reload()
            metamask_tab.wait_for_load_state("domcontentloaded")
            page = metamask_tab
            # ================================
            # ✅ import wallet
            # ================================
            metamask = MetaMaskPage(page)
            metamask.import_wallet(
                self.SEED_WORDS_LIST[i],
                cfg.METAMASK_PASSWORD
            )
            return playwright, browser, page
        except Exception as e:
            print(f"❌ Wallet {i} - MetaMask setup failed: {type(e).__name__}: {e}")
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

    """
    def test_x1ecochain(self):
        for i in range(0, 1000):
            playwright, browser, page = self.setup(i)
            if not page:
                print(f"❌ Setup failed for wallet {i}")
                continue  # 👈 go to next wallet
            try:
                page.goto("https://t.x1eco.com/?rcode=9Jd82wqL")
                ProjectPage(page).testnet_x1ecochain()
                print("✅ Completed wallet", i)
            except Exception as e:
                print("❌ Wallet failed", i)
            finally:
               self.teardown(playwright, browser)
    """
# =============================================================
# 🔥 PARALLEL WORKER (COMMON FOR ALL TESTS)
# =============================================================
def run_wallet_flow(i: int, flow_name: str):
    test = TestCryptoDailyRun()
    playwright, browser, page = test.setup(i)
    if not page:
        print(f"❌ Setup failed for wallet {i}")
        return
    try:
        #page.wait_for_load_state("networkidle")
        page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        project = ProjectPage(page)
        if flow_name == "veerarewards":
            page.goto("https://hub.veerarewards.com/loyalty?referral_code=MKANNAN3")
            project.test_veerarewards()
        elif flow_name == "x1":
            page.goto("https://t.x1eco.com/?rcode=9Jd82wqL")
            project.testnet_x1ecochain()
        elif flow_name == "konnex":
            page.goto("https://hub.konnex.world/points?referral_code=K31CE63L")
            project.test_konnex()
        elif flow_name == "hotstuff":
            page.goto("https://testnet.hotstuff.trade/join/mkannan3105")
            project.testnet_hotstuff_trade()
        elif flow_name == "decibel":
            page.goto("https://app.decibel.trade/trade/BTC-USD")
            project.test_decibel()
        print(f"✅ Completed wallet {i} [{flow_name}]")
    except Exception as e:
        print(f"❌ Wallet failed {i} [{flow_name}]: {e}")
    finally:
        test.teardown(playwright, browser)
        time.sleep(2)  # 🔥 cooling gap

# =============================================================
# 🚀 MASTER PARALLEL RUNNER
# =============================================================
def run_parallel(flow_name: str, start_index: int = 0, end_index: int = TOTAL_WALLETS, MAX_PARALLEL=MAX_PARALLEL):
    print(f"🚀 Starting parallel run: {flow_name} [{start_index} → {end_index}]")
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
# ▶️ MAIN (RUN WHAT YOU WANT)
# =============================================================
if __name__ == "__main__":
    run_parallel("veerarewards", start_index=0, end_index=1000)
    run_parallel("x1", start_index=0, end_index=1000, MAX_PARALLEL=1)
    #run_parallel("konnex", start_index=0, end_index=1)
    #run_parallel("hotstuff", start_index=0, end_index=12)
    #run_parallel("decibel", start_index=0, end_index=1000)