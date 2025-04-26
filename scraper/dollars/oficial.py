"""Oficial Dollar"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import DollarRate

class OficialDollar(DollarRate):
    """Oficial Dollar Rate"""
    def __init__(self, buy: Optional[float], sell: Optional[float]):
        super().__init__(name='oficial', buy=buy, sell=sell)

    @classmethod
    def extract_from_html(cls, container: BeautifulSoup) -> 'OficialDollar':
        buy = cls._parse_price(container, is_buy=True)
        sell = cls._parse_price(container, is_buy=False)
        return cls(buy=buy, sell=sell)
