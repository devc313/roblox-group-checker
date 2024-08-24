# Roblox Group Checker
This repository contains a script that allows you to check and retrieve various details about your Roblox groups using your .ROBLOSECURITY cookie. It provides information about group funds, pending funds, number of games, total visits, clothing items, and more. This tool is particularly useful for Roblox group owners who want to manage and monitor their groups efficiently.

Features
Retrieve User ID: Fetch your Roblox User ID using your .ROBLOSECURITY cookie.\n
Group Details: Get information on all groups you own, including:\n
Group Name\n
Number of Members
Group Funds and Pending Funds
Total Number of Games and Game Visits
Number of Clothing Items
Logging: Logs all the retrieved data into a group_data.txt file for easy reference.
Cross-Platform: Works on both Windows and Unix-based systems.
Installation
To install the required dependencies, run:

pip install -r requirements.txt
The requirements.txt file includes the following Python packages:

aiohttp
asyncio
datetime
colorama
Usage
Clone this repository to your local machine.

Install the required dependencies using the command above.

Run the script using:

python roblox.py
The script will prompt you to enter your .ROBLOSECURITY cookie. Once provided, it will begin retrieving data about your groups and store the results in the group_data.txt file.

# License
This project is licensed under the MIT License.
