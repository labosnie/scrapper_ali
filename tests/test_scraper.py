import pytest
from src.ali_scraper.ali_scraper import AliExpressScraper


def test_scrape_zero_items():
    """
    Test pour vérifier le comportement de la fonction scrape lorsque max_items est 0.
    """
    scraper = AliExpressScraper()
    results = scraper.scrape("montre connectée", max_items=0)
    assert isinstance(results, list)
    assert results == []


def test_scrape_invalid_items():
    """
    Test pour vérifier le comportement de la fonction scrape lorsque max_items est négatif.
    """
    scraper = AliExpressScraper()
    results = scraper.scrape("http://example.com", max_items=5)
    assert isinstance(results, list)
    assert results == []    