from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_to_bottom(driver, pause_time=2, max_scrolls=10):
    """
    Scrolle vers le bas de la page jusqu'à stabilisation du nombre de cartes.
    """
    last_count = 0
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        cards = driver.find_elements(By.CSS_SELECTOR, "a.search-card-item")
        current_count = len(cards)
        if current_count == last_count:
            break
        last_count = current_count


def scrape_aliexpress_products(search_term_or_url: str, max_items: int = 50) -> list:
    """
    Scrape AliExpress en paginant si nécessaire pour atteindre max_items.
    Accepte un terme de recherche ou une URL de recherche.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    products = []
    page = 1

    while len(products) < max_items:
        # Construction de l'URL avec pagination
        if search_term_or_url.lower().startswith('http'):
            base_url = search_term_or_url
        else:
            base_url = (
                f"https://fr.aliexpress.com/wholesale?SearchText="
                f"{search_term_or_url.replace(' ', '+')}"
            )
        url = (
            base_url
            if page == 1
            else f"{base_url}&page={page}"
        )
        print(f"Chargement page {page} : {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        try:
            cookie_button = wait.until(
                EC.presence_of_element_located(
                    (By.ID, "onetrust-accept-btn-handler")
                )
            )
            cookie_button.click()
            print("Cookies acceptés")
        except:
            print("Pas de popup cookies")

        time.sleep(3)
        print("Scrolling pour charger la page...")
        scroll_to_bottom(driver)

        cards = driver.find_elements(By.CSS_SELECTOR, "a.search-card-item")
        if not cards:
            print(f"Aucune carte sur la page {page}, arrêt.")
            break

        for card in cards:
            if len(products) >= max_items:
                break
            try:
                title_el = card.find_element(By.CSS_SELECTOR, "h3.l5_kr")
                title = title_el.text.strip()

                price_el = card.find_element(By.CSS_SELECTOR, "div.l5_kt")
                price = "".join(
                    span.text for span in price_el.find_elements(By.TAG_NAME, "span")
                ).strip()

                raw_link = card.get_attribute("href")
                full_link = (
                    f"https:{raw_link}" if raw_link.startswith("//") else raw_link
                )

                products.append({
                    "Titre": title,
                    "Prix": price,
                    "Lien": full_link,
                })
                print(f"Produit ajouté: {title}")
            except Exception as e:
                print(f"Erreur sur produit: {e}")
                continue

        if len(products) < max_items:
            page += 1
            continue
        else:
            break

    driver.quit()
    return products


class AliExpressScraper:
    """
    Wrapper de scrape_aliexpress_products
    """
    def __init__(self):
        pass

    def scrape(self, query: str, max_items: int = 50) -> list:
        return scrape_aliexpress_products(query, max_items)
