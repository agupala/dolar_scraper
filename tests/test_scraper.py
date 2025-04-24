import pytest
from scraper import DolarScraper

@pytest.fixture
def scraper():
    return DolarScraper("https://www.dolarito.ar/")

def test_fetch_html(scraper):
    html = scraper.fetch_html()
    assert "<html" in html.lower()

def test_parse_data(scraper):
    html = scraper.fetch_html()
    scraper.parse_data(html)
    data = scraper.data

    assert any(key in data for key in ["Dólar Oficial", "Dólar Blue", "Dólar MEP"])

    for key in data:
        assert "compra" in data[key]
        assert "venta" in data[key]
        assert data[key]["compra"] != ""
        assert data[key]["venta"] != ""