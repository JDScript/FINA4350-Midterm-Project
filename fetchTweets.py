from datetime import date, datetime
from itertools import count
import json
import tweepy

# Initialize Twitter's API Client
appKey = "L0h53tDWdEhC2lJPpTd18Z2cG"
appSecret = "yZUSh7eDlDOpdehtj2PH9Roa6umCzmyUk6FD1H4YhcekiiUtf6"

auth = tweepy.OAuth2AppHandler(appKey, appSecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Custom JSON Encoder for datetime
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


# Search for CASHTAG related tweets (Since twitter only allows for 7-day search)
result = []
targetNum = 53500
maxId = None
while len(result) < targetNum:
    if maxId:
        tweets = api.search_tweets(q="$TSLA", lang="en", count=100, max_id=maxId)
    else:
        tweets = api.search_tweets(q="$TSLA", lang="en", count=100)
    for tweet in tweets:
        # Only record data we need
        result.append(
            {
                "id": tweet.id,
                "text": tweet.text,
                "truncated": tweet.truncated,
                "user": {
                    "name": tweet.user.name,
                    "screen_name": tweet.user.screen_name,
                    "followers": tweet.user.followers_count,
                    "verified": tweet.user.verified,
                },
                "favorite_count": tweet.favorite_count,
                "retweet_count": tweet.retweet_count,
                "created_at": tweet.created_at,
            }
        )
        if maxId == None or tweet.id < maxId:
            maxId = tweet.id
    print("Fetched: {}/{}".format(len(result), targetNum))

result = json.dumps(result, cls=CustomEncoder)
with open("./tweets.json", "w") as f:
    f.write(result)
    f.close()
