"""Main module - Minimalist version"""
from scraper.scraper import DolaritoScraper
from scraper.config.logger import setup_logger

logger = setup_logger()

def main() -> None:
    """Main function to run the scraper and display rates"""
    try:
        scraper = DolaritoScraper()
        rates = scraper.get_rates()

        print("\n" + "═" * 40)
        print("   COTIZACIONES DISPONIBLES   ".center(40))
        print("═" * 40)

        for name, rate in rates.items():
            print(f"- {name.upper()}:".ljust(12), end=" ")
            if rate.buy:
                print(f"Compra: ${rate.buy:.2f}".ljust(15), end=" ")
            if rate.sell:
                print(f"Venta: ${rate.sell:.2f}", end="")
            print()  # Salto de línea

        print("═" * 40 + "\n")

    except Exception as e:
        print(f"\n⚠️ Error: {str(e)}")

if __name__ == "__main__":
    main()
