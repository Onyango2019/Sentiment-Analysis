
# Import the Libraries

import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use("fivethirtyeight")

consumer_key = ""
consumer_key_secret = ""
access_token = ""
access_token_secret = ""



authenticate = tweepy.OAuthHandler(consumer_key, consumer_key_secret)

authenticate.set_access_token(access_token, access_token_secret)


api = tweepy.API(authenticate, wait_on_rate_limit=True)

# name = input("Enter name to search: ")
# n = int(input("Number of tweets to search: "))

posts = api.user_timeline(screen_name = "Trump",
                          count = 100000,
                          language = 'en',
                          tweet_mode = 'extended')
# print("Show the first 5 tweets")
# print()
i = 1
# for tweet in posts[0:5]:
#     print( str(i) + ')' + tweet.full_text + '\n')
#     i +=1
df = pd.DataFrame( [tweet.full_text for tweet in posts], columns=["Tweets"])
# print(df.head())


def CleanText(text):
    text = re.sub(r"@[A-Za-z0-9]+", " ", text)
    text = re.sub(r"#", " ", text)
    text = re.sub(r"RT[\s]+", " ", text)
    text = re.sub(r'https?:\/\/\S+', " ", text)
    return text

df["Tweets"] = df["Tweets"].apply(CleanText)
# print(df)

def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity


def getPolarity(text):
    return TextBlob(text).sentiment.polarity

df["Subjectivity"] = df["Tweets"].apply(getSubjectivity)
df["Polarity"] = df["Tweets"].apply(getPolarity)

# print(df)

allwords = " ".join(twts for twts in df["Tweets"])
wordcloud = WordCloud(width=500,
                      height=300,
                      random_state=21,
                      max_font_size=119).generate(allwords)
# plt.imshow(wordcloud, interpolation='bilinear')
# plt.axis('off')
# plt.show()

def getAnalysis(score):
    if score < 0:
        return "Negative"
    elif score == 0:
        return "Neutral"
    else:
        return "Positive"

df["Analysis"] = df["Polarity"].apply(getAnalysis)
# print(df)

# print all positive tweets
j =1
sortedDf = df.sort_values(by = ['Polarity'])
for i in range(0, sortedDf.shape[0]):
    if sortedDf["Analysis"][i] == "Positive":
        # print( str(j) + ')' + sortedDf["Tweets"][i])
        # print()
        j +=1

# Print the Negative Tweets
j =1
sortedDf = df.sort_values(by = ['Polarity'], ascending=False)
for i in range(0, sortedDf.shape[0]):
    if sortedDf["Analysis"][i] == "Negative":
        print( str(j) + ')' + sortedDf["Tweets"][i])
        print()
        j +=1

# Plot the Polarity and subjectivity
# plt.figure(figsize=(8,6))
# for i in range(0, df.shape[0]):
#     plt.scatter(df['Polarity'][i], df['Subjectivity'][i],
#                 color = "Blue",)
# plt.title("Sentiment Analysis")
# plt.xlabel("Polarity")
# plt.ylabel("Subjectivity")
# plt.show()


# Get the Percentage of the Positive tweets
ptweets = df[df.Analysis == 'Positive']
ptweets = ptweets['Tweets']
# print(ptweets)

print(round((ptweets.shape[0]/df.shape[0]*100), 1))


# Get the Percentage of the negative tweets
ntweets = df[df.Analysis == 'Negative']
ntweets = ntweets['Tweets']
# print(ptweets)

print(round((ntweets.shape[0]/df.shape[0]*100), 1))


# Show the Value Counts
df["Analysis"].value_counts()

# Plot and Visualize the counts\
plt.title("Sentimental Analysis")
# plt.axis("off")
plt.xlabel("Sentiment")
plt.ylabel("Counts")
df['Analysis'].value_counts().plot(kind ='bar')
plt.show()
