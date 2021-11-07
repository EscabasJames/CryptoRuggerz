import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import os
import colorama
from colorama import Fore

global TWITTERSCORE

print(Fore.LIGHTGREEN_EX + "\n============ STARTING TWITTER ACTIVITY CHECK ============\n" + Fore.RESET)

plt.style.use('fivethirtyeight')

consumer_key = "grqw2xsNIP3tcVzTuAJbCOxjq"
consumer_secret = "OTSc0lyRxc2woBamEG2jrsDvqoveXSgZzZnoiltLPkI1hBwRmS"
access_token = "382060044-AhEAmVqwJvBRMjtSn7MvqRTsj1SNR7zB8xJgYGSJ"
access_token_secret = "4vZHR9i7k636Y35itCp7QVSy7Lr3ET0ESUN7UpBWGpMwI"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


while True:
    choice = input("Choose the twitter account you would want to analyse: ")
    # count = 100 means 100 latest post
    posts = api.user_timeline(screen_name = choice, count= 100, tweet_mode="extended")
    # print("Show the 5 recent tweets: \n")
    i = 1
    for tweet in posts[0:5]:
        # print(str(i) + ')   '+ tweet.full_text + '\n')
        i = i + 1

    # Create dataframe with column called tweets
    df = pd.DataFrame([tweet.full_text for tweet in posts], columns=['Tweets'])

    #Show the first 5 rows of data
    # print(df.head())

    #Clean Text

    #Clean tweets using function
    def cleanTxt(text):
        #removes @mentions
        text = re.sub(r'@[A-Za-z0-9]+', '', text)
        #removes #
        text = re.sub(r'#', '', text)
        #removes retweets
        text = re.sub(r'RT[\s]+', '', text)
        #removes url/ hyperlink
        text = re.sub(r'https?:\/\/\S+', '', text)

        return text
    #Cleaning the text
    df['Tweets']= df['Tweets'].apply(cleanTxt)

    #Show Clean Text
    # print(df)

    #Create a function to get the subjectivity
    def getSubjectivity(text):
        return TextBlob(text).sentiment.subjectivity

    #Create a function to get polarity
    def getPolarity(text):
        return TextBlob(text).sentiment.polarity

    #create 2 columns
    df['Subjectvity'] = df['Tweets'].apply(getSubjectivity)
    df['Polarity'] = df['Tweets'].apply(getPolarity)

    # print(df)

    # Plot the Word Cloud
    allWords = ' '.join([twts for twts in df['Tweets']])
    wordCloud = WordCloud(width=500, height=300, random_state=21, max_font_size = 110).generate(allWords)

    plt.imshow(wordCloud, interpolation= "bilinear")
    plt.axis('off')
    plt.show()

    #Create function that computes negative, neutral and positive analysis
    def getAnalysis(score):
        # if score<0:
        #     return 'Negative'
        if score > 0.24:
            return 'Positive'
        elif score < 0:
            return 'Negative'
        else:
            return 'Neutral'

    df['Analysis']= df['Polarity'].apply(getAnalysis)

    #show analysis
    # print(df)

    # Plot the polarity and subjectivity
    plt.figure(figsize=(8,6))
    for i in range(0, df.shape[0]):
        plt.scatter(df['Polarity'][i], df['Subjectvity'][i], color='Blue')

    plt.title('Sentiment Analysis')
    plt.xlabel('Polarity')
    plt.ylabel('Subjectivity')
    plt.show()

    # #print all the positive tweets
    # j = 1
    # sortedDF = df.sort_values(by=['Polarity'])
    # for i in range(0, sortedDF.shape[0]):
    #     if(sortedDF['Analysis'][i] == 'Positive'):
    #         print(str(j) + ') '+sortedDF['Tweets'][i])
    #         print()
    #         j = j+1

    # #print the negative tweets
    # j = 1
    # sortedDF = df.sort_values(by=['Polarity'], ascending='False')
    # for i in range(0, sortedDF.shape[0]):
    #     if(sortedDF['Analysis'][i] == 'Negative'):
    #         print(str(j) + ') '+sortedDF['Tweets'][i])
    #         print()
    #         j = j+1


    #Get the percentage of positive tweets
    ptweets = df[df.Analysis == 'Positive']
    ptweets = ptweets['Tweets']

    round((ptweets.shape[0] / df.shape[0]) *100, 1)

    #Get the percentage of negative tweets
    ntweets = df[df.Analysis == 'Negative']
    ntweets = ntweets['Tweets']

    round((ntweets.shape[0] / df.shape[0]) *100, 1)

    #Show the value counts

    df['Analysis'].value_counts()

    #plot and visualize the counts
    plt.title('Sentiment Analysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Counts')
    df['Analysis'].value_counts().plot(kind='bar')
    plt.show()
    #num of positive comments out of the total tested
    p = round((ptweets.shape[0] / df.shape[0]) *100, 1)
    if p >= 40:
        print("HIGH RISK: High Chance it being Rug Pull")
        TWITTERSCORE = 0
    elif p > 30 and p < 40:
        print("MEDIUM RISK: Do more Checking")
        TWITTERSCORE = 5
    else:
        print("LOW RISK: Can never be too sure")
        TWITTERSCORE = 10

    decision = input("Do you want to analyse another twitter account? (please enter yes or no)\n")
    if decision == "no":
        print("Exiting...")
        break
    elif decision == "yes":
        print("--------------------------------------------------------------------------")
    else:
        decision = input("You have entered an invalid input, whats your decision again?\n")

print(Fore.RED + "\n============ END OF TWITTER ACTIVITY CHECK ============\n" + Fore.RESET)
