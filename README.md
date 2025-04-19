# 🛍️ AliExpress Scraper (Selenium + Streamlit)

Une application simple pour scraper les titres, prix et liens de produits sur une page de recherche AliExpress, en utilisant **Selenium** et une interface **Streamlit**.

## 🚀 Fonctionnalités

- Recherche par mot‑clé ou URL
- Pagination automatique jusqu’à un nombre d’items défini
- Configuration headless, proxy, user‑agent et timeout via `.env`
- Interface CLI simple (Typer) pour lancer une commande unique
- Export des résultats au format CSV
- Structure testable avec `pytest`
- Container Docker prêt à l’emploi

## 🛠️ Tech Stack

- Python
- Selenium
- Streamlit
- WebDriver Manager

## ▶️ Lancer le projet

```bash
git clone https://github.com/tonpseudo/aliexpress_scraper_selenium.git
cd aliexpress_scraper_selenium
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
