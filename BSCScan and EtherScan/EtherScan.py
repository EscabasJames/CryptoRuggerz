from parsel import Selector
import requests
import tabulate
import re

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
holderListResp = requests.get("https://etherscan.io/token/generic-tokenholders2?m=normal&a=0x4688a8b1f292fdab17e9a90c8bc379dc1dbd8713&s=100000000000000000000000000&sid=0x2859e4544c4bb03966803b044a93563bd2d0dd4d&p=1", headers=headers)
totalSupplyResp = requests.get("https://etherscan.io/token/0x4688a8b1f292fdab17e9a90c8bc379dc1dbd8713*#balances", headers=headers)

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

print(tabulate.tabulate(fullList, headers="firstrow", tablefmt="github"))