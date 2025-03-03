from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_rank(username):
    url = f"https://tracker.gg/marvel-rivals/profile/ign/{username}/overview"

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

        # ✅ SCROLL DOWN to load dynamic content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # ✅ WAIT for the rank element to be present (Max wait: 15 seconds)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-v-61e89f95]"))
        )

        # ✅ WAIT for the RS element to be present
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-v-044b198d]"))
        )

        # ✅ Extract Rank & RS (Ensure selectors are correct)
        rank_element = driver.find_element(By.CSS_SELECTOR, "[data-v-61e89f95]")
        rs_element = driver.find_element(By.CSS_SELECTOR, "[data-v-044b198d]")

        rank = rank_element.text.strip() if rank_element else "Not found"
        rs = rs_element.text.strip() if rs_element else "Not found"

        return {"username": username, "rank": rank, "RS": rs}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()  # Close browser
