import requests
from bs4 import BeautifulSoup
from datetime import datetime

LOG_URL = "https://www.leagueofgraphs.com/summoner/"
WOL_URL = "https://wol.gg/stats/"

HEADERS = {'User-Agent': 'My User Agent 1.0'}

def load_page(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print("load_page failed with error code: " + str(response.status_code))
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    return soup

def fetch_time_played(summoner_name, region):
    url = f"{WOL_URL}{str.lower(region)}/{summoner_name}/"

    soup = load_page(url)

    time_played_minutes = soup.find(id="time-minutes")
    time_played_minutes = "".join(filter(str.isdigit, time_played_minutes.text.strip()))

    return time_played_minutes

# check if summoner exists with the specified username on the specified region
def fetch_account(username, region):
    url = f"{LOG_URL}{str.lower(region)}/{username}/last-30-days"

    soup = load_page(url)

    account_exists = soup.find(class_="best-league")

    if not account_exists:
        print("There is no summoner on " + str.lower(region) + " named " + username)
        return

    return soup

def fetch_account_data(username, region, soup = None, account = None):
    if soup is None:
        soup = fetch_account(username, region)
        
    summoner_data = {
        "level": int(str(str.split(soup.find(class_="bannerSubtitle").text.strip(), "-")[0])[5:]),
        "rank": str(soup.find(class_="leagueTier").text.strip()),
        "games_played": int(soup.find(class_="summonerProfileQueuesTabs tabsContainer").find(class_="tabs-content").find("div", { "data-tab-id" : "championsData-all-queues" }).find(class_="pie-chart small").text.strip()),
        "time_played_minutes": int(fetch_time_played(username, region))
    }
    
    if account is not None:
        account.data = summoner_data
    
    return summoner_data