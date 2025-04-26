"""Base class for dollar rate scrapers"""
from typing import Dict
import requests
from bs4 import BeautifulSoup
from scraper.factory import DollarFactory
from scraper.dollars.base import DollarRate
from .config.logger import setup_logger

logger = setup_logger()

class DolaritoScraper:
    """Scraper for Dolarito website"""
    BASE_URL = "https://www.dolarito.ar/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (...)'
        })

    def _fetch_page(self) -> BeautifulSoup:
        try:
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as error:
            logger.error("Error fetching page: %s", error)
            raise

    def get_rates(self) -> Dict[str, DollarRate]:
        """Fetches and returns the dollar rates"""
        soup = self._fetch_page()
        return {
            'oficial': DollarFactory.create('oficial',soup.find('li', id='quotation-oficial-desktop')),
            'blue': DollarFactory.create('informal', soup.find('li', id='quotation-informal-desktop')),  
            'mep': DollarFactory.create('mep', soup.find('li', id='quotation-mep-desktop'))
        }
