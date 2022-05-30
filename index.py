import database
import interface
from accounts import Account, load_accounts
from utilities import thread_function as tf

connection = database.create_connection("data")
database.create_table("account", ("id", "summoner_username", "region", "username", "password"))

accounts = load_accounts()

account = Account(1, "test", "euw", "test", "test")
account.load()
account.username = "test3"
account.save()
account.fetch_summoner_web_data()

tf(interface.main, accounts)