import san
import pprint
import datetime
import pandas as pd
from simple_colors import *
from dateutil.relativedelta import relativedelta
import dateutil
from tabulate import tabulate
import colorama
from colorama import Fore

global GITACTSCORE

print(Fore.LIGHTGREEN_EX + "\n============ STARTING GIT ACTIVITY CHECK ============\n" + Fore.RESET)


san.ApiConfig.api_key = '46lecer3pqbes4nf_tjr6udpblnrtxapq'

'''Development Activity Metric
The 'pure' development activity. It excludes events that are not development related like:
Comments on issues
Issues created and closed
Creating of forks
Comments on commits
People following an issue
Downloading releases
Watching a repository
Project management events
This allows to better compare projects that use github for issue tracking and projects that do not use github for issue tracking. 
If such events are not excluded then the second project could have inflated activity just by discussion what they are going to build without actually building it.
'''

#getting today's date
today =  datetime.date.today()
d1 = today.strftime("%Y-%m-%d")

#3months
three_months = datetime.timedelta(4*365/12)
dateFrom3Months = (today - three_months)
d2 = dateFrom3Months.strftime("%Y-%m-%d")

#Standard coin that the user's coin will be compared against: Ethereum as it is the leading altcoin project
#get the first starting date of github activity for ETH
SDA4ETH = san.available_metric_for_slug_since(metric='dev_activity', slug='ethereum') 
#get the first starting date of dev_activity_contributors_count for ETH
SDAC4ETH = san.available_metric_for_slug_since(metric='dev_activity_contributors_count', slug='ethereum') 
#get the total number of ETH dev activity per month since its inception
noOfETHDevActivity = san.get(
    "dev_activity/ethereum",
    from_date=SDA4ETH,
    to_date=d1,
    interval="4w"
)

#get the unique number of ETH dev that contributed per month since its inception
noOfETHDevConPerMonth = san.get(
    "dev_activity_contributors_count/ethereum",
    from_date=SDA4ETH,
    to_date=d1,
    interval="4w"
)

#print("Descriptive statistics of ETH's Github activity per month")
#descriptive statistic of ETH's development activity
desStatETHDevAct = noOfETHDevActivity.describe()
#print(desStatETHDevAct)
meanETHACT = desStatETHDevAct.iloc[1]['value']
medianETHACT = desStatETHDevAct.iloc[5]['value']

#print("Descriptive statistics of number of unique ETH Developer that contributed per month")
#descriptive statistic of number of unique ETH Developer that contributed per month
desStatETHDevCon = noOfETHDevConPerMonth.describe()
#print(desStatETHDevCon)
meanETHCON = desStatETHDevCon.iloc[1]['value']
medianETHCON = desStatETHDevCon.iloc[5]['value']
meanETHRatio = meanETHACT/ meanETHCON
medianETHRatio = medianETHACT/medianETHCON

tryflag =1
start = True
#Coin that user wish to analyze
while(start == True):
    try:
        if tryflag ==1:
            nameOfCoin = input(Fore.LIGHTGREEN_EX + "\nEnter name of Coin for analysis or enter SKIP to skip git commits analysis: " + Fore.RESET)
            if nameOfCoin == "SKIP":
                tryflag = 0
                break
            #get the first starting date of github activity for nameOfCoin
            SDA4COIN = san.available_metric_for_slug_since(metric='dev_activity', slug=nameOfCoin)
            SDACC4COIN = san.available_metric_for_slug_since(metric='dev_activity_contributors_count', slug=nameOfCoin) 
            #get the number of dev activity per month since its inception
            noOfDevActivity = san.get(
                "dev_activity"+ "/" + nameOfCoin,
                from_date=SDA4COIN,
                to_date=d1,
                interval="4w"
            )

            #get the unique number of dev that contributed per month since its inception
            noOfDevPerMonth = san.get(
                "dev_activity_contributors_count" + "/" + nameOfCoin,
                from_date=SDACC4COIN,
                to_date=d1,
                interval="4w"
            )

    except Exception:
        print("Coin doesnt exist in database or wrong spelling")
        continue
    break

