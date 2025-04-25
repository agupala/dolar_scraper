"""Main module to demonstrate the functionality of the DolaritoScraper."""
import logging
import requests
from dolar_scraper.scraper import DolaritoScraper

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main function to demonstrate the scraper functionality."""
    scraper = DolaritoScraper()
    try:
        rates = scraper.get_rates()
        for rate in rates.values():
            logger.info(rate)
    except (requests.RequestException, ValueError) as error:
        logger.error("Failed to get rates due to a network or parsing error: %s", error)


if __name__ == '__main__':
    main()