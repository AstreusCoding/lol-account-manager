import user_interface
import accounts
import threading
import os
import json
import gc

def main():
    accounts.load_accounts()
    threading.Thread(target=user_interface.main_display).start()

def convert_old_data_structure_to_new():
    if not os.path.exists("./account_data.json"):
        return
    
    with open("account_data.json", "r") as file:
        data = json.load(file)
        for key, account in data.items():
            new_account = accounts.Account(summoner_username=account["summoner_name"], region=accounts.ServerRegion[str.upper(account["region"])], username=account["login_name"], password=account["password"])

    os.remove("./account_data.json")

if __name__ == "__main__":
    convert_old_data_structure_to_new()
    main()