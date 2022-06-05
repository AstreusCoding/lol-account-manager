from random import randint
import PySimpleGUI as gui
import webscraper
import accounts
import database

HEADINGS = [["ID", (2,1)],["Name", (14,1)], ["Level", (10,1)], ["Region", (10,1)],["Rank", (10,1)],["Games 30D", (10,1)], ["Hours Played", (10,1)]]
HEADINGS[1:-1]

REGIONS = ["BR", "EUNE", "EUW", "JP", "KR", "LAN", "LAS", "NA", "OCE", "RU", "TR"]

loaded_ids = {}

login_dict = {}
delete_dict = {}
current_tab = "account_list"
total_games = 0

def create_account_list_layout():
    
    layout_header =  [[gui.Text(header[0], size=header[1], background_color="Gray") for header in HEADINGS]]

    placeholders = [[gui.Text("" ,size=header[1], background_color = "#6488ea", visible=False, key=f"-{header[0]}-{x + 1}-") for header in HEADINGS] for x in range(50)]

    for count, ph in enumerate(placeholders):
        ph.append(gui.Button("Login", size=(10,1), key=f"-login-{count + 1}-", visible=False))
        ph.append(gui.Button("Delete", size=(10,1), key=f"-delete-{count + 1}-", visible=False))

    layout = [[gui.Column(placeholders, size=(821, 320), scrollable=True, vertical_scroll_only=True, pad=1, key="-test-")]]

    buttons = [[gui.Button("Add Account", size=(10,1), key="-add-account-"),
            #gui.Button("Clear Accounts", size=(12,1), key="-clear-accounts-"),
            gui.Text("??? matches played in the last 30 days", key="-games-played-"),
            ]]

    layout = layout_header + layout + buttons

    return layout

def create_add_account_layout():
    layout = [
        [gui.Text("Region")],
        [gui.Combo([region for region in REGIONS], size=(16,1), key="-region-")],
        [gui.Text("Summoner Name")],
        [gui.Input("", key="-summoner-", size=(16,1))],
        [gui.Text("Username")],
        [gui.Input("", key="-username-", size=(16,1))],
        [gui.Text("Password")],
        [gui.Input("", password_char="*", key="-password-", size=(16,1))],
        [gui.Button("submit", key="-submit-", size=(10,1))],
        [gui.Button("cancel", key="-cancel-", size=(10,1))],
    ]
    
    return layout

def clear_account_list(window):
    global total_games
    global login_dict
    global delete_dict
    global loaded_ids
    
    total_games = 0
    login_dict = {}
    delete_dict = {}
    loaded_ids = {}
    
    for counter in range(50):
        for header in HEADINGS:
            window[f"-{header[0]}-{counter + 1}-"].update("")
            window[f"-{header[0]}-{counter + 1}-"].update(visible=False)
        
        window[f"-login-{counter + 1}-"].update(visible=False)
        window[f"-delete-{counter + 1}-"].update(visible=False)
        
        window["-games-played-"].update("??? matches played in the last 30 days")     

def update_account_list(window, accounts):
    global total_games
    global login_dict
    global delete_dict
    if accounts is not None:
        for acc_index, account in enumerate(accounts):
            if not account.id in loaded_ids:
                for counter in range(50):
                    if window[f"-ID-{counter + 1}-"].get() == "": 
                        for header in HEADINGS:
                            window[f"-{header[0]}-{counter + 1}-"].update(visible=True)
                        
                        window[f"-login-{counter + 1}-"].update(visible=True)
                        window[f"-delete-{counter + 1}-"].update(visible=True)
                        window[f"-ID-{counter + 1}-"].update(counter + 1)
                        window[f"-Name-{counter + 1}-"].update(account.summoner_username)
                        window[f"-Region-{counter + 1}-"].update(account.region)
                        
                        if account.data is not None:
                            window[f"-Level-{counter + 1}-"].update(account.data["level"])
                            window[f"-Rank-{counter + 1}-"].update(account.data["rank"])
                            window[f"-Games 30D-{counter + 1}-"].update(str(account.data["games_played"]) + " games")
                            window[f"-Hours Played-{counter + 1}-"].update(str(round(account.data["time_played_minutes"] / 60, 2)) + " hours")
                            total_games += int(account.data["games_played"])
                        
                        window["-games-played-"].update(str(total_games) + " matches played in the last 30 days")
                        
                        login_dict[f"-login-{counter + 1}-"] = (account, counter + 1, acc_index)
                        delete_dict[f"-delete-{counter + 1}-"] = (account, counter + 1, acc_index)
                        loaded_ids[account.id] = counter + 1
                        break
            else:
                if account.data is not None:
                    window[f"-Level-{loaded_ids[account.id]}-"].update(account.data["level"])
                    window[f"-Rank-{loaded_ids[account.id]}-"].update(account.data["rank"])
                    window[f"-Games 30D-{loaded_ids[account.id]}-"].update(str(account.data["games_played"]) + " games")
                    window[f"-Hours Played-{loaded_ids[account.id]}-"].update(str(round(account.data["time_played_minutes"] / 60, 2)) + " hours")

def account_list_logic(window, event, values, accounts):
    global current_tab
    global total_games
    global login_dict
    global delete_dict
    
    update_account_list(window, accounts)
           
    if event in delete_dict:
        delete_dict[event][0].delete()
        del accounts[delete_dict[event][2]]
        clear_account_list(window)
        update_account_list(window, accounts)
    elif event in login_dict:
        login_dict[event][0].login()  
    elif event == "-add-account-":
        window["-account-list-"].update(visible=False)
        window["-account-list-"].hide_row()
        
        window["-add-account-menu-"].update(visible=True)
        window["-add-account-menu-"].unhide_row()
        current_tab = "add_account"
        
def add_account_logic(window, event, values):
    global current_tab
    if event == "-submit-":
        if values["-summoner-"] != "":
            account_page = webscraper.fetch_account(values["-summoner-"], values["-region-"])
            if not account_page:
                gui.popup("This summoner name is not connected to any account!")
                return

        database.create_connection("data")
        account = accounts.Account(id=randint(1, 999999999), summoner_username=values["-summoner-"], region=values["-region-"], username=values["-username-"], password=values["-password-"])
        account.save()
        
        window["-add-account-menu-"].update(visible=False)
        window["-add-account-menu-"].hide_row()
        
        window["-account-list-"].update(visible=True)
        window["-account-list-"].unhide_row()
        
        current_tab = "account_list"
    elif event == "-cancel-":
        window["-add-account-menu-"].update(visible=False)
        window["-add-account-menu-"].hide_row()
        
        window["-account-list-"].update(visible=True)
        window["-account-list-"].unhide_row()
        
        current_tab = "account_list"

def main(accounts = None):
    global current_tab
    global login_dict
    global delete_dict
    
    layout = [[gui.Column(create_account_list_layout(), key="-account-list-")], [gui.Column(create_add_account_layout(), key="-add-account-menu-", visible=False)]]

    window = gui.Window("Account Manager", layout, icon="logo.ico")

    while True:
        event, values = window.read(500)

        if event == gui.WIN_CLOSED or event == 'Exit':
            return False
        window.refresh()
        if current_tab == "account_list":
            account_list_logic(window, event, values, accounts)
        elif current_tab == "add_account":
            add_account_logic(window, event, values)
            
if __name__ == "__main__":
    main()