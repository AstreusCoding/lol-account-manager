import json
import time
import subprocess
import threading
import os
import random

import scraper
import utilities

import PySimpleGUI as gui

from tabulate import tabulate
from pynput.keyboard import Key, Controller

keyboard = Controller()

global_account_data = None
cached_account_data = {}
active_threads = {}

def load_account_to_cache(account, thread_number):
    account_data = global_account_data[str(account)]
    
    try:
        unobscured_password = utilities.unobscure(str(account_data["password"]).encode()).decode()
    except:
        unobscured_password = str(account_data["password"])
    
    new_account_data = {
        "account_stats": {
            "summoner_name": account_data["login_name"],
            "level": "Unknown",
            "region": "Unknown",
            "rank": "Unknown",
            "games_played": "Unknown"
        },
        "account_info": {
            "id": account,
            "username": account_data["login_name"],
            "password": unobscured_password
        }
    }

    if account_data["summoner_name"] != "":
        soup, summoner_data = scraper.load_summoner_page(account_data["region"], account_data["summoner_name"])
        new_account_data["account_stats"] = {
            "summoner_name": account_data["summoner_name"],
            "level": summoner_data["level"],
            "region": account_data["region"],
            "rank": summoner_data["rank"],
            "games_played": summoner_data["games_played"]
        }
    
    cached_account_data[str(account)] = new_account_data

    if thread_number != None:
        time.sleep(0.1)
        active_threads.pop(thread_number, None)

def load_data():
    global global_account_data
    if not os.path.exists("./account_data.json"):
        with open("account_data.json", "w") as file:
            global_account_data = {}
            file.write(json.dumps(global_account_data, indent = 4))
    else:
        with open("account_data.json", "r") as file:
            global_account_data = json.load(file)
            
    for account in global_account_data:
        thread = threading.Thread(target=load_account_to_cache, args=(account, len(active_threads)))
        active_threads[len(active_threads)] = thread
        
    for thread_number in active_threads:
        active_threads[thread_number].start()

def delete_account(account_id):
    if global_account_data[str(int(account_id))]:
        global_account_data.pop(str(int(account_id)))
    if cached_account_data[str(account_id)]:
        cached_account_data.pop(str(account_id))
    with open("account_data.json", "w") as file:
        file.write(json.dumps(global_account_data, indent = 4))

def login_account(account_id):
    account_data = cached_account_data[str(int(account_id))]
    if account_data:
        subprocess.call(["C:\Riot Games\League of Legends\LeagueClient.exe"])
        time.sleep(2.5)
        keyboard.type(account_data["account_info"]["username"])
        keyboard.press(Key.tab)
        keyboard.release(Key.tab)
        time.sleep(0.25)
        keyboard.type(account_data["account_info"]["password"])
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

def clear_accounts():
    global global_account_data
    global cached_account_data
    global_account_data = {}
    cached_account_data = {}
    with open("account_data.json", "w") as file:
        file.write(json.dumps(global_account_data))

