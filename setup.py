from setuptools import setup

setup(
    name="scrapper_ali",
    version="0.1.0",
    py_modules=["ali_scraper"],
    install_requires=[
        "selenium==4.31.0",
        "streamlit==1.44.1",
        "pandas==2.2.3",
        "webdriver-manager==4.0.2",
    ],
    extras_require={
        "dev": ["pytest>=7.0.0", "black>=24.0.0", "flake8>=5.0.0"]
    },
)
