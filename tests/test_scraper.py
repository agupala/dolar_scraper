"""
Unit tests for the dolarito.ar scraper.
"""
import pytest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from dolar_scraper.scraper import DolaritoScraper, DollarRate

SAMPLE_HTML = """
<html>
    <body>
        <li id="quotation-oficial-desktop">
            <div class="css-0">
                <div class="chakra-text css-1hexnl9">Comprá a:</div>
                <div><p class="css-113t1jt">1.140</p></div>
            </div>
            <div class="css-0">
                <div class="chakra-text css-1hexnl9">Vendé a:</div>
                <div><p class="css-12u0t8b">1.190</p></div>
            </div>
        </li>
        <li id="quotation-blue-desktop">
            <div class="css-0">
                <div class="chakra-text css-1hexnl9">Comprá a:</div>
                <div><p class="css-113t1jt">1.240</p></div>
            </div>
            <div class="css-0">
                <div class="chakra-text css-1hexnl9">Vendé a:</div>
                <div><p class="css-12u0t8b">1.290</p></div>
            </div>
        </li>
        <li id="quotation-mep-desktop">
            <div class="css-0">
                <div class="chakra-text css-1hexnl9">Comprá a:</div>
                <div><p class="css-113t1jt">1.340</p></div>
            </div>
            <div class="css-0">
                <div class="chakra-text css-1hexnl9">Vendé a:</div>
                <div><p class="css-12u0t8b">1.390</p></div>
            </div>
        </li>
    </body>
</html>
"""


@pytest.fixture
def mock_successful_request():
    """Fixture for mocking successful HTTP request."""
    with patch('requests.Session.get') as mock_get:
        mock_response = MagicMock()
        mock_response.text = SAMPLE_HTML
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        yield mock_get


@pytest.fixture
def mock_failed_request():
    """Fixture for mocking failed HTTP request."""
    with patch('requests.Session.get') as mock_get:
        mock_get.side_effect = Exception("Request failed")
        yield mock_get


def test_dollar_rate_str_representation():
    """Test the string representation of DollarRate."""
    rate = DollarRate("official", 100.0, 105.0)
    assert str(rate) == "Official - Buy: 100.0, Sell: 105.0"


def test_fetch_page_success(mock_successful_request):
    """Test successful page fetch."""
    scraper = DolaritoScraper()
    soup = scraper._fetch_page()
    assert isinstance(soup, BeautifulSoup)
    mock_successful_request.assert_called_once()


def test_fetch_page_failure(mock_failed_request):
    """Test failed page fetch."""
    scraper = DolaritoScraper()
    with pytest.raises(Exception):
        scraper._fetch_page()
    mock_failed_request.assert_called_once()


def test_extract_rate_success(mock_successful_request):
    """Test successful rate extraction."""
    scraper = DolaritoScraper()
    soup = scraper._fetch_page()
    rate = scraper._extract_rate(soup, 'oficial')
    assert rate.name == 'oficial'
    assert rate.buy == 1.140
    assert rate.sell == 1.190


def test_extract_rate_not_found(mock_successful_request):
    """Test rate extraction when element is not found."""
    scraper = DolaritoScraper()
    soup = scraper._fetch_page()
    rate = scraper._extract_rate(soup, 'nonexistent')
    assert rate.name == 'nonexistent'
    assert rate.buy is None
    assert rate.sell is None


def test_parse_price_valid():
    """Test parsing a valid price."""
    scraper = DolaritoScraper()
    soup = BeautifulSoup("""
        <div class="css-0">
            <div class="chakra-text css-1hexnl9">Comprá a:</div>
            <div><p class="css-113t1jt">1.140</p></div>
        </div>
    """, 'html.parser')
    section = soup.find('div', class_='css-1hexnl9')
    price = scraper._parse_price(section)
    assert price == 1.140


def test_parse_price_invalid():
    """Test parsing an invalid price."""
    scraper = DolaritoScraper()
    soup = BeautifulSoup("""
        <div class="css-0">
            <div class="chakra-text css-1hexnl9">Comprá a:</div>
            <div><p class="css-113t1jt">invalid</p></div>
        </div>
    """, 'html.parser')
    section = soup.find('div', class_='css-1hexnl9')
    price = scraper._parse_price(section)
    assert price is None


def test_get_rates(mock_successful_request):
    """Test getting all rates."""
    scraper = DolaritoScraper()
    rates = scraper.get_rates()
    assert len(rates) == 3
    assert rates['official'].name == 'oficial'
    assert rates['blue'].name == 'blue'
    assert rates['mep'].name == 'mep'