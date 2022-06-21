import database
import interface
import accounts as acc
from utilities import thread_function as tf
import os

database.create_connection("data")
database.create_table()

if not os.path.exists("secret.key"):
    acc.Encryption.generate_key()

accounts = acc.load_accounts()

tf(interface.main, accounts)