import requests
import json
import tabulate
import colorama
from colorama import Fore

global MEANAGESCORE
skipFlag = "SKIP"
flag = True

print(Fore.LIGHTGREEN_EX + "\n============ STARTING MEAN AGE CHECK ============\n" + Fore.RESET)

while(flag):
    slug = input(Fore.RESET + "Please enter coin slug name OR type SKIP to skip: ")

    if slug.casefold() == skipFlag.casefold():
        flag = False
    else:
        # Use Sanbase grahiql to query since we are not going to pay for this API
        meanAgeReq = "http://api.santiment.net/graphiql?query={getMetric(metric:\"mean_age\"){timeseriesData(selector:{slug:\""+slug+"\"}\nfrom:\"utc_now-30d\"\nto:\"utc_now\"\ninterval:\"4w\"){\ndatetime\nvalue}}}"

        meanAgeResp = requests.get(meanAgeReq)
        meanAgeJson = json.loads(json.dumps(meanAgeResp.json()))
        meanAgeDict = meanAgeJson["data"]["getMetric"]["timeseriesData"]

        # Check if data does exist
        if meanAgeDict is None:
            print(Fore.RED + "\nData for this coin does not exist yet!")
            print(Fore.RED + "You can try entering the slug again or type SKIP to skip\n")
            continue
        elif len(meanAgeDict) == 0:
            print(Fore.RED + "\nData for this coin does not exist yet!")
            print(Fore.RED + "You can try entering the slug again or type SKIP to skip\n")
            continue
        else:
            print("====== Mean age of coins in days ========\n")
            print(tabulate.tabulate(meanAgeDict, headers={"Date": "Date", "Value": "Value"}, tablefmt="github"))


        print("")
        # For approximate month value, divide the days value by 30.417
        months = meanAgeDict[0]["value"] / 30.417

        if months < 3:
            # Less than 3 months, relatively new coin
            print(Fore.RED + "Coin is relatively new!")
            MEANAGESCORE = 0
        elif months < 6:
            # More than 3 months but less than 6 months, be cautious
            print(Fore.YELLOW + "Coin is older than 3 months but be cautious!")
            MEANAGESCORE = 2.5
        else:
            # More than 6 months, relatively trustable
            print(Fore.GREEN + "Coin is older than 6 months!")
            MEANAGESCORE = 5

        flag = False

if slug.casefold() == skipFlag.casefold():
    MEANAGESCORE = 0

print(Fore.RED + "\n============ END OF COIN MEAN AGE CHECK ============\n" + Fore.RESET)
