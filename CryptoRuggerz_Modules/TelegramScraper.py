from telethon.sync import TelegramClient
from telethon import functions, types
from datetime import datetime, timedelta
import json
import tabulate
import colorama
from colorama import Fore

global TELESCORE

print(Fore.LIGHTGREEN_EX + "\n============ STARTING TELE GROUP CHECK ============\n" + Fore.RESET)

# Use our own API key and App ID
api_id = 17232835
api_hash = '7143803aea59e783dabe6e6950b24827'

coinToSearch = input("Enter a coin to search: ")

listOfGroups = ["https://t.me/MegaPumpFFA", "https://t.me/wallstreetevents",
                "https://t.me/Cryptocoinpumpsignals", "https://t.me/binancepumpcryptopump",
                "https://t.me/binancepumproys", "https://t.me/TodayWePush", "https://t.me/binacepumpswhales",
                "https://t.me/mega_pump_group", "https://t.me/wall_street_bets_channel", "https://t.me/wsb_crpyto"]

mentionList = [["Pump and Dump Telegram Channel", "Times Mentioned in past 3 months"]]

with TelegramClient('anon', api_id, api_hash) as client:

    for i in range(10):
        reqRes = client(functions.messages.SearchRequest(
            peer=listOfGroups[i],
            q=coinToSearch,
            filter=types.InputMessagesFilterEmpty(),
            min_date=datetime.today() - timedelta(days=90),
            max_date=datetime.today(),
            offset_id=0,
            add_offset=0,
            limit=100,
            max_id=0,
            min_id=0,
            hash=0,
            from_id=None
        ))

        listToAppend = []
        listToAppend.append(listOfGroups[i].lstrip("https://t.me/"))
        listToAppend.append(reqRes.count)
        mentionList.append(listToAppend)

# for i in gp1Results.messages:
#     gp1List.append(i.message)

print(tabulate.tabulate(mentionList, headers="firstrow", tablefmt="github"))
totalMentions = 0

for i in mentionList[1:]:
    totalMentions += int(i[1])

if totalMentions != 0:
    print(Fore.RED + "\nQuery has been mentioned a total of", totalMentions, "time(s)!")
    TELESCORE = 0
else:
    print(Fore.GREEN + "\nQuery has been mentioned a total of", totalMentions, "time(s)!")
    TELESCORE = 15

print(Fore.RED + "\n============ END OF GIT ACTIVITY CHECK ============\n" + Fore.RESET)
