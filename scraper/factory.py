"""Factory to create different dollar rate objects."""
from bs4 import BeautifulSoup
from .dollars.base import DollarRate
from .dollars.oficial import OficialDollar
from .dollars.blue import BlueDollar
from .dollars.mep import MEPDollar
from .exceptions import InvalidDollarType

class DollarFactory:
    """Factory class to create different dollar rate objects.
    Arguments:
        dollar_type (str): Type of dollar rate to create ('oficial', 'informal', 'mep').
        container (BeautifulSoup): BeautifulSoup object containing the HTML to parse.
    """
    _dollar_classes = {
        'oficial': OficialDollar,
        'informal': BlueDollar,
        'mep': MEPDollar
    }

    @classmethod
    def create(cls, dollar_type: str, container: BeautifulSoup) -> DollarRate:
        """Creates a dollar rate object based on the type and HTML container.
        Args:
            dollar_type (str): Type of dollar rate to create ('oficial', 'informal', 'mep').
            container (BeautifulSoup): BeautifulSoup object containing the HTML to parse.
        Returns:
            DollarRate: An instance of the appropriate dollar rate class.
        Raises:
            ValueError: If the dollar type is not supported.
        """
        dollar_class = cls._dollar_classes.get(dollar_type)
        if not dollar_class:
            raise InvalidDollarType(f"Invalid dollar type: {dollar_type}")

        if not container:
            return dollar_class(buy=None, sell=None) if dollar_type != 'mep' else dollar_class(sell=None)

        return dollar_class.extract_from_html(container)

