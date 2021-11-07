import tabulate
from colorama import Fore
from enum import Enum
import sys
import importlib

# Adding module folder to the system path
sys.path.insert(0, 'CryptoRuggerz_Modules')

# Set flags for full scans
BSCFLAG = "BSC"
ETHERFLAG = "ETHER"

namesOfModules = [[1, "BSCScan Scrape"], [2, "EtherScan Scrape"], [3, "Decentralised Exchange Listing Check"],
                  [4, "Github Activity Check"], [5, "Get Mean Age of Coin"],
                  [6, "Get Social Metrics of Coin"], [7, "Telegram PnD Group Check"], [8, "Twitter Activity Check"],
                  [9, "WhitePaper Analysis"]]

print(Fore.LIGHTGREEN_EX + "Welcome to CryptoRuggerz!" + Fore.RESET)
print(tabulate.tabulate(namesOfModules, headers=["Module ID", "Name of Module"], tablefmt="github"))

print(Fore.LIGHTGREEN_EX + "To get started enter " + Fore.RED + "BSC/ETHER" + Fore.LIGHTGREEN_EX+ " to select which smart chain to use")
moduleInput = input("Type BSC/ETHER or modules to be used: " + Fore.RESET)
print("")

totalScore = 0

if BSCFLAG.casefold() in moduleInput.casefold():
    import CryptoRuggerz_Modules.BSCscan
    totalScore += CryptoRuggerz_Modules.BSCscan.BSCSCORE

    import CryptoRuggerz_Modules.DEXOnly
    totalScore += CryptoRuggerz_Modules.DEXOnly.DEXSCORE

    import CryptoRuggerz_Modules.GitCommits
    totalScore += CryptoRuggerz_Modules.GitCommits.GITACTSCORE

    import CryptoRuggerz_Modules.MeanCoinAge
    totalScore += CryptoRuggerz_Modules.MeanCoinAge.MEANAGESCORE

    import CryptoRuggerz_Modules.SantimentsSocial
    totalScore += CryptoRuggerz_Modules.SantimentsSocial.SOCIALSCORE

    import CryptoRuggerz_Modules.TelegramScraper
    totalScore += CryptoRuggerz_Modules.TelegramScraper.TELESCORE

    import CryptoRuggerz_Modules.TwitterCoin
    totalScore += CryptoRuggerz_Modules.TwitterCoin.TWITTERSCORE

    import CryptoRuggerz_Modules.Whitepaper_Analysis
    totalScore += CryptoRuggerz_Modules.Whitepaper_Analysis.WHITEPAPERSCORE

    print(Fore.GREEN + "\nResult is ", totalScore, "out of 100")
    print("The lower the number the worse the coin is!" + Fore.RESET)

    yesNo = input("Would you like to perform a background check on the project[Y/N]?")

    if yesNo.casefold() == "y":
        import CryptoRuggerz_Modules.GitGet
    else:
        print("Use the information gathered wisely!")

elif ETHERFLAG.casefold() in moduleInput.casefold():
    import CryptoRuggerz_Modules.EtherScan
    totalScore += CryptoRuggerz_Modules.EtherScan.ETHERSCORE

    import CryptoRuggerz_Modules.DEXOnly
    totalScore += CryptoRuggerz_Modules.DEXOnly.DEXSCORE

    import CryptoRuggerz_Modules.GitCommits
    totalScore += CryptoRuggerz_Modules.GitCommits.GITACTSCORE

    import CryptoRuggerz_Modules.MeanCoinAge
    totalScore += CryptoRuggerz_Modules.MeanCoinAge.MEANAGESCORE

    import CryptoRuggerz_Modules.SantimentsSocial
    totalScore += CryptoRuggerz_Modules.SantimentsSocial.SOCIALSCORE

    import CryptoRuggerz_Modules.TelegramScraper
    totalScore += CryptoRuggerz_Modules.TelegramScraper.TELESCORE

    import CryptoRuggerz_Modules.TwitterCoin
    totalScore += CryptoRuggerz_Modules.TwitterCoin.TWITTERSCORE

    import CryptoRuggerz_Modules.Whitepaper_Analysis
    totalScore += CryptoRuggerz_Modules.Whitepaper_Analysis.WHITEPAPERSCORE

    print(Fore.GREEN + "\nResult is ", totalScore, "out of 100")
    print("The lower the number the worse the coin is!" + Fore.RESET)

    yesNo = input("Would you like to perform a background check on the project[Y/N]?")

    if yesNo.casefold() == "y":
        import CryptoRuggerz_Modules.GitGet
    else:
        print("Use the information gathered wisely!")