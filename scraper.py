import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_rank(username):
    url = f"https://tracker.gg/marvel-rivals/profile/ign/{username}/overview"
    print(f"🚀 Opening URL: {url}")

    # Use undetected Chrome driver
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")  # New headless mode (helps bypass detection)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Bypass detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        print("✅ Successfully loaded page!")

        # Wait for Cloudflare to finish loading (adjust if needed)
        time.sleep(10)

        # Print page source to confirm Cloudflare is gone
        print(f"🔍 Page Source After Waiting:\n{driver.page_source[:1000]}")

        # Scroll to ensure full content is loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("📜 Scrolled down!")

        # Wait for Rank element
        rank_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-v-61e89f95]"))
        )
        print("✅ Rank element found!")

        # Wait for RS element
        rs_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-v-044b198d]"))
        )
        print("✅ RS element found!")

        # Extract data
        rank = rank_element.text.strip() if rank_element else "Not found"
        rs = rs_element.text.strip() if rs_element else "Not found"

        print(f"🎯 Extracted Data: Rank={rank}, RS={rs}")
        return {"username": username, "rank": rank, "RS": rs}

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"error": str(e)}

    finally:
        driver.quit()