def add_account_list():
    layout = [
        [gui.Text("name:password")],
        [gui.Input("", key="-list-")],
        [gui.Button("submit", key="-submit-")]
    ]
    window = gui.Window("add by list", layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break
            
        if event == "-submit-":
            account_list = values["-list-"].splitlines()
            for account in account_list:
                random_number = random.randint(1, 99999999999)
                username, password = account.split(":")
                global_account_data[str(random_number)] = {
                    "region": "",
                    "summoner_name": "",
                    "login_name": username,
                    "password": utilities.obscure(str(password).encode()).decode()
                }
                load_account_to_cache(str(random_number), None)
            gui.popup("Accounts have been successfully added!")
            window.close()

def add_account():
    layout = [
        [gui.Text("Region Name")],
        [gui.Input("", key="-region-")],
        [gui.Text("Summoner Name")],
        [gui.Input("", key="-summoner-")],
        [gui.Text("Username")],
        [gui.Input("", key="-username-")],
        [gui.Text("Password")],
        [gui.Input("", password_char="*", key="-password-")],
        [gui.Button("submit", key="-submit-")],
        [gui.Button("add by list", key="-add_list-")]
    ]
    window = gui.Window("add account", layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break
        
        if event == "-add_list-":
            window.close()
            add_account_list()
            return
                    
        if event == "-submit-":
            random_number = random.randint(1, 99999999999)
            
            if values["-summoner-"] != "":
                account_page = scraper.load_summoner_page(values["-region-"], values["-summoner-"])
                if not account_page:
                    gui.popup("This summoner name is not connected to any account!")
                    return
                
            global_account_data[str(random_number)] = {
                "region": values["-region-"],
                "summoner_name": values["-summoner-"],
                "login_name": values["-username-"],
                "password": utilities.obscure(str(values["-password-"]).encode()).decode()
            }

            load_account_to_cache(str(random_number),  None)
            with open("account_data.json", "w") as file:
                file.write(json.dumps(global_account_data, indent = 4))
                
            gui.popup("Account has successfully been added!")
                
            window.close()

def fix_data_file():
    global global_account_data
    fix_data_layout = [
        [gui.Text("Are you certain you want to do this? You should only do this if your account data file is not using obscured password saving, otherwise you will end up breaking your entire data file. I recommend backing up your account data file.")],
        [gui.Button("Continue", key="-continue-")],
        [gui.Button("Cancel", key="-cancel-")]
    ]
    
    fix_data_window = gui.Window("Fix Data File", fix_data_layout, modal=True)
    
    while True:
        event, values = fix_data_window.read(100)

        if event == gui.WIN_CLOSED:
            return False
        
        if event == "-continue-":
            for account in global_account_data:
                global_account_data[account]["password"] = utilities.obscure(global_account_data[account]["password"].encode()).decode()
                
            with open("account_data.json", "w") as file:
                file.write(json.dumps(global_account_data, indent = 4))
            fix_data_window.close()
        if event == "-cancel-":
            fix_data_window.close()

def setup():
    global global_account_data
    load_data()

    thread_amount = len(active_threads)
    loading_window_layout = [
        [gui.ProgressBar(thread_amount, orientation = "h", size = (50 , 20), key = "-progressbar-")],
    ]
    
    loading_window = gui.Window("Loading Program", loading_window_layout, icon="logo.ico")
    
    while True:
        event, values = loading_window.read(100)

        if event == gui.WIN_CLOSED:
            return False
        
        loading_window["-progressbar-"].update(len(cached_account_data))
        
        if len(cached_account_data) == thread_amount:
            loading_window.close()
            break
         
def main():
    global global_account_data
    global cached_account_data
    if len(active_threads) > 0: # should not even happen, but checking just in case.
        time.sleep(1)
        main()
        return

    headings = [
        ["ID", (2,1), ""],
        ["Name", (14,1), ""],
        ["Level", (10,1), ""],
        ["Region", (10,1), ""],
        ["Rank", (10,1), ""],
        ["Games 30D", (10,1), " games"]]
    
    layout_header =  [[gui.Text(header[0], size=header[1], background_color="Gray") for header in headings]]
    
    output_rows = []
    login_dict = {}
    delete_dict = {}
    total_games_played = 0

    #print(json.dumps(cached_account_data, indent = 4))
    for account in cached_account_data:
        account_stats = cached_account_data[str(account)]["account_stats"]
        account_info = cached_account_data[str(account)]["account_info"]
        
        output_row = []
        
        output_row.append(gui.Text(str(len(output_rows) + 1), size=(2, 1)))
        
        for data in account_stats:
            if account_stats["level"] == "Unknown":
                output_row.append(gui.Text(str(account_stats[data]), size=headings[len(output_row)][1], background_color = "Blue"))
            else:
                output_row.append(gui.Text(str(account_stats[data]) + str(headings[len(output_row)][2]), size=headings[len(output_row)][1], background_color = "Navy Blue"))
                
        if str(account_stats["games_played"]).isnumeric():
            total_games_played += int(account_stats["games_played"])
        
        login_dict["-login " + str(account_info["id"]) + "-"] = str(account_info["id"])
        delete_dict["-delete " + str(str(account_info["id"])) + "-"] = str(account_info["id"])
        
        output_row.append(gui.Button("Login", size=(10,1), key="-login " + str(account_info["id"]) + "-"))
        output_row.append(gui.Button("Delete", size=(10,1), key="-delete " + str(account_info["id"]) + "-"))
        output_rows.append(output_row)
   
    bottom_layout = [
        [gui.Button("Add Account", size=(10,1), key="-add_account-"),
         gui.Button("Clear Accounts", size=(12,1), key="-clear_accounts-"),
         gui.Button("Fix DATA File", size=(14,1), key="-fix_data_file-"), 
         gui.Text(str(total_games_played) + " matches played in the last 30 days")]
    ]
   
    layout = layout_header + output_rows + bottom_layout

    main_window = gui.Window("Account List", layout, icon="logo.ico")

    while True:
        event, values = main_window.read()
        
        if event == gui.WIN_CLOSED:
            return False
        
        if event == "-add_account-":
            add_account()
            main_window.close()
            main()
            return
        
        if event == "-fix_data_file-":
            fix_data_file()
        
        if event == "-clear_accounts-":
            clear_accounts()
            main_window.close()
            main()
            return
            
        if event in delete_dict:
            delete_account(delete_dict[event])
            main_window.close()
            main()
            return
        
        if event in login_dict:
            login_account(login_dict[event])

if __name__ == "__main__":
    setup()
    main()