"""
Module for scraping dollar exchange rates from dolarito.ar website.
"""
from dataclasses import dataclass
from typing import Optional
import requests
from bs4 import BeautifulSoup


@dataclass
class DollarRate:
    """
    Data class to store dollar exchange rate information.

    Attributes:
        name (str): Name of the dollar type (e.g., 'official', 'blue', 'mep')
        buy (Optional[float]): Buy price in ARS
        sell (Optional[float]): Sell price in ARS
    """
    name: str
    buy: Optional[float]
    sell: Optional[float]

    def __str__(self) -> str:
        return f"{self.name.title()} - Buy: {self.buy}, Sell: {self.sell}"


class DolaritoScraper:
    """
    Scraper for dolarito.ar website to get dollar exchange rates.

    Methods:
        get_rates(): Retrieves all dollar rates from the website
    """

    BASE_URL = "https://www.dolarito.ar/"

    def __init__(self) -> None:
        """Initialize the scraper with a requests session."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/91.0.4472.124 Safari/537.36'
        })

    def _fetch_page(self) -> BeautifulSoup:
        """
        Fetch the dolarito.ar webpage and return parsed HTML.

        Returns:
            BeautifulSoup: Parsed HTML content

        Raises:
            requests.RequestException: If there's an error fetching the page
        """
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            logger.error("Error fetching page: %s", e)
            raise

    def _extract_rate(self, soup: BeautifulSoup, dollar_type: str) -> DollarRate:
        """
        Extrae tasas de compra/venta para un tipo de dólar específico.
        """
        container = soup.find('li', id=f"quotation-{dollar_type}-desktop")
        if not container:
            logger.warning("Container for %s not found", dollar_type)
            return DollarRate(dollar_type, None, None)

        return DollarRate(
            name=dollar_type,
            buy=self._parse_price(container, is_buy=True),  # Precio de compra
            sell=self._parse_price(container, is_buy=False)  # Precio de venta
        )


    def _parse_price(self, container: BeautifulSoup, is_buy: bool) -> Optional[float]:
        """
        Extrae el precio de compra o venta del contenedor principal.
        
        Args:
            container: Contenedor BeautifulSoup del elemento <li>
            is_buy: True para precio de compra, False para venta
        
        Returns:
            Precio como float o None si no se encuentra
        """
        try:
            # Selecciona el div correcto según compra/venta
            price_div = container.find('div', class_='css-4ywm3s' if is_buy else 'css-6g5h8t')
            if not price_div:
                return None

            # Encuentra el elemento que contiene el precio numérico
            price_element = price_div.find('p', class_='chakra-text css-113t1jt' if is_buy else 'chakra-text css-12u0t8b')
            if not price_element:
                return None

            # Limpia y convierte el texto
            price_text = price_element.get_text()
            return float(price_text.replace('$', '').replace('.', '').replace(',', '.').strip())


        except (ValueError, AttributeError) as e:
            logger.error("Error parsing price: %s", e)
            return None


    def get_rates(self) -> dict[str, DollarRate]:
        """
        Get all dollar rates from the website.

        Returns:
            dict[str, DollarRate]: Dictionary mapping dollar types to their rates
        """
        soup = self._fetch_page()
        return {
            'oficial': self._extract_rate(soup, 'oficial'),
            'informal': self._extract_rate(soup, 'informal'),
            'mep': self._extract_rate(soup, 'mep')
        }
