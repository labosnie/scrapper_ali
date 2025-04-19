import streamlit as st
import pandas as pd
from src.ali_scraper.ali_scraper import AliExpressScraper

# Titre de l'application
st.set_page_config(page_title="AliExpress Scraper", layout="wide")
st.title("🛒 AliExpress Scraper")

# Paramètres utilisateur
query = st.text_input("🔍 Terme de recherche", value="Entrée votre recherche")
max_items = st.slider("🔢 Nombre max de produits à extraire", min_value=10, max_value=100, value=20)

# Bouton pour lancer le scraping
if st.button("🚀 Lancer le scraping"):
    scraper = AliExpressScraper()
    with st.spinner("⏳ Scraping en cours..."):
        
        results = scraper.scrape(query, max_items=max_items)

    if results:
        df = pd.DataFrame(results)
        st.success(f"✅ {len(results)} produits récupérés !")
        st.dataframe(df)
    else:
        st.warning("⚠️ Aucun produit trouvé. Vérifie ta requête ou réessaye.")

# Info footer
st.markdown("---")
st.caption("Développé avec ❤️ par ton scraper personnalisé.")
