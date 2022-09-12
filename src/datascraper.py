"""
    This handles any web scraping that is needed. Optionally this can use an API key.
    Written by: github.com/CasperDoesCoding
    Date: September / 9 / 2022
"""

import aiohttp
from unsync import unsync
from bs4 import BeautifulSoup as bs
from logzero import logger

LOG_URL = "https://www.leagueofgraphs.com/summoner/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"  # noqa: E501
}


class DataScraper:
    def __init__(self, api_key: str = None) -> None:
        """
        Initializes the DataScraper class.

        Args:
            NOT IMPLEMENTED
            api_key (str, optional): If you have an riot API key
            you can use that instead of scraping league of graphs website, which
            is a lot faster. Defaults to None.
        """
        self.api_key = api_key

    @unsync
    async def get_page(self, url: str) -> str:
        """
        Gets the page from the specified url.

        Args:
            url (str): The url to get the page from.

        Returns:
            requests.models.Response: The response from the url.
        """

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=HEADERS) as response:
                    response.raise_for_status()
                    return await response.content.read()
        except Exception as e:
            logger.error(f"Failed to get page. {e}")
            return None

    @unsync
    def scrape_account_data(self, username, region) -> dict:
        """
        Scrapes the account data from league of graphs.

        Args:
            username (str): The username of the account.
            region (str): The region of the account.

        Returns:
            dict: The account data.
        """
        url = f"{LOG_URL}{str.lower(region)}/{username}/last-30-days"

        page = self.get_page(url).result()

        if page is None:
            return None

        soup = bs(page, "html.parser")

        account_exists = soup.find(class_="best-league")

        if not account_exists:
            logger.error(
                f"There is no summoner on {str.lower(region)} named {username}"
            )
            return

        summoner_data = {
            "level": int(
                str(str.split(soup.find(class_="bannerSubtitle").text.strip(), "-")[0])[
                    5:
                ]
            ),
            "rank": str(soup.find(class_="leagueTier").text.strip()),
            "games_played": int(
                soup.find(class_="summonerProfileQueuesTabs tabsContainer")
                .find(class_="tabs-content")
                .find("div", {"data-tab-id": "championsData-all-queues"})
                .find(class_="pie-chart small")
                .text.strip()
            ),
        }

        return summoner_data

    def scrape_several_accounts(self, accounts: list) -> list:
        """
        Scrapes several accounts.

        Args:
            accounts (list): A list of accounts.

        Returns:
            list: A list of account data.
        """
        tasks = [
            self.scrape_account_data(account.display_name, account.region)
            for account in accounts
        ]

        results = [task.result() for task in tasks]

        for i, account in enumerate(accounts):
            account.data = results[i]

        return True
