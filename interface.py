import PySimpleGUI as gui
import gc

def main(accounts = None):

    headings = [["ID", (2,1)],["Name", (14,1)], ["Level", (10,1)], ["Region", (10,1)],["Rank", (10,1)],["Games 30D", (10,1)], ["Hours Played", (10,1)]]
    headings[1:-1]

    layout_header =  [[gui.Text(header[0], size=header[1], background_color="Gray") for header in headings]]

    layout = [[gui.Column([[gui.Text("" ,size=header[1], background_color = "#6488ea", visible=False, key=f"-{header[0]}-{x + 1}-") for header in headings] for x in range(50)], size=(641, 320), scrollable=True, vertical_scroll_only=True, pad=1, key="-test-")]]

    layout = layout_header + layout

    window = gui.Window("Account Manager", layout, icon="logo.ico")
    
    while True:
        event, values = window.read(500)
        
        if event == gui.WIN_CLOSED or event == 'Exit':
            return False

        if accounts is not None:
            for account in accounts:
                if account.data is not None:
                    if window[f"-ID-{account.id}-"].get() == "": 
                        for header in headings:
                            window[f"-{header[0]}-{account.id}-"].update(visible=True)
                            
                        window[f"-ID-{account.id}-"].update(account.id)
                        window[f"-Name-{account.id}-"].update(account.summoner_username)
                        window[f"-Level-{account.id}-"].update(account.data["level"])
                        window[f"-Region-{account.id}-"].update(account.region)
                        window[f"-Rank-{account.id}-"].update(account.data["rank"])
                        window[f"-Games 30D-{account.id}-"].update(str(account.data["games_played"]) + " games")
                        window[f"-Hours Played-{account.id}-"].update(str(round(account.data["time_played_minutes"] / 60, 2)) + " hours")
                        
if __name__ == "__main__":
    main()