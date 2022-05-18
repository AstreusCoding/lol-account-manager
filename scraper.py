import requests
from bs4 import BeautifulSoup

league_of_graphs_url = "https://www.leagueofgraphs.com/summoner/"
headers = {'User-Agent': 'My User Agent 1.0'}

def load_summoner_page(region, summoner_name):
    
    response = requests.get(league_of_graphs_url + region + "/" + summoner_name + "/last-30-days", headers=headers)
    if response.status_code != 200:
        print("load_summoner_page failed with error code: " + str(response.status_code))
        return
        
    soup = BeautifulSoup(response.content, 'html.parser')

    is_valid_summoner = soup.find(class_="best-league")

    if not is_valid_summoner:
        print("There is no summoner on " + region + " named " + summoner_name)
        return
    
    summoner_data = {
        "level": int(str(str.split(soup.find(class_="bannerSubtitle").text.strip(), "-")[0])[5:]),
        "rank": str(soup.find(class_="leagueTier").text.strip()),
        "games_played": int(soup.find(class_="summonerProfileQueuesTabs tabsContainer").find(class_="tabs-content").find("div", { "data-tab-id" : "championsData-all-queues" }).find(class_="pie-chart small").text.strip())
    }
    
    return soup, summoner_data