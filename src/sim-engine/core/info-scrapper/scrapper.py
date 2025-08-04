from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import os


# Setup
BASE_DOMAIN = "https://voz.vn"
BASE_FORUM_URL = f"{BASE_DOMAIN}/f/%C4%90iem-bao.33"

# --- Chrome Options ---
chrome_options = Options()
chrome_options.add_argument("--headless")  # Comment this out to see the browser
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("window-size=1920,1080")
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36"
)

# Path to chromedriver (adjust if needed)
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "chromedriver")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# --- Scraping functions ---
def scrape_page(page_num):
    url = f"{BASE_FORUM_URL}/page-{page_num}"
    print(f"Scraping {url} ...")

    try:
        driver.get(url)
        time.sleep(2)  # Let JavaScript execute and content load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        posts = soup.select("div.structItem-title > a")

        result = []
        for post in posts:
            title = post.get_text(strip=True)
            link = post.get("href")
            full_url = BASE_DOMAIN + link if link.startswith("/") else link
            result.append({"title": title, "url": full_url})

        return result

    except Exception as e:
        print(f"❌ Error on page {page_num}: {e}")
        return []


def scrape_all_pages(start=1, end=10):
    all_posts = []
    for page in range(start, end + 1):
        posts = scrape_page(page)
        all_posts.extend(posts)
    return all_posts


def save_to_file(posts, filename="voz_posts.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for idx, post in enumerate(posts, 1):
            f.write(f"{idx:03d}. {post['title']}\n")
            f.write(f"     {post['url']}\n\n")


# --- Entry point ---
if __name__ == "__main__":
    posts = scrape_all_pages(1, 10)
    save_to_file(posts)
    driver.quit()
    print("✅ Saved to voz_posts.txt")
