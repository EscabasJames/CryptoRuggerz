import requests
import json
import time
import datetime

# Get 30 days
today =  datetime.date.today()
d1 = today.strftime("%-%m-%d")

three_months = datetime.timedelta(4*365/12)
dateFrom3Months = (today - three_months)
d2 = dateFrom3Months.strftime("%Y-%m-%d")
d2 = d2 + "T00:00:00Z"

slug = input("Please enter coin slug name:\n")

# Get social volume of coin
socialVolStr = "http://api.santiment.net/graphiql?query={getMetric(metric:\"social_volume_total\"){timeseriesData(selector:{slug:\""+slug+"\"}\nfrom:\""+d2+"\"\nto:\"utc_now\"\ninterval:\"4w\"){\ndatetime\nvalue}}}"

# Get social dominance of coin
socialDomStr = "http://api.santiment.net/graphiql?query={getMetric(metric:\"social_dominance_total\"){timeseriesData(selector:{slug:\""+slug+"\"}\nfrom:\""+d2+"\"\nto:\"utc_now\"\ninterval:\"4w\"){\ndatetime\nvalue}}}"

# Get postive sentiments of coin
socialPosStr = "http://api.santiment.net/graphiql?query={getMetric(metric:\"sentiment_positive_total\"){timeseriesData(selector:{slug:\""+slug+"\"}\nfrom:\""+d2+"\"\nto:\"utc_now\"\ninterval:\"4w\"){\ndatetime\nvalue}}}"

# Get negative sentiments of coin
socialNegStr = "http://api.santiment.net/graphiql?query={getMetric(metric:\"sentiment_negative_total\"){timeseriesData(selector:{slug:\""+slug+"\"}\nfrom:\""+d2+"\"\nto:\"utc_now\"\ninterval:\"4w\"){\ndatetime\nvalue}}}"

# Get unique social volume sentiments of coin
socialUniStr = "http://api.santiment.net/graphiql?query={getMetric(metric:\"unique_social_volume_total_1h\"){timeseriesData(selector:{slug:\""+slug+"\"}\nfrom:\""+d2+"\"\nto:\"utc_now\"\ninterval:\"4w\"){\ndatetime\nvalue}}}"

# Request results

socialVolRes = requests.get(socialVolStr)
socialDomRes = requests.get(socialDomStr)
socialPosRes = requests.get(socialPosStr)
socialNegRes = requests.get(socialNegStr)
socialUniRes = requests.get(socialUniStr)

# Use some pump and dump project as metrics to compare with
# Examples:
# MaidSafeCoin
# Ark
# Safemoon
# DogeElon
# Since the pump and dump timings doesn't change, gather data and fix values
# 1 month before the pump the month the pump happened and 1 month after

# DogeElon recent pump and dump data

# Averages for ark pump and dump data (Data gathered from SanApi beforehand) 
dogelonVolAvg = 16133
dogelonDomAvg = 1.06
dogelonPosAvg = 2816
dogelonNegAvg = 2355
dogelonUniAvg = 4196

# Averages for safemoon pump and dump data (Data gathered from SanApi beforehand)
safemoonVolAvg = 343410
safemoonDomAvg = 1.36
safemoonPosAvg = 8958
safemoonNegAvg = 2093
safemoonUniAvg = 19443

# Get results from JSON
volJson = json.dumps(socialVolRes.json())
domJson = json.dumps(socialDomRes.json())
posJson = json.dumps(socialPosRes.json())
negJson = json.dumps(socialNegRes.json())
uniJson = json.dumps(socialUniRes.json())

# Dump JSON into a dictionary
volJson = json.loads(volJson)
domJson = json.loads(domJson)
posJson = json.loads(posJson)
negJson = json.loads(negJson)
uniJson = json.loads(uniJson)

# Get only required data
volJsonDict = volJson["data"]["getMetric"]["timeseriesData"]
domJsonDict = domJson["data"]["getMetric"]["timeseriesData"]
posJsonDict = posJson["data"]["getMetric"]["timeseriesData"]
negJsonDict = negJson["data"]["getMetric"]["timeseriesData"]
uniJsonDict = uniJson["data"]["getMetric"]["timeseriesData"]

