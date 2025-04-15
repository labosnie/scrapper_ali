from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_aliexpress_products(search_url: str, max_items=10) -> list:
    print("Scraping AliExpress avec Selenium...")

    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Garde visible pour debug
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)
    print(f"URL chargée: {search_url}")
    
    # Attendre que la page soit chargée
    wait = WebDriverWait(driver, 20)
    
    try:
        # Accepter les cookies si présent
        cookie_button = wait.until(EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")))
        cookie_button.click()
        print("Popup de cookies acceptée")
    except:
        print("Pas de popup de cookies trouvée")

    time.sleep(5)

    # Scroll vers le bas pour forcer le chargement dynamique
    print("Début du scroll...")
    scroll_pause = 2
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(5):
        print(f"Scroll {i+1}/5")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    time.sleep(3)

    products = []
    # Nouveaux sélecteurs spécifiques à AliExpress
    cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='product-card']")
    print(f"Nombre de cartes trouvées: {len(cards)}")

    if len(cards) == 0:
        print("Aucune carte trouvée, tentative avec un autre sélecteur...")
        cards = driver.find_elements(By.CSS_SELECTOR, "div[class*='item']")
        print(f"Nombre de cartes trouvées avec second sélecteur: {len(cards)}")

    for card in cards[:max_items]:
        try:
            title_el = card.find_element(By.CSS_SELECTOR, "h3[class*='title'], div[class*='title']")
            # Nouveau sélecteur pour le prix
            price_el = card.find_element(By.CSS_SELECTOR, "span[style*='font-size:20px'][style*='currency-symbol:€']")
            link_el = card.find_element(By.CSS_SELECTOR, "a[class*='item'], a[class*='product']")
            
            title = title_el.text.strip()
            price = price_el.text.strip()
            link = link_el.get_attribute("href")
            full_link = f"https:{link}" if link.startswith("//") else link

            print(f"Produit trouvé: {title} - {price}")
            products.append({
                "Titre": title,
                "Prix": price,
                "Lien": full_link
            })
        except Exception as e:
            print(f"Erreur sur un produit: {str(e)}")
            continue

    driver.quit()
    return products
