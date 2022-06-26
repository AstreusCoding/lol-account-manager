import database
import accounts as acc
import os
from dotenv import load_dotenv
from utilities import thread_function as tf

def test_database():
    database.create_connection("test_data")
    database.create_table()
    league_account = acc.Account(1, "asdf", "OCE", "password", "Reese")
    league_account.save()


def test_id_creation():
    database.create_connection("test_data")
    database.create_table()
    for i in range(10):
        league_account = acc.Account(database.count_from_table("account", "id")[0][0], "asdf", "OCE", "password", "Reese")
        print(league_account.id)
        league_account.save()
    sql = database.count_from_table("account", "id")
    for x in sql:
        print(x[0])

def test_path_loadenv():
    with open('.env', 'w') as file:
        file.write('LEAGUE_PATH=D:\Games\League Of Legends\LeagueClient.exe')
    file.close()
    load_dotenv()
    if os.path.exists(os.getenv('LEAGUE_PATH')):
        print("YES")

def test_decoding():
    database.create_connection("data")
    sql_accounts = database.load_all_from_table("account")
    for account in sql_accounts:
        print("password: " + str(account[4]))

def test_check_env():
    with open('.env', 'r') as file:
        if 'LEAGUE_PATH' in file.read():
            print('yes')
        else:
            print('no')


test_check_env()