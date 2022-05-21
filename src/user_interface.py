import time
import PySimpleGUI as gui
import gc
import accounts
import random
import scraper

main_window = None

def clear_accounts():
    account_list = []

    for obj in gc.get_objects():
        if isinstance(obj, accounts.Account):
            if obj.deleted is False:
                account_list.append(obj)

    for account in account_list:
        account.remove()

def add_account_display():
    layout = [
        [gui.Text("Region")],
        [gui.Combo([region.name for region in accounts.ServerRegion], size=(16,1), key="-region-")],
        [gui.Text("Summoner Name")],
        [gui.Input("", key="-summoner-", size=(16,1))],
        [gui.Text("Username")],
        [gui.Input("", key="-username-", size=(16,1))],
        [gui.Text("Password")],
        [gui.Input("", password_char="*", key="-password-", size=(16,1))],
        [gui.Button("submit", key="-submit-", size=(16,1))],
    ]
    
    window = gui.Window("add account", layout, modal=True)
    
    while True:
        event, values = window.read()
        if event == gui.WIN_CLOSED:
            break
        
        if event == "-add_list-":
            window.close()
            #add_account_list()
            return
                    
        if event == "-submit-":
            random_number = random.randint(1, 99999999999)
            
            if values["-summoner-"] != "":
                account_page = scraper.load_summoner_page(values["-region-"], values["-summoner-"])
                if not account_page:
                    gui.popup("This summoner name is not connected to any account!")
                    return

            new_account = accounts.Account(region=accounts.ServerRegion[values["-region-"]], summoner_username=values["-summoner-"], username=values["-username-"], password=values["-password-"])
            gui.popup("Account has successfully been added!")
            
            window.close()
            update_main_display()

def update_main_display(window = None):
    global main_window
    if window is None:
        if main_window is not None:
            main_window.hide()
        main_display()
        return
        
    account_list = []
    total_games_played = 0
        
    for obj in gc.get_objects():
        if isinstance(obj, accounts.Account):
            if obj.deleted is False:
                account_list.append(obj)

    for count, account in enumerate(account_list):
        if account.summoner_username == "":
            return
        level = account.statistics.get("level")
        rank = account.statistics.get("rank") 
        games_played = account.statistics.get("games_played")
        
        if not f"-{account.id}_summoner_name-" in window.AllKeysDict:
            window.hide()
            main_display()
            return
        
        window[f"-{account.id}_summoner_name-"].update(account.summoner_username)
        window[f"-{account.id}_level-"].update(level)
        window[f"-{account.id}_region-"].update(account.region.name)
        window[f"-{account.id}_rank-"].update(rank)
        window[f"-{account.id}_games_played-"].update(f"{games_played} games")
            
        if str(games_played).isnumeric():
            total_games_played += games_played
    
    window["-games-played-"].update(f"{total_games_played} matches played in the last 30 days")
                
def main_display():
    global main_window
    account_list = []
    
    for obj in gc.get_objects():
        if isinstance(obj, accounts.Account):
            if obj.deleted is False:
                account_list.append(obj)
    
    headings = [["ID", (2,1)],["Name", (14,1)], ["Level", (10,1)], ["Region", (10,1)],["Rank", (10,1)],["Games 30D", (10,1)]]
    headings[1:-1]

    layout_header =  [[gui.Text(header[0], size=header[1], background_color="Gray") for header in headings]]
    
    output_rows = []
    login_dict = {}
    delete_dict = {}
    total_games_played = 0

    for count, account in enumerate(account_list):
        
        output_row = []
        
        level = account.statistics.get("level")
        rank = account.statistics.get("rank") 
        games_played = account.statistics.get("games_played")

        if account.summoner_username == "":
            output_row.append(gui.Text(f"{count + 1}", size=(2, 1), background_color = "#6488ea", key=f"-{account.id}-0-"))
            output_row.append(gui.Text(account.username, background_color = "#6488ea", size=(14, 1), key=f"-{account.id}_summoner_name-"))
            output_row.append(gui.Text("Unknown", background_color = "#6488ea", size=(10, 1), key=f"-{account.id}_level-"))
            output_row.append(gui.Text(account.region.name, background_color = "#6488ea", size=(10, 1), key=f"-{account.id}_region-"))
            output_row.append(gui.Text("Unknown", background_color = "#6488ea", size=(10, 1), key=f"-{account.id}_rank-"))
            output_row.append(gui.Text("Unknown", background_color = "#6488ea", size=(10, 1), key=f"-{account.id}_games_played-"))
        else:
            output_row.append(gui.Text(f"{count + 1}", size=(2, 1), background_color = "Navy Blue", key=f"-{account.id}-0-"))
            output_row.append(gui.Text(f"{account.summoner_username}", size=(14, 1), background_color = "Navy Blue", key=f"-{account.id}_summoner_name-"))
            output_row.append(gui.Text(f"{level}", size=(10, 1), background_color = "Navy Blue", key=f"-{account.id}_level-"))
            output_row.append(gui.Text(f"{account.region.name}", size=(10, 1), background_color = "Navy Blue", key=f"-{account.id}_region-"))
            output_row.append(gui.Text(f"{rank}", size=(10, 1), background_color = "Navy Blue", key=f"-{account.id}_rank-"))
            output_row.append(gui.Text(f"{games_played} games", size=(10, 1), background_color = "Navy Blue", key=f"-{account.id}_games_played-"))
              
        if str(games_played).isnumeric():
            total_games_played += games_played
        
        login_dict[f"-login_{account.id}-"] = account
        delete_dict[f"-delete_{account.id}-"] = account
        
        output_row.append(gui.Button("Login", size=(10,1), key=f"-login_{account.id}-"))
        output_row.append(gui.Button("Delete", size=(10,1), key=f"-delete_{account.id}-"))
        output_rows.append(output_row)

    layout = [
            [gui.Button("Add Account", size=(10,1), key="-add_account-"),
            gui.Button("Clear Accounts", size=(12,1), key="-clear_accounts-"),
            gui.Text(str(total_games_played) + " matches played in the last 30 days", key="-games-played-")]
        ]
   
    layout = layout_header + output_rows + layout

    window = gui.Window("Account List", layout, icon="logo.ico")
    main_window = window
    
    while True:
        event, values = window.read(1000)
        
        if event == gui.WIN_CLOSED:
            return False
        
        if event == "-clear_accounts-":
            clear_accounts()
            window.hide()
            main_display()
            return
        
        if event == "-add_account-":
            add_account_display()
        
        if event in delete_dict:
            delete_dict[event].remove()
            window.hide()
            main_display()
            return
        
        if event in login_dict:
            login_dict[event].login()
            
        update_main_display(window)