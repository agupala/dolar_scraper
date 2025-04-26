"""Exceptions for the package."""

class ScraperError(Exception):
    """Base exception for scraper-related errors"""


class InvalidDollarType(ScraperError):
    """Invalid dollar type requested"""


class ScrapingError(ScraperError):
    """Error during scraping operation"""
