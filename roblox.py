import sys
import aiohttp
import json
import asyncio
import socket
import os
from datetime import datetime
from colorama import Fore, Style

if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Console:
    @staticmethod
    def clear() -> int:
        if "nt" in os.name:
            return os.system("cls")
        return os.system("clear")

    @staticmethod
    def timer() -> str:
        return Style.BRIGHT + Fore.BLACK + f"[{datetime.now().strftime('%I:%M:%S')}] "

    @staticmethod
    def log(query: str) -> None:
        print(
            Console.timer() + f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}INFO {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{query}",
            end="\n")

    @staticmethod
    def success(query: str) -> None:
        print(
            Console.timer() + f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}SUCCESS {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{query}",
            end="\n")

    @staticmethod
    def danger(query: str) -> None:
        print(
            Console.timer() + f"{Style.BRIGHT}{Fore.LIGHTRED_EX}ROBUXFOUND {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{query}",
            end="\n")

    @staticmethod
    def uid(query: str) -> str:
        return input(
            Console.timer() + f"{Style.BRIGHT}{Fore.LIGHTCYAN_EX}CHECKER {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{query}")

    @staticmethod
    def get_cookie(query: str) -> str:
        return input(
            Console.timer() + f"{Style.BRIGHT}{Fore.YELLOW}COOKIE {Fore.WHITE}{Fore.RESET}{Style.BRIGHT}{Fore.BLACK} >  {Fore.RESET}{Fore.WHITE}{query}")

class File:
    def __init__(self) -> None:
        self.path = "group_data.txt"

    def store(self, data) -> None:
        with open(self.path, "a+", encoding="utf-8") as opener:
            opener.write(data + "\n")

    def purge(self) -> None:
        with open(self.path, "w+", encoding="utf-8") as purge:
            return None

class Checker:
    def __init__(self, roblox_cookie) -> None:
        self.roblox_cookie = {
            ".ROBLOSECURITY": roblox_cookie
        }
        self.console = Console()

    async def get_user_id(self):
        async with aiohttp.ClientSession(cookies=self.roblox_cookie,
                                         connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)) as session:
            try:
                async with session.get(f'https://www.roblox.com/mobileapi/userinfo') as response:
                    data = await response.json()
                    user_id = data["UserID"]
                    return user_id
            except Exception:
                return None

    async def get_group_ids(self, user_id):
        group_ids = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)) as session:
            try:
                async with session.get(f"https://groups.roblox.com/v2/users/{user_id}/groups/roles") as response:
                    data = await response.json()
                    groups_data = data.get('data', [])
                    for group_data in groups_data:
                        if group_data['role']['rank'] == 255:
                            group_ids.append(group_data['group']['id'])
            except Exception:
                pass
        return group_ids

    async def get_group_info(self, group_id):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)) as session:
            try:
                async with session.get(f"https://groups.roblox.com/v1/groups/{group_id}") as response:
                    data = await response.json()
                    group_name = data.get("name", "")
                    group_members = data.get("memberCount", 0)
                    return group_name, group_members
            except Exception:
                return "", 0

    async def get_clothing_count(self, group_id):
        total_clothing_count = 0
        url = f"https://catalog.roblox.com/v1/search/items/details"
        params = {
            "Category": "3",
            "CreatorTargetId": str(group_id),
            "CreatorType": "2",
            "SortType": "Relevance",
            "SortAggregation": "Relevance",
            "limit": "30",
        }

        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)
        ) as session:
            while True:
                try:
                    async with session.get(url, params=params) as req:
                        response_data = await req.json()
                        items, cursor = response_data["data"], response_data["nextPageCursor"]
                        total_clothing_count += len(items)

                        if cursor:
                            params["cursor"] = cursor
                        else:
                            break
                except Exception:
                    return 0

            return total_clothing_count

    async def get_group_funds(self, group_id):
        async with aiohttp.ClientSession(cookies=self.roblox_cookie,
                                         connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)) as session:
            try:
                async with session.get(f'https://economy.roblox.com/v1/groups/{group_id}/currency') as response:
                    data = await response.json()
                    group_funds = data.get("robux", 0)
            except Exception:
                group_funds = 0
        return group_funds

    async def get_pending_funds(self, group_id):
        async with aiohttp.ClientSession(cookies=self.roblox_cookie,
                                         connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)) as session:
            try:
                async with session.get(
                        f"https://economy.roblox.com/v1/groups/{group_id}/revenue/summary/{datetime.day}") as response:
                    data = await response.json()
                    pendingBobux = data.get("pendingRobux", 0)

            except Exception:
                pendingBobux = 0

        return pendingBobux

    async def get_total_visits(self, group_id):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)) as session:
            try:
                async with session.get(
                        f'https://games.roblox.com/v2/groups/{group_id}/games?accessFilter=All&sortOrder=Asc&limit=100') as response:
                    data = await response.json()
                    games_data = data.get("data", [])
            except Exception:
                games_data = []

        if not games_data:
            return 0

        total_visits = 0
        for game in games_data:
            visits = game.get("placeVisits", 0)
            total_visits += visits
        return total_visits

    async def get_total_games(self, group_id):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(family=socket.AF_INET, ssl=False)) as session:
            try:
                async with session.get(
                        f'https://games.roblox.com/v2/groups/{group_id}/games?accessFilter=All&sortOrder=Asc&limit=100') as response:
                    data = await response.json()
                    games_data = data.get("data", [])
            except Exception:
                games_data = []

        return len(games_data)

    async def check_groups(self):
        user_id = await self.get_user_id()
        if not user_id:
            self.console.log("Failed to retrieve user ID.")
            return

        group_ids = await self.get_group_ids(user_id)
        if not group_ids:
            self.console.log("No groups found.")
            return

        for group_id in group_ids:
            group_info = await self.get_group_info(group_id)
            group_funds = await self.get_group_funds(group_id)
            group_pending_funds = await self.get_pending_funds(group_id)
            total_visits = await self.get_total_visits(group_id)
            total_games = await self.get_total_games(group_id)
            clothing_count = await self.get_clothing_count(group_id)

            group_name, group_members = group_info
            File().store(
                f"Group ID: {group_id} | Group Name: {group_name} | Group Members: {group_members} | Group Funds: {group_funds} / Pending Funds: {group_pending_funds} | Group Clothings: {clothing_count} | Group Games: {total_games} | Group GameVisits: {total_visits}")
            
            if group_funds > 0:
                self.console.danger(f"Stored data of '{group_id}'")
            else:
                self.console.success(f"Stored data of '{group_id}'")

if __name__ == '__main__':
    console = Console()
    console.clear()
    File().purge()
    roblox_cookie = console.get_cookie("Please enter your .ROBLOSECURITY cookie: ")
    checker = Checker(roblox_cookie)
    console.log("Starting Group Checker...")
    asyncio.run(checker.check_groups())
