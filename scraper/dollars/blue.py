"""Base class for dollar rate scrapers"""
from typing import Optional, Dict
from .base import DollarRate

class BlueDollar(DollarRate):
    """Dólar Blue (informal)"""
    def __init__(self, buy: Optional[float], sell: Optional[float]):
        super().__init__(name='blue', buy=buy, sell=sell)

    @classmethod
    def extract_from_html(cls, container: Dict[str, str]) -> 'BlueDollar':
        """Extracts the buy and sell prices from the HTML container."""
        buy = cls._parse_price(container, is_buy=True)
        sell = cls._parse_price(container, is_buy=False)
        return cls(buy=buy, sell=sell)