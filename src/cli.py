"""
    This handles the command line interface.
    Written by: github.com/CasperDoesCoding
    Date: September / 12 / 2022
"""

from os import system
from database import Database
from account import Account
from logzero import logger, logfile
from datascraper import DataScraper

logfile("debugging.log")

datascraper = DataScraper()
database_connection = Database()
accounts = database_connection.get_all_accounts()
if len(accounts) != 0:
    datascraper.scrape_several_accounts(accounts)


def clear_screen():
    system("cls")


def list_accounts():
    clear_screen()
    for account in accounts:
        print("--------------------")
        print(f"Username: {account.username}")
        print(f"Display Name: {account.display_name}")
        print(f"Region: {account.region}")
        if account.data:
            print(f"Level: {account.data['level']}")
            print(f"Rank: {account.data['rank']}")
        else:
            print(
                "No data available yet either the display name isn't provided or the data is not available yet."  # noqa: E501
            )

    print("--------------------")
    input("Press enter to continue...\n")


def login_to_account():
    clear_screen()
    print("Not implemented yet.")
    input("Press enter to continue...\n")


def add_account():
    clear_screen()
    username = input("Enter the name you login to the account with:\n")
    password = input("Enter the password you login to the account with:\n")
    region = input("Enter the region of the account:\n")
    display_name = input("Enter the display name of the account OPTIONAL:\n")
    account = Account(username, password, region, display_name)
    database_connection.add_account(username, password, region, display_name)
    accounts.append(account)
    datascraper.scrape_account_data(display_name, region)
    input("Press enter to continue...\n")


def delete_account_by_username():
    username = input("Enter the username of the account you want to delete:\n")
    database_connection.remove_account_by_username(username)
    for account in accounts:
        if account.username == username:
            accounts.remove(account)


def delete_account_by_display_name():
    display_name = input("Enter the display name of the account you want to delete:\n")
    database_connection.remove_account_by_display_name(display_name)
    for account in accounts:
        if account.display_name == display_name:
            accounts.remove(account)


def delete_account():
    clear_screen()
    choice = input(
        "Would you like to delete an account by username or display name? (u/d/cancel)\n"  # noqa: E501
    )
    clear_screen()
    if choice == "u":
        delete_account_by_username()
    elif choice == "d":
        delete_account_by_display_name()
    elif choice == "cancel":
        pass
    else:
        delete_account()


def custom_exit():
    clear_screen()
    exit()


choices = {
    "1": list_accounts,
    "list": list_accounts,
    "2": login_to_account,
    "login": login_to_account,
    "3": add_account,
    "add": add_account,
    "4": delete_account,
    "delete": delete_account,
    "5": custom_exit,
    "exit": custom_exit,
}


def list_options():
    print("1. List Accounts")
    print("2. Login to Account")
    print("3. Add Account")
    print("4. Delete Account")
    print("5. Exit")


def main():
    while True:
        clear_screen()
        list_options()
        choice = input("Enter your choice:\n")
        if choice in choices:
            choices[choice]()
        else:
            logger.error("Invalid choice")


if __name__ == "__main__":
    main()
