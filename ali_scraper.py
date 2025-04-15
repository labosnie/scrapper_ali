from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def scroll_to_bottom(driver, pause_time=2, max_scrolls=20):
    last_count = 0
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        current_cards = driver.find_elements(By.CSS_SELECTOR, "a.search-card-item")
        print(f"Scroll {i+1} - Produits détectés : {len(current_cards)}")
        if len(current_cards) == last_count:
            break
        last_count = len(current_cards)


def scrape_aliexpress_products(search_url: str, max_items=50) -> list:
    print("Scraping page de recherche AliExpress...")

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)

    wait = WebDriverWait(driver, 15)

    try:
        cookie_button = wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        cookie_button.click()
        print("Cookies acceptés")
    except:
        print("Pas de popup cookies")

    time.sleep(3)

    print("Scrolling pour chargement complet...")
    scroll_to_bottom(driver)

    products = []
    cards = driver.find_elements(By.CSS_SELECTOR, "a.search-card-item")
    print(f"Nombre de cartes trouvées: {len(cards)}")

    for card in cards[:max_items]:
        try:
            title_el = card.find_element(By.CSS_SELECTOR, "h3.l5_kr")
            title = title_el.text.strip()

            price_el = card.find_element(By.CSS_SELECTOR, "div.l5_kt")
            price = "".join([span.text for span in price_el.find_elements(By.TAG_NAME, "span")]).strip()

            raw_link = card.get_attribute("href")
            full_link = f"https:{raw_link}" if raw_link.startswith("//") else raw_link

            print(f"Produit trouvé: {title} - {price}")
            products.append({
                "Titre": title,
                "Prix": price,
                "Lien": full_link
            })
        except Exception as e:
            print(f"Erreur sur un produit: {e}")
            continue

    driver.quit()
    return products


