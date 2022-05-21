import json
from random import randint
from os import path, mkdir, listdir
from json import dumps
from shutil import rmtree
from utilities import obscure, unobscure
from enum import Enum, auto
import time
import subprocess

from tabulate import tabulate
from pynput.keyboard import Key, Controller

import threading
from datetime import datetime
import scraper

main_dir: str = "./src/"
data_folder: str = main_dir + "account_data/"
keyboard = Controller()

loaded_accounts = []

##rmtree(data_folder)
if not path.exists(data_folder):
    mkdir(data_folder)

class ServerRegion(Enum):
    """All available regions in league of legends"""
    
    EUW = auto()
    EUNE = auto()
    RU = auto()

def load_accounts():
    for account_id in listdir(data_folder):
        if path.exists(f"{data_folder}{account_id}/main.json"):
            with open(f"{data_folder}{account_id}/main.json", "r") as file:
                account_json = json.load(file)
                
                loaded_account = Account(
                    id = account_id,
                    region = ServerRegion[str.upper(account_json["region"])],
                    summoner_username = account_json["summoner_username"],
                    username = account_json["username"],
                    password = account_json["password"]
                )

                loaded_accounts.append(loaded_account)
                threading.Thread(target=loaded_account.update_data).start()


class Account:

    statistics = {
        "level": "Unknown",
        "rank": "Unknown",
        "games_played": "Unknown"
    }
    
    def __init__(self, *, id: int = None, summoner_username: str = "", username: str, password: str, region: ServerRegion):
        
        if id is None:
            id = randint(1, 99999999999)

        self.id = id
        self.region = region
        self.summoner_username = summoner_username
        
        self.username = username
        self.password = password

        self.deleted = False

        self.directory = f"{data_folder}{str(self.id)}/"
        if not path.exists(self.directory):
            mkdir(self.directory)
            with open(f"{self.directory}main.json", "w") as file:
                file.write(dumps(
                    {
                        "region": str(self.region.name),
                        "summoner_username": self.summoner_username,
                        "username": self.username,
                        "password": obscure(self.password.encode()).decode(),
                    }
                    , indent = 4))
        else:
            self.password = unobscure(password.encode()).decode()

        if path.exists(f"{self.directory}recent_data.json"):
            with open(f"{self.directory}recent_data.json", "r") as file:
                self.statistics = json.load(file)
        else:
            with open(f"{self.directory}recent_data.json", "w") as file:
                file.write(dumps(self.statistics, indent = 4))
   
    def login(self):
        subprocess.call(["C:\Riot Games\League of Legends\LeagueClient.exe"])
        time.sleep(2.5)
        keyboard.type(self.username)
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(0.25)
        keyboard.type(self.password)
    
    def remove(self):
        if path.exists(self.directory):
            rmtree(self.directory)
        self.deleted = True
    
    def update_data(self):
        if self.summoner_username == "":
            return
        
        soup, summoner_data = scraper.load_summoner_page(str.lower(self.region.name), self.summoner_username)
        self.statistics = {
            "level": summoner_data["level"],
            "rank": summoner_data["rank"],
            "games_played": summoner_data["games_played"],
            "data_fetched": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        }
        
        with open(f"{self.directory}recent_data.json", "w") as file:
                file.write(dumps(self.statistics, indent = 4))
