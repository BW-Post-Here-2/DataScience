# Co-written by Samuel Swank (DS14) and Josh Black-Star (DS14)

# TODO:
# Force spreadsheet to include post ID for Joo Woon (and rest of web dev side)
# Prediction output per post is tuple of ('Subreddit name' : probablility) eg. ('worldnews':0)

import praw
import pandas as pd

import os
from dotenv import load_dotenv

PRAW_CLIENT_ID = os.getenv("PRAW_CLIENT_ID", default="oops")
PRAW_CLIENT_SECRET = os.getenv("PRAW_CLIENT_SECRET", default="oops")
PRAW_USER_AGENT = os.getenv("PRAW_USER_AGENT", default="oops")

r = praw.Reddit(client_id=PRAW_CLIENT_ID, client_secret=PRAW_CLIENT_SECRET, user_agent=PRAW_USER_AGENT)

#
# -----------------------------------------------------------------
#

subreddits = ['Home', 'AskReddit', 'Coronavirus' , 'worldnews', 'politics', 'ChoosingBeggars', 'leagueoflegends', 'NoStupidQuestions', 
'gaming', 'pcmasterrace', 'movies', 'todayilearned', 'teenagers', 'explainlikeimfive', 'AskMen', 'personalfinance', 'Tinder', 
'relationship_advice', 'news', 'discordapp', 'wallstreetbets', 'mildlyinteresting', 'interestingasfuck', 'Showerthoughts', 
'Wellthatsucks', 'nba', 'anime', 'DnD', 'nextfuckinglevel', 'IAmA', 'WTF', 'buildapc', 'coolguides', 'oddlysatisfying', 'AskWomen', 
'relationships', 'askscience', 'Amd', 'OutOfTheLoop', 'AmItheAsshole', 'IdiotsInCars', 'unpopularopinion', 'TwoXChromosomes', 'Piracy', 
'Unexpected', 'television', 'copypasta', 'insaneparents', 'soccer', 'OldSchoolCool']

post_subreddits = []
post_title = []
post_content = []

for sub in subreddits:
    posts = r.subreddit(sub).hot(limit=200)
    for post in posts:
        post_subreddits.append(post.subreddit)
        post_title.append(post.title)
        post_content.append(post.selftext)

# print(len(post_subreddits))
# print(len(post_title))
# print(len(post_content))
df = pd.DataFrame({
    "subreddits" : post_subreddits,
    "post_title" : post_title,
    "post_content" : post_content})

df.to_csv('model_data.csv', index=False)