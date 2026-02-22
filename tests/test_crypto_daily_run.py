import sys, os
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from playwright_setup import launch_browser
from pages.metamask_page import MetaMaskPage
from pages.project_page import ProjectPage
import config.config as cfg


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
            playwright, browser = launch_browser(
                profile_name=profile_name,
                clean_profile=clean_profile,
                headless=False
            )

            # ✅ Wait for MetaMask tab (with retry)
            try:
                metamask_tab = browser.wait_for_event("page", timeout=60000)
            except Exception:
                print(f"⚠️ Wallet {i} - retrying MetaMask tab...")
                metamask_tab = browser.wait_for_event("page", timeout=30000)

            if "chrome-extension://" not in metamask_tab.url:
                raise Exception("MetaMask extension did not load")

            # ✅ Close extra tabs
            for p in browser.pages[:-1]:
                time.sleep(1)
                p.close()

            metamask_tab.reload()
            page = metamask_tab

            # ✅ Import wallet
            metamask = MetaMaskPage(page)
            metamask.import_wallet(
                self.SEED_WORDS_LIST[i],
                cfg.METAMASK_PASSWORD
            )

            return playwright, browser, page

        except Exception as e:
            print(f"❌ Wallet {i} - MetaMask setup failed: {type(e).__name__}: {e}")

            if browser:
                try:
                    browser.close()
                except:
                    pass

            if playwright:
                try:
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
# 🔹 PARALLEL ENTRY FUNCTION (VERY IMPORTANT)
# =============================================================
def run_single_wallet(i: int):
    test = TestCryptoDailyRun()
    playwright, browser, page = test.setup(i)

    if not page:
        print(f"❌ Setup failed for wallet {i}")
        return

    try:
        page.goto("https://hub.veerarewards.com/loyalty?referral_code=MKANNAN3")
        ProjectPage(page).test_veerarewards()
        print(f"✅ Completed wallet {i}")

    except Exception as e:
        print(f"❌ Wallet failed {i}: {e}")

    finally:
        test.teardown(playwright, browser)


    def test_x1ecochain(self):
        for i in range(0, 1000):
            playwright, browser, page = self.setup(i)
            if not page:
                print(f"❌ Setup failed for wallet {i}")
                continue  # 👈 go to next wallet
            try:
                page.goto("https://t.x1.one/?rcode=9Jd82wqL")
                ProjectPage(page).testnet_x1ecochain()
                print("✅ Completed wallet", i)
            except Exception as e:
                print("❌ Wallet failed", i)
            finally:
               self.teardown(playwright, browser)

    """
    def test_veerarewards(self):
        for i in range(0, 1000):
            playwright, browser, page = self.setup(i)
            if not page:
                print(f"❌ Setup failed for wallet {i}")
                continue  # 👈 go to next wallet
            try:
                page.goto("https://hub.veerarewards.com/loyalty?referral_code=MKANNAN3")
                ProjectPage(page).test_veerarewards()
                print("✅ Completed wallet", i)
            except Exception as e:
                print("❌ Wallet failed", i)
            finally:
                self.teardown(playwright, browser)
    """

    def test_konnex(self):
        # Weekly claim
        for i in range(0, 1):
            playwright, browser, page = self.setup(i)
            if not page:
                print(f"❌ Setup failed for wallet {i}")
                continue  # 👈 go to next wallet
            try:
                page.goto("https://hub.konnex.world/points?referral_code=K31CE63L")
                ProjectPage(page).test_konnex()
                print("✅ Completed wallet", i)
            except Exception as e:
                print("❌ Wallet failed", i)
            finally:
                self.teardown(playwright, browser)

    def test_hotstuff_trade(self):
        for i in range(0, 12): # 0-12 Wallet
            playwright, browser, page = self.setup(i)
            if not page:
                print(f"❌ Setup failed for wallet {i}")
                continue  # 👈 go to next wallet
            try:
                page.goto("https://testnet.hotstuff.trade/join/mkannan3105")
                ProjectPage(page).testnet_hotstuff_trade()
                print("✅ Completed wallet", i)
            except Exception as e:
                print("❌ Wallet failed", i)
            finally:
                self.teardown(playwright, browser)

    def test_decibel(self):
        for i in range(0, 1000):
            playwright, browser, page = self.setup(i)
            try:
                page.goto("https://app.decibel.trade/trade/BTC-USD")
                ProjectPage(page).test_decibel()
                print("✅ Completed wallet", i)
            except Exception as e:
                print("❌ Wallet failed", i)
            finally:
                self.teardown(playwright, browser)

def run_single_wallet(i: int):
    test = TestCryptoDailyRun()
    playwright, browser, page = test.setup(i)

    if not page:
         print(f"❌ Setup failed for wallet {i}")
         return

    try:
         page.goto("https://hub.veerarewards.com/loyalty?referral_code=MKANNAN3")
         ProjectPage(page).test_veerarewards()
         print("✅ Completed wallet", i)
    except Exception as e:
         print("❌ Wallet failed", i, e)
    finally:
         test.teardown(playwright, browser)