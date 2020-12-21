import tweepy

# Authenticate to Twitter
auth = tweepy.OAuthHandler("api-key", "api-secret")  # API key, secret
auth.set_access_token("access-key", "access-secret")  # access key, secret

# Create API object
api = tweepy.API(auth)

# validate authentication
if not api.verify_credentials():
    print("Error during Twitter Auth")
else:
    print("Twitter Auth successful")

# Create a tweet
#api.update_status("Bot test in progress....")

# read timeline
#timeline = api.home_timeline()
#for tweet in timeline:
#    print(f"{tweet.user.name} said {tweet.text}")

# get user and last 20 followers
'''
user = api.get_user("ReclusiveCoder")

print("User details:")
print(user.name)
print(user.description)
print(user.location)

print("Last 20 Followers:")
for follower in user.followers():
    print(follower.name)
'''

# searching tweets
for tweet in api.search(q="committed suicide",  rpp=10):
    print(f"--> {tweet.user.name}:   {tweet.text}")



