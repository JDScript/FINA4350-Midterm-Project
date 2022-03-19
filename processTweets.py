from collections import defaultdict
import json
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import ssl
import matplotlib.pyplot as plt

# Download datasets from nltk
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download("vader_lexicon")

# Open file to read tweets data
with open("./tweets.json", "r") as f:
    data = json.load(f)
    print("Successfully read data from file")

# Do text-preprocessing
# 1. Remove link in tweets
# 2. Remove @xxx in tweets, they're useless
# 3. Remove $xxx in tweets, they're just for scratching
# 4. Remove punctuation and special characters, nothing to do with emotion analyze
def cleanTweet(s):
    # 1. Remove links
    s = re.sub("[a-z]*[:.]+\S+", "", s)
    # 2~3. Remove tags...
    s = re.sub("[@$][\w_-]+", "", s)
    # 4. Remove punctuation and special characters
    s = re.sub("[^A-Z^a-z^0-9^ ]", "", s)
    return s


# This function is a factory function
def statisticsPerDay():
    return {"total": 0, "positive": 0, "neutral": 0, "negative": 0}

# For counting each day's tweets stats
tweetsStats = defaultdict(statisticsPerDay)
# For analyzing emotions
sia = SentimentIntensityAnalyzer()
for tweet in data:
    # Clean tweets
    tweet["text"] = cleanTweet(tweet["text"])
    # Count the number of tweets each day
    createdAt = str(tweet["created_at"]).split()[0]
    tweetsStats[createdAt]['total'] += 1
    # Retrieve the emotion by NLTK
    emotion = sia.polarity_scores(tweet["text"])
    if emotion['compound'] >= 0.05:
        # Regarded as positve
        tweetsStats[createdAt]['positive'] += 1
    elif emotion['compound'] <= -0.05:
        # Regarded as negative
        tweetsStats[createdAt]['negative'] += 1
    else:
        # Regarded as neutral
        tweetsStats[createdAt]['neutral'] += 1

print(json.dumps(tweetsStats))