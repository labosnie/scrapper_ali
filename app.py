import streamlit as st
import pandas as pd
from ali_scraper import scrape_aliexpress_products

st.set_page_config(page_title="AliExpress Scraper")
st.title("Scraper AliExpress (Selenium)")

ali_url = st.text_input("URL de recherche AliExpress", placeholder="https://fr.aliexpress.com/w/wholesale-nogi.html")

if st.button("Scraper AliExpress"):
    if not ali_url:
        st.warning("Veuillez entrer une URL valide.")
    else:
        with st.spinner("Scraping en cours..."):
            try:
                data = scrape_aliexpress_products(ali_url, max_items=50)

                # 🔍 DEBUG : voir la sortie brute
                st.subheader("Données brutes retournées")
                st.write(data)

                if not data:
                    st.warning("Aucun produit détecté.")
                else:
                    df = pd.DataFrame(data)
                    st.success(f"{len(df)} produits trouvés")
                    st.dataframe(df)
                    st.download_button("Télécharger CSV", df.to_csv(index=False).encode("utf-8"), "produits.csv", "text/csv")
            except Exception as e:
                st.error(f"Erreur : {e}")
