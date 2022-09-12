from src.database import Database
from src.datascraper import DataScraper

# from src.account import Account
from logzero import logger  # noqa: F401

test_accounts = [
    ("root2", "sysadmin", "euw", "test"),
    ("root", "sysadmin", "euw", "casper"),
    ("root5", "sysadmin", "euw", "jonathan"),
    ("root6", "sysadmin", "euw", "scripter"),
]


def test_test_func():
    new_db = Database()
    datascraper = DataScraper()
    accounts = new_db.get_all_accounts()

    datascraper.scrape_several_accounts(accounts)

    for account in accounts:
        logger.info(f"{account.display_name}   {account.data}")
