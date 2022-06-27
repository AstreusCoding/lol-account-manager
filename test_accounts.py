import database
import accounts as acc
import os
import unittest
from dotenv import load_dotenv
from utilities import thread_function as tf

class TestAccounts(unittest.TestCase):
    def test_database(self):
        database.create_connection("test_data")
        database.wipe_database()
        database.create_table()
        league_account = acc.Account(1, "asdf", "OCE", "password", "Reese")
        league_account.save()
        self.assertEqual(database.count_from_table("account", "id")[0][0], 1)

    def test_id_creation(self):
        database.create_connection("test_data")
        database.wipe_database()
        database.create_table()
        for i in range(10):
            league_account = acc.Account(database.count_from_table("account", "id")[0][0], "asdf", "OCE", "password", "Reese")
            league_account.save()
        self.assertEqual(database.count_from_table("account", "id")[0][0], 10)

    def test_path_loadenv(self):
        with open('.env', 'w') as file:
            file.write('LEAGUE_PATH=D:\Games\League Of Legends\LeagueClient.exe')
        file.close()
        load_dotenv()
        self.assertTrue(os.path.exists(os.getenv('LEAGUE_PATH')))

    def test_check_env(self):
        with open('.env', 'r') as file:
            self.assertTrue('LEAGUE_PATH' in file.read())


if __name__ == "__main__":
    unittest.main()