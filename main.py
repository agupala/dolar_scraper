"""Main module - Minimalist version"""
from scraper.scraper import DolaritoScraper
from scraper.config.logger import setup_logger

logger = setup_logger()

def main() -> None:
    """Main function to run the scraper and display rates"""
    try:
        scraper = DolaritoScraper()
        rates = scraper.get_rates()
        
        line_length = 50

        print("\n" + "═" * line_length)
        print("   COTIZACIONES DISPONIBLES DEL DOLAR 💵    ".center(40))
        print("═" * line_length)

        for name, rate in rates.items():
            print(f"- {name.upper()}:".ljust(12), end=" ")
            if rate.buy:
                print(f"Compra: ${rate.buy:.2f}".ljust(15), end=" ")
                print("|", end=" ")
            if rate.sell:
                print(f"Venta: ${rate.sell:.2f}", end="")
            print()  # Salto de línea

        print("═" * line_length + "\n")

    except (ConnectionError, ValueError) as error:
        print(f"\n⚠️ Error: {str(error)}")

if __name__ == "__main__":
    main()
