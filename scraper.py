from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_rank(username):
    url = f"https://tracker.gg/marvel-rivals/profile/ign/{username}/overview"
    print(f"🚀 Opening URL: {url}")  # Debugging

    # Set up Chrome options for headless mode
    options = Options()
    options.add_argument("--headless")  # Run without GUI
    options.add_argument("--no-sandbox")  # Required for Docker
    options.add_argument("--disable-dev-shm-usage")  # Prevent memory issues
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Start Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(url)  # Open page
        print("✅ Successfully loaded page!")  # Debugging

        # Print page source for debugging
        time.sleep(5)  # Allow page to load
        page_source = driver.page_source
        print(f"🔍 Page Source:\n{page_source[:1000]}")  # Print first 1000 characters

        # Scroll to load dynamic content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("📜 Scrolled down!")

        # Wait for rank element
        rank_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-v-61e89f95]"))
        )
        print("✅ Rank element found!")

        # Wait for RS element
        rs_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-v-044b198d]"))
        )
        print("✅ RS element found!")

        # Extract rank & RS
        rank = rank_element.text.strip() if rank_element else "Not found"
        rs = rs_element.text.strip() if rs_element else "Not found"

        print(f"🎯 Extracted Data: Rank={rank}, RS={rs}")  # Debugging
        return {"username": username, "rank": rank, "RS": rs}

    except Exception as e:
        print(f"❌ Error: {str(e)}")  # Print error
        return {"error": str(e)}

    finally:
        driver.quit()  # Close browser
