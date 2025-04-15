
Write-Host "Initialisation du projet AliExpress Scraper avec Selenium..."

$project = "C:\Users\$env:USERNAME\Documents\aliexpress_scraper_selenium"
New-Item -ItemType Directory -Force -Path $project
Set-Location $project

Write-Host "Création de l'environnement virtuel..."
py -3.10 -m venv venv

Write-Host "Activation de l'environnement virtuel..."
.\venv\Scripts\Activate

Write-Host "Création du fichier requirements.txt..."
@"
streamlit
pandas
selenium
webdriver-manager
"@ | Out-File -Encoding UTF8 requirements.txt

Write-Host "Installation des dépendances..."
pip install -r requirements.txt

New-Item -ItemType Directory -Force -Path "$project\scraper"
New-Item -ItemType File -Path "$project\scraper\__init__.py"

@"
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

def scrape_aliexpress_products(search_url: str, max_items=10) -> list:
    print("Scraping AliExpress avec Selenium...")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(search_url)
    time.sleep(5)

    products = []
    cards = driver.find_elements(By.CSS_SELECTOR, "div[data-productid]")

    for card in cards[:max_items]:
        try:
            title_el = card.find_element(By.CSS_SELECTOR, "h1, h2, h3, .manhattan--titleText--WccSjUS")
            price_el = card.find_element(By.CSS_SELECTOR, "._12A8D, .manhattan--price-sale--1CCSZfK")
            link_el = card.find_element(By.CSS_SELECTOR, "a")
            title = title_el.text.strip() if title_el else "N/A"
            price = price_el.text.strip() if price_el else "N/A"
            link = link_el.get_attribute("href") if link_el else ""
            full_link = f"https:{link}" if link.startswith("//") else link

            products.append({
                "Titre": title,
                "Prix": price,
                "Lien": full_link
            })
        except:
            continue

    driver.quit()
    return products
"@ | Out-File -Encoding UTF8 "$project\scraper\ali_scraper.py"

@"
import streamlit as st
import pandas as pd
from scraper.ali_scraper import scrape_aliexpress_products

st.set_page_config(page_title="AliExpress Scraper")
st.title("Scraper AliExpress (Selenium)")

ali_url = st.text_input("URL de recherche AliExpress", placeholder="https://fr.aliexpress.com/w/wholesale-nogi.html")

if st.button("Scraper AliExpress"):
    if not ali_url:
        st.warning("Veuillez entrer une URL valide.")
    else:
        with st.spinner("Scraping en cours..."):
            try:
                data = scrape_aliexpress_products(ali_url, max_items=10)
                df = pd.DataFrame(data)
                st.success(f"{len(df)} produits trouvés")
                st.dataframe(df)
                st.download_button("Télécharger CSV", df.to_csv(index=False).encode("utf-8"), "produits.csv", "text/csv")
            except Exception as e:
                st.error(f"Erreur : {e}")
"@ | Out-File -Encoding UTF8 "$project\app.py"

Write-Host "Projet Selenium prêt. Lancez avec :"
Write-Host "cd `"$project`""
Write-Host ".\venv\Scripts\activate"
Write-Host "streamlit run app.py"
