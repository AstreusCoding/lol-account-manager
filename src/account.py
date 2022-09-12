"""
    This handles the database connection and queries.
    Written by: github.com/CasperDoesCoding
    Date: September / 9 / 2022
"""

# from database import Database
from logzero import logger
from datascraper import DataScraper

datascraper = DataScraper()


class Account:
    def __init__(self, username, password, region, display_name) -> None:
        logger.info("Creating new account object...")
        self.username = username
        self.password = password
        self.region = region
        self.display_name = display_name
        self.data = None

    def get_account_data(self):
        self.data = datascraper.scrape_account_data(
            self.display_name, self.region
        ).result()

    def login(self):
        logger.info("Logging in...")
        pass  # TODO: Implement login
