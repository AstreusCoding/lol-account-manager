import database
import interface
from accounts import load_accounts
from utilities import thread_function as tf

connection = database.create_connection("data")
database.create_table("account", ("id", "summoner_username", "region", "username", "password"))

accounts = load_accounts()

tf(interface.main, accounts)