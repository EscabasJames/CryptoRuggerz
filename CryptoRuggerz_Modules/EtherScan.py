from parsel import Selector
import requests
import tabulate
import re
import colorama
from colorama import Fore

global ETHERSCORE

flag = True

print(Fore.LIGHTGREEN_EX + "\n============ STARTING ETHERSCAN SCRAPE ============\n" + Fore.RESET)

# Make request look like it comes from a legitimate browser
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

# Ask user for contract address
while(flag):
    contractAddress = input(Fore.LIGHTGREEN_EX + "Input Ethereum contract address: " + Fore.RESET)

    holderListResp = requests.get("https://etherscan.io/token/generic-tokenholders2?m=normal&a=" + contractAddress + "&s=100000000000000000000000000&sid=0x2859e4544c4bb03966803b044a93563bd2d0dd4d&p=1", headers=headers)
    totalSupplyResp = requests.get("https://etherscan.io/token/" + contractAddress + "#balances", headers=headers)

    sel = Selector(holderListResp.text)
    newSel = Selector(totalSupplyResp.text)
    fullList = [["Type", "Wallet Address", "Percentage Holding"]]

    # Manually read the total supply of coin because API doesn't give these values
    totalSupply = str(newSel.xpath('.//span[contains(@class, "hash-tag text-truncate")]/@title').get())
    totalSupply = totalSupply.replace(" ", "")
    totalSupply = totalSupply.replace(",", "")

    for row in sel.css('tr'):
        # Get total number of tokens wallet holds in column 3
        perc = row.xpath('td[3]/text()').get()

        # Skip rows with no values
        if not perc:
            continue

        # Calculate holding percentage
        perc = float(perc.replace(",", "")) / float(totalSupply) * 100
        perc = round(perc, 4)
        perc = str(perc) + "%"

        # Address is on 2nd column under <a> node
        # we can also use `re()` method to only take the token part of the url
        addr = row.xpath('td[2]//a/text()').re('([^#?]+)')[0]
        isContract = row.xpath('td[2]//i')

        if len(isContract) != 0:
            fullList.append(["Contract", addr, perc])
        elif re.search("Burn", addr, re.IGNORECASE):
            fullList.append(["Burn Address", addr, perc])
        else:
            fullList.append(["Wallet", addr, perc])

    if len(fullList) == 1:
        print(Fore.RED + "\nCannot find contract! Are you sure you entered a valid contract?\n"+ Fore.RESET)
    else:
        print("")
        print(tabulate.tabulate(fullList, headers="firstrow", tablefmt="github"))

        for i in fullList[1:]:
            if "Wallet" in i[0]:
                highestHolder = i
                break

        highestHolderVal = float(highestHolder[2].replace("%",""))
        if highestHolderVal > 50:
            print(Fore.RED + "\nWallet holding the highest number of coins is more than 50%!")
            print("This is very dangerous.")
            print("Wallet holds", highestHolderVal, "% of total coin")
            ETHERSCORE = 0
        elif highestHolderVal > 20:
            print(Fore.YELLOW + "\nWallet holding the highest number of coins is more than 20%.")
            print("Take caution.")
            print("Highest Wallet holds", highestHolderVal, "% of total coin")
            ETHERSCORE = 15
        else:
            print(Fore.GREEN + "\nWallet holding the highest number of coins is less than 20%.")
            print("Highest Wallet holds", highestHolderVal, "% of total coin")
            ETHERSCORE = 35

        print(Fore.LIGHTRED_EX + "\n============ END OF ETHERSCAN SCRAPE ============\n" + Fore.RESET)
        flag = False