import subprocess
import time
import database
import webscraper
from utilities import thread_function as tf
from cryptography.fernet import Fernet

from pynput.keyboard import Key, Controller
keyboard = Controller()

REGULAR_PATH = "D:\\Games\\League Of Legends\\LeagueClient.exe"

accounts = []

def load_accounts():
    global accounts
    encryption = Encryption()
    sql_accounts = database.load_all_from_table("account")
    for account in sql_accounts:
        account = Account(id=account[0], summoner_username=account[1], region=account[2], username=account[3], password=account[4])
    return accounts

class Account:
    
    def __init__(self, id: int, username: str = "", region: str = "", password: str = "", summoner_username: str = ""):
        self.id = id
        self.summoner_username = summoner_username
        self.region = region
        self.username = username
        self.password = password
        
        self.data = None
        
        self.fetch_summoner_web_data()
        accounts.append(self)
    
    def fetch_summoner_web_data(self):
        if self.summoner_username == "":
            print("No username provided.")
            return
        return tf(webscraper.fetch_account_data, self.summoner_username, self.region, None, self)
    
    def save(self):
        encryption = Encryption()
        print(self.password)
        encrypted = encryption.encrypt_message(self.password)
        print(encrypted)
        database.save_to_table("account", ("id", "summoner_username", "region", "username", "password"), (self.id, self.summoner_username, self.region, self.username, encrypted))

    def load(self):
        encryption = Encryption()
        data = database.load_from_table("account", "id", self.id)
        if data is not None:
            self.id = data[0]
            self.summoner_username = data[1]
            self.region = data[2]
            self.username = encryption.decrypt_message(data[3])
            self.password = data[4]
        else:
            print("Account not found")
            
    def delete(self):
        database.create_connection("data")
        database.delete_from_table("account", "id", self.id)
        
    def login(self):
        subprocess.call(REGULAR_PATH)
        time.sleep(2.5)
        keyboard.type(self.username)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(0.25)
        keyboard.type(self.password)
        time.sleep(0.25)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)


class Encryption:
    def generate_key():
        """
        Generates a key and save it into a file
        """
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        """
        Load the previously generated key
        """
        return open("secret.key", "rb").read()

    def encrypt_message(self, message: str):
        """
        Encrypts a message
        """
        key = self.load_key()
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)

        return encrypted_message

    def decrypt_message(self, encrypted_message):
        """
        Decrypts an encrypted message
        """
        key = self.load_key()
        f = Fernet(key)
        decrypted_message = f.decrypt(encrypted_message)

        return decrypted_message.decode()