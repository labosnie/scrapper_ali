import os
from dotenv import load_dotenv

# Charge les variables d’environnement depuis un .env à la racine
load_dotenv()

# Mode headless (True/False)
HEADLESS = os.getenv("HEADLESS", "True").lower() in ("true", "1", "yes")

# Proxy à utiliser (ex. "http://user:pass@host:port"), ou None
PROXY = os.getenv("PROXY", None)

# User‑Agent personnalisé, ou None
USER_AGENT = os.getenv("USER_AGENT", None)

# Timeout global pour Selenium (en secondes)
TIMEOUT = int(os.getenv("TIMEOUT", 30))
