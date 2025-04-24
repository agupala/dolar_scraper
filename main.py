from scraper import DolarScraper

if __name__ == "__main__":
    url = "https://www.dolarito.ar/"
    scraper = DolarScraper(url)
    scraper.get_data()
    scraper.display_data()