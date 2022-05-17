import json
import time
import subprocess
import threading
import PySimpleGUI as gui
import os
import scraper
import zlib
import random

from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from tabulate import tabulate
from pynput.keyboard import Key, Controller
from win32gui import GetWindowText, GetForegroundWindow

keyboard = Controller()

global_account_data = None
cached_account_data = {}
active_threads = {}

def obscure(data):
    return b64e(zlib.compress(data, 9))

def unobscure(obscured):
    return zlib.decompress(b64d(obscured))


def load_account_to_cache(account, thread_number):
    account_data = global_account_data[str(account)]
    
    if account_data["summoner_name"] != "":
        soup, summoner_data = scraper.load_summoner_page(account_data["region"], account_data["summoner_name"])

        try:
            unobscured_password = unobscure(str(account_data["password"]).encode()).decode()
        except:
            unobscured_password = str(account_data["password"])

        if thread_number != None:
            cached_account_data[str(thread_number)] = [[int(thread_number) + 1, account_data["summoner_name"], summoner_data["level"], account_data["region"], summoner_data["rank"], summoner_data["games_played"]], [account_data["login_name"], unobscured_password, account]]
            time.sleep(0.1)
            active_threads.pop(thread_number, None)
        else:
            cached_account_data[str(len(cached_account_data) + 1)] = [[int(len(cached_account_data)) + 1, account_data["summoner_name"], summoner_data["level"], account_data["region"], summoner_data["rank"], summoner_data["games_played"]], [account_data["login_name"], unobscured_password, account]]
    else:
        try:
            unobscured_password = unobscure(str(account_data["password"]).encode()).decode()
        except:
            unobscured_password = str(account_data["password"])

        if thread_number != None:
            cached_account_data[str(thread_number)] = [[int(thread_number) + 1, account_data["login_name"], "", account_data["region"], "", ""], [account_data["login_name"], unobscured_password, account]]
            time.sleep(0.1)
            active_threads.pop(thread_number, None)
        else:
            cached_account_data[str(len(cached_account_data) + 1)] = [[int(len(cached_account_data)) + 1, account_data["login_name"], "", account_data["region"], "", ""], [account_data["login_name"], unobscured_password, account]]
    
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


def delete_account(account_id, cached_id):
    if global_account_data[str(int(account_id))]:
        global_account_data.pop(str(int(account_id)))
    if cached_account_data[str(cached_id)]:
        cached_account_data.pop(str(cached_id))
    with open("account_data.json", "w") as file:
        file.write(json.dumps(global_account_data, indent = 4))

def login_account(account_id):
    account_data = cached_account_data[str(int(account_id) - 1)]
    if account_data:
        subprocess.call(["C:\Riot Games\League of Legends\LeagueClient.exe"])
        time.sleep(2.5)
        if GetWindowText(GetForegroundWindow()) == "Riot Client Main":
            keyboard.type(account_data[1][0])
            keyboard.press(Key.tab)
            keyboard.release(Key.tab)
            time.sleep(0.25)
            keyboard.type(account_data[1][1])
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)

def clear_accounts():
    global account_data
    global cached_account_data
    global_account_data = {}
    cached_account_data = {}
    with open("account_data.json", "w") as file:
        file.write(json.dumps(global_account_data))

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
    window = gui.Window("add account", layout)
    
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break
        
        if event == "-add_list-":
            layout = [
                [gui.Text("name:password")],
                [gui.Input("", key="-list-")],
                [gui.Button("submit", key="-submit-")]
            ]
            list_window = gui.Window("add by list", layout)
            while True:
                event2, values2 = list_window.read()
                if event2 == gui.WIN_CLOSED:
                    break
                    
                if event2 == "-submit-":
                    account_list = values2["-list-"].splitlines()
                    for account in account_list:
                        random_number = random.randint(1, 99999999999)
                        username, password = account.split(":")
                        global_account_data[str(random_number)] = {
                            "region": values["-region-"],
                            "summoner_name": "",
                            "login_name": username,
                            "password": obscure(str(password).encode()).decode()
                        }
                        load_account_to_cache(str(random_number),  None)
                    gui.popup("Accounts have been successfully added!")
                    list_window.close()
                    window.close()
                    
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
                    "password": obscure(str(values["-password-"]).encode()).decode()
                }
            else:
                global_account_data[str(random_number)] = {
                    "region": values["-region-"],
                    "summoner_name": "",
                    "login_name": values["-username-"],
                    "password": obscure(str(values["-password-"]).encode()).decode()
                }
                
            gui.popup("Account has successfully been added!")

            load_account_to_cache(str(random_number),  None)

            with open("account_data.json", "w") as file:
                file.write(json.dumps(global_account_data, indent = 4))
                
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
                global_account_data[account]["password"] = obscure(global_account_data[account]["password"].encode()).decode()
                
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
        ["Level", (6,1), ""],
        ["Region", (6,1), ""],
        ["Rank", (8,1), ""],
        ["Games 30D", (10,1), " games"]]
    
    layout_header =  [[gui.Text(header[0], size=header[1], background_color="Gray") for header in headings]]
    
    output_rows = []
    login_dict = {}
    delete_dict = {}
    total_games_played = 0
    
    for account in cached_account_data:
        summoner_data = cached_account_data[str(account)][0]
        account_data = cached_account_data[str(account)][1]
        output_row = []
        
        for data in summoner_data:
            output_row.append(gui.Text(str(data) + str(headings[len(output_row)][2]), size=headings[len(output_row)][1]))
        total_games_played += int(summoner_data[5])
        
        login_dict["-login " + str(account_data[2]) + "-"] = str(account_data[2])
        delete_dict["-delete " + str(account_data[2]) + "-"] = [str(account_data[2]), str(account)]
        
        output_row.append(gui.Button("Login", size=(10,1), key="-login " + str(account_data[2]) + "-"))
        output_row.append(gui.Button("Delete", size=(10,1), key="-delete " + str(account_data[2]) + "-"))
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
            delete_account(delete_dict[event][0], delete_dict[event][1])
            main_window.close()
            main()
            return
        
        if event in login_dict:
            login_account(login_dict[event])


        

if __name__ == "__main__":
    setup()
    main()