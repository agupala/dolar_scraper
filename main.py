"""Main module - Minimalist version"""
from scraper.scraper import DolaritoScraper
from scraper.config.logger import setup_logger

logger = setup_logger()

def mostrar_cotizaciones() -> None:
    """Function to display current dollar rates"""
    logger.info("Fetching current dollar rates...")
    try:
        scraper = DolaritoScraper()
        cotizaciones = scraper.get_rates()

        print("\n" + "═"*40)
        print("   COTIZACIONES ACTUALES   ".center(40))
        print("═"*40)

        # Oficial
        print("\n • OFICIAL".ljust(12) +
              f"Compra: ${cotizaciones['oficial'].buy:.2f}".ljust(20) +
              f"Venta: ${cotizaciones['oficial'].sell:.2f}")

        # Blue
        print(" • BLUE".ljust(12) +
              f"Compra: ${cotizaciones['blue'].buy:.2f}".ljust(20) +
              f"Venta: ${cotizaciones['blue'].sell:.2f}")

        # MEP (solo venta)
        print(" • MEP".ljust(12) +
              "".ljust(20) +
              f"Venta: ${cotizaciones['mep'].sell:.2f}")

        print("═"*40 + "\n")

    except (KeyError, AttributeError) as error:
        logger.error("Error displaying rates")
        logger.error("%s: %s", type(error).__name__, error)

if __name__ == "__main__":
    mostrar_cotizaciones()
