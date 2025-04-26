"""MEP Dollar Rate"""
from typing import Optional
from bs4 import BeautifulSoup
from .base import DollarRate


class MEPDollar(DollarRate):
    """Dólar MEP (solo venta)"""
    def __init__(self, sell: Optional[float]):
        super().__init__(name='mep', buy=None, sell=sell)

    @classmethod
    def extract_from_html(cls, container: BeautifulSoup) -> 'MEPDollar':
        sell = cls._parse_price(container, is_buy=False)
        return cls(sell=sell)
