# reddit_data.py

import praw
import os
from dotenv import load_dotenv
import pandas

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv("USER_AGENT")

r = praw.Reddit(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                user_agent=USER_AGENT)


# Now to apply the above to the following subreddits:
subreddits = [
    "nba",
    "anime",
    "DnD",
    "nextfuckinglevel",
    "IAmI",
    "WTF",
    "buildapc",
    "coolguides",
    "oddlysatisfying",
    "AskWomen",
    "relationships",
    "askscience",
    "Amd",
    "OutOfTheLoop",
    "AmItheAsshole",
    "IdiotsInCars",
    "unpopularopinion",
    "TwoXChromosomes",
    "Piracy",
    "Unexpected",
    "television",
    "copypasta",
    "insaneparents",
    "soccer",
    "OldSchoolCool"
]

# I replicated Josh's code when I saw just how much more
# concise it was compared with mine.
post_subreddits = []
post_title = []
post_content = []
for sub in subreddits:
    posts = r.subreddit(sub).hot(limit=100)
    for post in posts:
        post_subreddits.append(post.subreddit)
        post_title.append(post.title)
        post_content.append(post.selftext)

print(len(post_subreddits))
print(len(post_title))
print(len(post_content))

df = pandas.DataFrame({
    "subreddits" : post_subreddits,
    "post_title" : post_title,
    "post_content" : post_content})


URI = "/Users/samuel/Programming/GitHub/Lambda\ School/Projects/DataScience" 

second_half = df.to_csv(r'second_half.csv', index=False)