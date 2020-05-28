import praw
import requests
import pandas as pd
import numpy as np 
import time


reddit = praw.Reddit(client_id='xxxxxxx', client_secret='xxxxx', user_agent='reddit flask')

def reddit_to_csv(subreddit, filename, n_requests):
    """
    arg:
        The function 'reddit_to_csv' will take three arguments -
        1. the subreddit being scraped; 
        2. the filename, or the name the csv file will be given; and 
        3. the number of requests the user would like to make of reddit's API.

    returns:
        dataframe of scrapped subreddit, post_title, post_paragraph
    """
    #Create an empty list to be used later in function:
    posts = []

    #Create User-Agent to avoid 429 res.status_code:
    headers = {'User-Agent': 'user_agent'}
    #Establish that 'after' (a variable used later) is None type:
    after = None
    #for loop n_requests iterations (n_requests is established by user):
    for i in range(n_requests):
        #Print i to inform user how far along function is:
        print(i)
        #At first, 'after' will be None, as established above, making params, initially, an empty dictionary
        #without any parameters set.  After the first iteration, 'after' will be given a value containing an id
        #tag of the last post pulled in that iteration's request, allowing the function to continue looping
        #through the next set of posts instead of continuously pulling the same 25 posts, for example.
        if after == None:
            params = {}
        else:
            params = {'after': after}
        #Assign 'url' to reddit's base url, plus whatever subreddit the user provides, plus .json for clean results:
        url = 'https://www.reddit.com/r/' + str(subreddit) + '/.json'
        #Set my res variable equal to the results from requests.get, and the parameters set above like 'url' or 'params':
        res = requests.get(url, params = params, headers = headers)
        #Conditional statement to ensure access to the API is approved:
        if res.status_code == 200:
            the_json = res.json()
            for x in range(len(the_json['data']['children'])):
                #Create temporary dictionary to add results of each post to:
                temp_dict = {}
                #After looking through the json results, I've selected the below information about the posts
                #as those that can potentially add value to my model's results.
                temp_dict['subreddit'] = the_json['data']['children'][x]['data']['subreddit']
                temp_dict['title'] = the_json['data']['children'][x]['data']['title']
                temp_dict['post_paragraph'] = the_json['data']['children'][x]['data']['selftext']
                #Add the temporary dictionary to 'posts',the list of each post's dictionary of information:
                posts.append(temp_dict)
            after = the_json['data']['after']
        else:
            print(res.status_code)
            break
        #Enter a delay of one second in the requests to reddit's API for good internet citizenship:    
        time.sleep(1)
    #Turn the list of post dictionaries into a pandas DataFrame:
    posts_df = pd.DataFrame(posts)
    #Drop any duplicate rows that may have been pulled:
    posts_df.drop_duplicates(inplace = True)
    # #Rearrange the columns into a more logical order:
    # posts_df = posts_df[['subreddit', 'title', 'text' ]]
    #Save the DataFrame as a .csv file:
    posts_df.to_csv(str(filename), index = False, sep = ",")

# list of Top 50 subreddits
subber = ['home', 'askreddit', 'coronavirus', 'worldnews', 'politics', 'choosingbeggars', 
'leagueoflegends', 'nostupidquestions', 'gaming', 
'pcmasterrace', 'movies', 'todayilearned', 'teenagers', 'explainlikeimfive', 'askmen', 'personalfinance', 
'tinder', 'relationship_advice', 'news', 'discordapp', 'wallstreetbets', 'mildlyinteresting', 'interestingasfuck', 
'showerthoughts', 'wellthatsucks', 'nba', 'anime', 'dnd', 'nextfuckinglevel', 'iama', 'wtf', 'buildapc', 'coolguides',
'oddlysatisfying', 'askwomen', 'relationships', 'askscience', 'amd', 'outoftheloop', 
'amitheasshole', 'idiotsincars', 'unpopularopinion', 'twoxchromosomes', 
'piracy', 'unexpected', 'television', 'copypasta', 'insaneparents', 'soccer', 'oldschoolcool']

# Loop through list of subreddits and pass items as arg to the function
i = 0
for sub in subber:
    filename = 'scrapped_data' + str(i) + '.csv'
    final_df = pd.DataFrame()
    reddit_to_csv(sub, filename ,n_requests=10)
    i += 1


# List of saved csv files -- not DRY code
csv_file_list = ['scrapped_data0.csv', 'scrapped_data1.csv', 'scrapped_data2.csv', 'scrapped_data3.csv',
 'scrapped_data4.csv', 'scrapped_data5.csv', 'scrapped_data6.csv', 'scrapped_data7.csv', 
 'scrapped_data8.csv', 'scrapped_data9.csv','scrapped_data10.csv', 'scrapped_data11.csv', 
 'scrapped_data12.csv', 'scrapped_data13.csv', 'scrapped_data14.csv', 'scrapped_data15.csv', 
'scrapped_data16.csv', 'scrapped_data17.csv', 'scrapped_data18.csv', 'scrapped_data19.csv', 
'scrapped_data20.csv', 'scrapped_data21.csv', 'scrapped_data22.csv', 'scrapped_data23.csv', 
'scrapped_data24.csv', 'scrapped_data25.csv', 'scrapped_data26.csv', 'scrapped_data27.csv', 
'scrapped_data28.csv', 'scrapped_data29.csv', 'scrapped_data30.csv', 'scrapped_data31.csv', 
'scrapped_data32.csv', 'scrapped_data33.csv', 'scrapped_data34.csv', 'scrapped_data35.csv', 
'scrapped_data36.csv', 'scrapped_data37.csv', 'scrapped_data38.csv', 'scrapped_data39.csv', 
'scrapped_data40.csv', 'scrapped_data41.csv', 'scrapped_data42.csv', 'scrapped_data43.csv', 
'scrapped_data44.csv', 'scrapped_data45.csv', 'scrapped_data46.csv', 'scrapped_data47.csv',
 'scrapped_data48.csv', 'scrapped_data49.csv']

list_of_dataframes = []
for filename in csv_file_list:
    list_of_dataframes.append(pd.read_csv(filename))

final_df = pd.concat(list_of_dataframes)
# Drop duplicates
final_df.drop_duplicates(inplace = True)
#Save the DataFrame as a .csv file:
final_df.to_csv('final_df.csv', index = False)

# Alternative function to read in CSV and save files
#  Asssuming we name list of CSVs as files
files = []

def reader(f):
    """
    arg: item(s) from list of saved csvs
    returns: the read csv 
    """
    d = read_csv(f, index_col=0, header=None, axis=1)
    d.columns = range(d.shape[1])
    return d

df = concat([reader(f) for f in files], keys=files)