if tryflag != 0:
    #nameOfCoin = input("\nEnter name of Coin for analysis: ")
    #Flag for mean or median
    exit = 0
    flag = 0
    while (exit == 0):
        mode = input("Mean or Median as mode of measure: ")
        if mode == "Mean" or mode == "mean":
            flag = 1
            exit =1
        elif mode == "Median" or mode == "median":
            flag = 2
            exit = 1
        else:
            exit = 0
    #get the first starting date of github activity for nameOfCoin
    #SDA4COIN = san.available_metric_for_slug_since(metric='dev_activity', slug=nameOfCoin) 
    #get the first starting date of dev_activity_contributors_count for nameOfCoin
    #SDACC4COIN = san.available_metric_for_slug_since(metric='dev_activity_contributors_count', slug=nameOfCoin) 


    print("\nDescriptive statistics of "+ nameOfCoin +" Github activity per month")
    #get Descriptive statistics of developer activity of coin
    coinStatGitAct=noOfDevActivity.describe()
    #print(coinStatGitAct)
    #print(noOfDevActivity)
    coinGitActHistMean = coinStatGitAct.iloc[1]['value']
    coinGitActHistMedian = coinStatGitAct.iloc[5]['value']
    coinGitActHistSTD = coinStatGitAct.iloc[2]['value']
    print("Mean " + nameOfCoin + " github activity per month: "+str(coinGitActHistMean))
    print("Median " + nameOfCoin + " github activity per month: "+str(coinGitActHistMedian))
    print("Standard Deviation " + nameOfCoin + " github activity per month: "+str(coinGitActHistSTD))

    print("\nDescriptive statistics of number of unique "+ nameOfCoin +" Developer that contributed per month")
    # get Descriptive statistics of the number of unique developer that contributed to coin
    coinStatGitCon=noOfDevPerMonth.describe()
    #print(coinStatGitCon)
    #print(noOfDevPerMonth)
    coinGitConHistMean = coinStatGitCon.iloc[1]['value']
    coinGitConHistMedian = coinStatGitCon.iloc[5]['value']
    coinGitConHistSTD = coinStatGitCon.iloc[2]['value']
    print("Mean " + nameOfCoin +" unique Developers that contributed per month: "+str(coinGitConHistMean))
    print("Median " + nameOfCoin + " unique Developers that contributed per month: "+str(coinGitConHistMedian))
    print("Standard Deviation " + nameOfCoin + " unique Developers that contributed per month: "+str(coinGitConHistSTD))
    print("\nStart date of github activity: "+ SDA4COIN)

    #get the number of dev activity from the past 3 month
    recent3MonthDevActivity = san.get(
        "dev_activity"+ "/" + nameOfCoin,
        from_date= d2,
        to_date=d1,
        interval="4w"
    )
    #print(recent3MonthDevActivity)

    #get date for 3 months
    a_date = datetime.datetime.strptime(str(dateFrom3Months),"%Y-%m-%d")
    a_month = dateutil.relativedelta.relativedelta(months=1)
    date_plus_month = a_date + a_month
    date3 = date_plus_month + a_month
    datelist = []
    datelist.append(d2)
    datelist.append(date_plus_month.strftime("%Y-%m-%d"))
    datelist.append(date3.strftime("%Y-%m-%d"))


    k = 0
    recent3MonthACTCount = []
    for x in range(0, 3):
        recent3MonthACTCount.append(recent3MonthDevActivity.iloc[x,0])   


    #get the number of unique number of dev that contributed per month from the past 3 month
    recent3MonthNoOfDevCont = san.get(
        "dev_activity_contributors_count" + "/" + nameOfCoin,
        from_date= d2,
        to_date=d1,
        interval="4w"
    )
    #print(recent3MonthNoOfDevCont)
    recent3MonthDevCount = []
    for x in range(0, 3):
        recent3MonthDevCount.append(recent3MonthNoOfDevCont.iat[x,0])


    print("\n" + nameOfCoin + " Recent 3 month Statistic per Month")
    print("Date                     Number of Developer Activity                     Number of Developer That Contributed")
    for i in recent3MonthACTCount:
        print(str(datelist[k]) + "               " + str(i) + "                                             " + str(recent3MonthDevCount[k]))
        k+=1

    #checks
    score = 0

    postivedifference = 0
    negativedifference = 0

    print("")
    print(green("Green = Very Safe/ Very Good -- 3",'bold'))
    print(blue("Blue = Safe/ Good -- 2",'bold'))
    print(yellow("Yellow = Caution -- 1",'bold'))
    print(red("Red = unsafe/ Bad -- 0",'bold'))
    print("\nChecks for the Developer's Activity For the Past 3 months:")
    #loop through selected coin's past 3 months github developer activity using MEAN
    if (flag == 1):
        print(nameOfCoin + " historical MEAN Developer Activity per month: "+ str(coinGitActHistMean))
        print("Date             Number of Developer Activity             Metric")
        for x in range(3):
            #check if the coin's recent 3 month developer github activity is more than its historical mean per month activity
            if (recent3MonthACTCount[x]> coinGitActHistMean):
                postivedifference = recent3MonthACTCount[x]-coinGitActHistMean
                #check if the postive diffrence is higher than the standard deviation
                if (postivedifference >= coinGitActHistSTD):
                    score+=3
                    print(green(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEAN",'bold'))
                else:
                    score+=2
                    #print("MEAN dev activity good : " + str(x))
                    print(blue(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEAN",'bold'))
            #check if the coin's recent 3 month developer github activity is lesser than its historical mean per month activity
            if (recent3MonthACTCount[x]<= coinGitActHistMean):
                negativedifference = coinGitActHistMean - recent3MonthACTCount[x]
                #check if 0
                if recent3MonthACTCount[x] <= 0:
                    score+=0
                    print(red(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEAN",'bold'))
                #check if the negative diffrence is higher than the standard deviation
                elif (negativedifference >= coinGitActHistSTD):
                    score+=0
                    #print("MEAN dev activity  very bad : " + str(x))
                    print(red(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEAN",'bold'))
                else:
                    score+=1
                    #("MEAN dev activity bad : " + str(x))
                    print(yellow(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEAN",'bold'))


    if (flag == 2):
        print(nameOfCoin + " historical MEDIAN Developer Activity per month: "+ str(coinGitActHistMedian))
        print("Date             Number of Developer Activity             Metric")
        #loop through selected coin's past 3 months github developer activity using MEDIAN
        for x in range(3):
            #check if the coin's recent 3 month developer github activity is more than its historical median per month activity
            if (recent3MonthACTCount[x]> coinGitActHistMedian):
                postivedifference = recent3MonthACTCount[x]-coinGitActHistMedian
                #check if the postive diffrence is higher than the standard deviation
                if (postivedifference >= coinGitActHistSTD):
                    score+=3
                    #print("MEDIAN dev activity  very good : " + str(x))
                    print(green(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEDIAN",'bold'))
                else:
                    score+=2
                    #print("MEDIAN dev activity  good : " + str(x))
                    print(blue(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEDIAN",'bold'))
            #check if the coin's recent 3 month developer github activity is lesser than its historical median per month activity
            if (recent3MonthACTCount[x]<= coinGitActHistMedian):
                negativedifference = coinGitActHistMedian - recent3MonthACTCount[x]
                if recent3MonthACTCount[x] <= 0:
                    score+=0
                    print(red(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEDIAN",'bold'))
                #check if the negative diffrence is higher than the standard deviation
                elif (negativedifference >= coinGitActHistSTD):
                    score+=0
                    #("MEDIAN dev activity very bad : " + str(x))
                    print(red(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEDIAN",'bold'))
                else:
                    score+=1
                    #("MEDIAN dev activity bad : " + str(x))
                    print(yellow(str(datelist[x])+ "           "+ str(recent3MonthACTCount[x]) + "                                 MEDIAN",'bold'))


    print("\nChecks for the unique number of Developers that contributed For the Past 3 months:")
    if (flag == 2):
        print(nameOfCoin + " historical MEDIAN number of Developers that contributed per month: "+ str(coinGitConHistMedian))
        print("Date             Number of Developer             Metric")
        #loop through selected coin's past 3 months unique number of developer that contributed using MEDIAN
        for x in range(3):
            #check if the coin's recent 3 month unique number of developers that contributed is higher than its historical median number of unique developer that contributed per month 
            if (recent3MonthDevCount[x]> coinGitConHistMedian):
                postivedifference = recent3MonthDevCount[x]-coinGitConHistMedian 
                #check if the positive diffrence is higher than the standard deviation
                if (postivedifference >= coinGitConHistSTD):
                    score+=3
                    #print("MEDIAN dev activity very good : " + str(x))
                    print(green(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEDIAN",'bold'))
                else:
                    score+=2
                    #print("MEDIAN dev activity good : " + str(x))
                    print(blue(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEDIAN",'bold'))
            #check if the coin's recent 3 month unique number of developers that contributed is higher than its historical median number of unique developer that contributed per month 
            if (recent3MonthDevCount[x]<= coinGitConHistMedian):
                negativedifference = coinGitConHistMedian - recent3MonthDevCount[x]
                if recent3MonthDevCount[x] <= 0:
                    score+=0
                    print(red(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEDIAN",'bold'))
                #check if the negative diffrence is higher than the standard deviation
                elif (negativedifference >= coinGitConHistSTD):
                    score+=0
                    #print("MEDIAN dev activity very bad : " + str(x))
                    print(red(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEDIAN",'bold'))
                else:
                    score+=1
                    #print("MEDIAN dev activity bad : " + str(x))
                    print(yellow(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEDIAN",'bold'))

    if (flag == 1):
        print(nameOfCoin + " historical MEAN number of Developers that contributed per month: "+ str(coinGitConHistMean))
        print("Date             Number of Developer             Metric")
        #loop through selected coin's past 3 months unique number of developer that contributed using MEAN
        for x in range(3):
            #check if the coin's recent 3 month unique number of developers that contributed is higher than its historical mean number of unique developer that contributed per month 
            if (recent3MonthDevCount[x]> coinGitConHistMean):
                postivedifference = recent3MonthDevCount[x]-coinGitConHistMean
                #check if the positive diffrence is higher than the standard deviation
                if (postivedifference >= coinGitConHistSTD):
                    score+=3
                    #print("MEAN dev very good : " + str(x))
                    print(green(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEAN",'bold'))
                else:
                    score+=2
                    #print("MEAN dev good : " + str(x))
                    print(blue(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEAN",'bold'))
            #check if the coin's recent 3 month unique number of developers that contributed is lower than its historical mean number of unique developer that contributed per month 
            if (recent3MonthDevCount[x]<= coinGitConHistMean):
                negativedifference = coinGitConHistMean - recent3MonthDevCount[x]
                if recent3MonthDevCount[x] <= 0:
                    score+=0
                    print(red(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEAN",'bold'))
                #check if the negative diffrence is higher than the standard deviation
                elif (negativedifference >= coinGitConHistSTD):
                    score+=0
                    #print("MEAN dev activity very bad : " + str(x))
                    print(red(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEAN",'bold'))
                else:
                    score+=1
                    #print("MEAN dev activity bad : " + str(x))
                    print(yellow(str(datelist[x])+ "           "+ str(recent3MonthDevCount[x]) + "                                 MEAN",'bold'))



    #get the average number of contribution a dev will make per month
    meanaveragecontri = 0
    meanaveragecontri = coinGitActHistMean/ coinGitConHistMean
    medianaveragecontri = 0
    medianaveragecontri = coinGitActHistMedian/ coinGitConHistMedian
    extra =0

    if flag == 1:
        if meanaveragecontri >= meanETHRatio:
            print(green("\n" + str(nameOfCoin) +"'s historical Mean Github contribution per developer: " + str(meanaveragecontri) + " is higher or equals to ETH's: " + str(meanETHRatio),'bold'))
            extra = 3
        else:
            print(red("\n" + str(nameOfCoin) +"'s historical Mean Github contribution per developer: " + str(meanaveragecontri) + " is lower than ETH's: " + str(meanETHRatio),'bold'))
            extra = 0

    if flag == 2:
        if medianaveragecontri >= medianETHRatio:
            print(green("\n" + str(nameOfCoin) +"'s historical Median Github contribution per developer: " + str(medianaveragecontri) + " is higher or equals to ETH's: " + str(medianETHRatio),'bold'))
            extra  = 3
        else:
            print(red("\n" + str(nameOfCoin) +"'s historical Median Github contribution per developer: " + str(medianaveragecontri) + " is lower than ETH's: " + str(medianETHRatio),'bold'))
            extra = 0

    score += extra
    print("Score is : "+ str(score)+ "/ 21")
    GITACTSCORE = (score / 21) * 0.1
    print(Fore.RED + "\n============ END OF GIT ACTIVITY CHECK ============\n" + Fore.RESET)
    # print(green("ETH Median number of activty per developer: " + str(),'bold'))
    # print("\n"+str(nameOfCoin) +"'s Mean Average contribution per developer: "+ str(meanaveragecontri))
    # print(str(nameOfCoin) +"'s Median Average contribution per developer: "+ str() + "\n")


else:
    print(Fore.RED + "\n============ GIT ACTIVITY CHECK SKIPPED! ============\n" + Fore.RESET)
    GITACTSCORE = 0




