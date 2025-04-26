"""Base class for dollar rate scrapers"""
from dataclasses import dataclass
from typing import Optional
from bs4 import BeautifulSoup
from ..config.logger import setup_logger

logger = setup_logger()

@dataclass
class DollarRate:
    """Class representing a dollar rate"""
    name: str
    buy: Optional[float] = None
    sell: Optional[float] = None

    @classmethod
    def extract_from_html(cls, container: BeautifulSoup) -> 'DollarRate':
        """Method to extract dollar rates from HTML"""
        raise NotImplementedError

    @staticmethod
    def _parse_price(container: BeautifulSoup, is_buy: bool) -> Optional[float]:
        """Method to parse the price from the HTML container"""
        try:
            div_class = 'css-4ywm3s' if is_buy else 'css-6g5h8t'
            p_class = 'chakra-text css-113t1jt' if is_buy else 'chakra-text css-12u0t8b'

            price_div = container.find('div', class_=div_class)
            if not price_div:
                return None

            price_element = price_div.find('p', class_=p_class)
            if not price_element:
                return None

            price_text = price_element.get_text()
            return float(price_text.replace('$', '').replace('.', '').replace(',', '.').strip())

        except (ValueError, AttributeError) as error:
            logger.error("Error parsing price: %s", error)
            return None
