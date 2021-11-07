import requests
import json
import tabulate
import colorama
from colorama import Fore

slug = input("Please enter coin slug name: ")

# Use Sanbase grahiql to query since we are not going to pay for this API
meanAgeReq = "http://api.santiment.net/graphiql?query={getMetric(metric:\"mean_age\"){timeseriesData(selector:{slug:\""+slug+"\"}\nfrom:\"utc_now-30d\"\nto:\"utc_now\"\ninterval:\"4w\"){\ndatetime\nvalue}}}"

meanAgeResp = requests.get(meanAgeReq)
meanAgeJson = json.loads(json.dumps(meanAgeResp.json()))
meanAgeDict = meanAgeJson["data"]["getMetric"]["timeseriesData"]

# Check if data does exist
if meanAgeDict is None:
    print(Fore.RED + "\nEither coin doesn't exist or metrics for this coin does not exist!")

elif len(meanAgeDict) == 0:
    print(Fore.RED + "\nEither coin doesn't exist or metrics for this coin does not exist!")

else:
    print("====== Mean age of coins in days ========\n")
    print(tabulate.tabulate(meanAgeDict, headers={"Date": "Date", "Value": "Value"}, tablefmt="github"))


print("")
# For approximate month value, divide the days value by 30.417
months = meanAgeDict[0]["value"] / 30.417

if months < 3:
    # Less than 3 months, relatively new coin
    print(Fore.RED + "Coin is relatively new!")
elif months < 6:
    # More than 3 months but less than 6 months, be cautious
    print(Fore.YELLOW + "Coin is older than 3 months but be cautious!")
else:
    # More than 6 months, relatively trustable
    print(Fore.GREEN + "Coin is older than 6 months!")