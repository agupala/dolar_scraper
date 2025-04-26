"""Unit tests for the scraper module."""

import pytest
from bs4 import BeautifulSoup
from scraper.dollars.oficial import OficialDollar

# HTML de prueba basado en la estructura real de dolarito.ar
TEST_HTML = """
<li id="quotation-oficial-desktop">
    <div class="css-4ywm3s">
        <p class="chakra-text css-113t1jt">$350,50</p>
    </div>
    <div class="css-6g5h8t">
        <p class="chakra-text css-12u0t8b">$355,20</p>
    </div>
</li>
"""

@pytest.fixture
def oficial_container():
    """Fixture que devuelve un contenedor BeautifulSoup para pruebas"""
    return BeautifulSoup(TEST_HTML, 'html.parser')

def test_oficial_creation():
    """Test de creación básica con valores directos"""
    dolar = OficialDollar(buy=350.50, sell=355.20)
    assert dolar.name == 'oficial'
    assert dolar.buy == 350.50
    assert dolar.sell == 355.20

def test_oficial_from_html(oficial_container):
    """Test de extracción desde HTML real"""
    dolar = OficialDollar.extract_from_html(oficial_container)
    
    assert isinstance(dolar, OficialDollar)
    assert dolar.buy == 350.50
    assert dolar.sell == 355.20

def test_oficial_with_missing_data():
    """Test con datos faltantes"""
    dolar = OficialDollar(buy=None, sell=355.20)
    assert dolar.buy is None
    assert dolar.sell == 355.20

def test_oficial_string_representation():
    """Test del formato de string"""
    dolar = OficialDollar(buy=350.50, sell=355.20)
    assert str(dolar) == "Oficial Dollar: Buy: 350.5, Sell: 355.2"

def test_oficial_with_empty_container():
    """Test con contenedor vacío"""
    empty_container = BeautifulSoup("<li></li>", 'html.parser')
    dolar = OficialDollar.extract_from_html(empty_container)
    
    assert dolar.buy is None
    assert dolar.sell is None

def test_oficial_with_malformed_data():
    """Test con datos mal formados"""
    malformed_html = """
    <li id="quotation-oficial-desktop">
        <div class="wrong-class">
            <p>invalid</p>
        </div>
    </li>
    """
    container = BeautifulSoup(malformed_html, 'html.parser')
    dolar = OficialDollar.extract_from_html(container)
    
    assert dolar.buy is None
    assert dolar.sell is None
