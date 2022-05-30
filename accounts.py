import database
import webscraper
from utilities import thread_function as tf

accounts = []

def load_accounts():
    global accounts
    sql_accounts = database.load_all_from_table("account")
    for account in sql_accounts:
        account = Account(account[0], account[1], account[2], account[3], account[4])
    return accounts

class Account:
    
    def __init__(self, id: int, username: str = "", region: str = "", password: str = "", summoner_username: str = ""):
        self.id = id
        self.summoner_username = summoner_username
        self.region = region
        self.username = username
        self.password = password
        
        self.data = None
        
        accounts.append(self)
    
    def fetch_summoner_web_data(self):
        if self.summoner_username == "":
            return
        return tf(webscraper.fetch_account_data, self.summoner_username, self.region, None, self)
    
    def save(self):
        database.save_to_table("account", ("id", "summoner_username", "region", "username", "password"), (self.id, self.summoner_username, self.region, self.username, self.password))
        
    def load(self):
        data = database.load_from_table("account", "id", self.id)
        if data is not None:
            self.id = data[0]
            self.summoner_username = data[1]
            self.region = data[2]
            self.username = data[3]
            self.password = data[4]
        else:
            print("Account not found")
            
    def delete(self):
        database.delete_from_table("account", "id", self.id)