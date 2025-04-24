"""Module for scraping exchange rates from dolarito.ar."""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
from utils.logger import get_logger

logger = get_logger(__name__)

class DolarScraper:
    """A class to scrape dollar exchange rates from dolarito.ar."""

    def __init__(self, url: str) -> None:
        """
        Initialize the scraper with a URL.

        Args:
            url (str): The URL to scrape data from.
        """
        self.url = url
        self.data: Dict[str, Dict[str, str]] = {}

    def fetch_html(self) -> str:
        """
        Fetch HTML content from the URL.

        Returns:
            str: HTML content of the page.
        """
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        return response.text

    def parse_quotation_block(self, soup: BeautifulSoup, block_id: str, name: str) -> None:
        """
        Parse a specific block of the page to extract exchange rate data.

        Args:
            soup (BeautifulSoup): Parsed HTML soup.
            block_id (str): ID of the HTML block.
            name (str): Name for the currency type.
        """
        block = soup.find("ul", {"id": block_id})
        if block is None:
            logger.warning("Block not found: %s", block_id)
            return

        buy_price: Optional[str] = None
        sell_price: Optional[str] = None

        labels = block.find_all("div", class_="chakra-text css-1hexnl9")
        for label in labels:
            if "Vendé a" in label.text:
                value_div = label.find_next("div", class_="chakra-skeleton css-ahyunb")
                value_tag = value_div.find("p", class_="chakra-text css-113t1jt") if value_div else None
                sell_price = value_tag.text.strip() if value_tag else None
            elif "Comprá a" in label.text:
                value_div = label.find_next("div", class_="chakra-skeleton css-ahyunb")
                value_tag = value_div.find("p", class_="chakra-text css-12u0t8b") if value_div else None
                buy_price = value_tag.text.strip() if value_tag else None

        if buy_price and sell_price:
            self.data[name] = {"compra": buy_price, "venta": sell_price}
        else:
            logger.warning("Incomplete data for: %s", name)

    def parse_data(self, html: str) -> None:
        """
        Parse HTML content to extract all desired currency data.

        Args:
            html (str): Raw HTML content.
        """
        soup = BeautifulSoup(html, 'html.parser')
        self.parse_quotation_block(soup, "quotation-oficial-desktop", "Official Dollar")
        self.parse_quotation_block(soup, "quotation-informal-desktop", "Blue Dollar")
        self.parse_quotation_block(soup, "quotation-mep-desktop", "MEP Dollar")

    def get_data(self) -> Dict[str, Dict[str, str]]:
        """
        Retrieve all parsed data.

        Returns:
            dict: Dictionary with currency data.
        """
        html = self.fetch_html()
        self.parse_data(html)
        return self.data

    def display_data(self) -> None:
        """Log all extracted data to the console."""
        for currency, values in self.data.items():
            logger.info("%s -> Buy: %s | Sell: %s", currency, values['compra'], values['venta'])