import database
import interface
import accounts as acc
from utilities import thread_function as tf
import os

connection = database.create_connection("data")
if not os.path.exists('data.sqlite'):
    database.create_table("account", ("id", "summoner_username", "region", "username", "password"))

if not os.path.exists("secret.key"):
    acc.Encryption.generate_key()

accounts = acc.load_accounts()

tf(interface.main, accounts)