"""
    This handles the main program loop.
    Written by: github.com/CasperDoesCoding
    Date: September / 9 / 2022
"""
from database import Database
from logzero import logger


def test():
    new_db = Database()
    account = new_db.get_account_by_id("1")
    logger.info(account.username)
    # new_account = Account(account[1], account[2])
    # logger.info(new_account.username)


if __name__ == "__main__":
    test()
