![Tests](https://github.com/labosnie/scrapper_ali/actions/workflows/python-app.yml/badge.svg)

# 🛍️ AliExpress Scraper avec Streamlit & Selenium

Un scraper web simple et efficace pour extraire les titres, prix et liens de produits depuis les pages de recherche AliExpress.  
Interface utilisateur via **Streamlit**. Automatisation via **Selenium**.

---

## 🚀 Fonctionnalités

- Interface Streamlit simple
- Saisie d’une URL AliExpress (page de recherche)
- Scraping dynamique (scroll + chargement des cartes)
- Extraction :
  - Titre du produit
  - Prix affiché
  - Lien cliquable
- Téléchargement des résultats en `.csv`

---

## ⚙️ Stack technique

- `Python 3.10+`
- `Selenium`
- `Streamlit`
- `webdriver-manager`
- `pandas`

---

## 🧪 Lancer l'app en local

```bash
git clone https://github.com/votre-utilisateur/aliexpress_scraper_selenium.git
cd aliexpress_scraper_selenium

python -m venv venv
venv\Scripts\activate   # ou source venv/bin/activate sur Mac/Linux

pip install -r requirements.txt

streamlit run app.py
```