# Check if data does exist
if volJsonDict is None:
	print("Social Metrics for this coin does not exist yet!")

else:

	# Get only last 3 months of data
	volJsonDict = volJsonDict[-3:]
	domJsonDict = domJsonDict[-3:]
	posJsonDict = posJsonDict[-3:]
	negJsonDict = negJsonDict[-3:]
	uniJsonDict = uniJsonDict[-3:]
		
	#print(json.dumps(socialVolRes.json(), indent=2))

	# Print results
	print("\n====== Total Social Volume over 3 months ======\n")
	
	totalVol = 0
	
	print("Date\t\t\t", end="")
	print("Value")
	for i in volJsonDict:
		print(i.get("datetime"), end="")
		print("\t", end="")
		print(i.get("value"))
		totalVol += i.get("value")
	
	print("\nTotal volume:", round(totalVol))
	print("Average volume:", round(totalVol / 3))

	print("\n====== Total Social Dominance over 3 months ======\n")

	totalDom = 0
	
	print("Date\t\t\t", end="")
	print("Value")
	for i in domJsonDict:
		print(i.get("datetime"), end="")
		print("\t", end="")
		print(i.get("value"))
		totalDom += i.get("value")
	
	print("\nTotal Social Dominance :", round(totalDom))
	print("Average Social Dominance in %:", round(totalDom / 3))

	print("\n====== Total Positive Sentiment over 3 months ======\n")

	totalPos = 0
	
	print("Date\t\t\t", end="")
	print("Value")
	for i in posJsonDict:
		print(i.get("datetime"), end="")
		print("\t", end="")
		print(i.get("value"))
		totalPos += i.get("value")
	
	print("\nTotal Positive Sentiment:", round(totalPos))
	print("Average Positive Sentiment:", round(totalPos / 3))

	print("\n====== Total Negative Sentiment over 3 months ======\n")

	totalNeg = 0
	
	print("Date\t\t\t", end="")
	print("Value")
	for i in negJsonDict:
		print(i.get("datetime"), end="")
		print("\t", end="")
		print(i.get("value"))
		totalNeg += i.get("value")
	
	print("\nTotal Negative Sentiment:", round(totalNeg))
	print("Average Negative Sentiment:", round(totalNeg / 3))

	print("\n====== Total Unique Posts over 3 months ======\n")

	totalUni = 0
	
	print("Date\t\t\t", end="")
	print("Value")
	for i in uniJsonDict:
		print(i.get("datetime"), end="")
		print("\t", end="")
		print(i.get("value"))
		totalUni += i.get("value")
	
	print("\nTotal Unique Traffic:", round(totalUni))
	print("Average Unique Traffic:", round(totalUni / 3))
	
	# Calculate coin score upon 10
	# If coin distance is less than 50% do not deduct score
	
	totalScore = 10
	
	if ((totalVol / 3)  / dogelonVolAvg) < 0.5:
		totalScore -= 1
	
	if ((totalDom / 3)  / dogelonDomAvg) < 0.5:
		totalScore -= 1
		
	if ((totalPos / 3)  / dogelonPosAvg) < 0.5:
		totalScore -= 1
	
	if ((totalNeg / 3)  / dogelonNegAvg) < 0.5:
		totalScore -= 1
		
	if ((totalUni / 3)  / dogelonUniAvg) < 0.5:
		totalScore -= 1
		
	if ((totalVol / 3)  / safemoonVolAvg) < 0.5:
		totalScore -= 1
	
	if ((totalDom / 3)  / safemoonDomAvg) < 0.5:
		totalScore -= 1
		
	if ((totalPos / 3)  / safemoonPosAvg) < 0.5:
		totalScore -= 1
	
	if ((totalNeg / 3)  / safemoonNegAvg) < 0.5:
		totalScore -= 1
		
	if ((totalUni / 3)  / safemoonUniAvg) < 0.5:
		totalScore -= 1
	
	print("\n====== Comparing with coins with history of pump of dump ======")
	print("Total Score:", totalScore)
