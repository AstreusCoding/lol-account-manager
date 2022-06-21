import database
import accounts as acc
from utilities import thread_function as tf

connection = database.create_connection("test_data")
database.create_table()
league_account = acc.Account(1, "asdf", "OCE", "password", "Reese")

league_account.save()
