import requests
from datetime import datetime

# This is a test case for the data input API


address = "http://127.0.0.1:5000"

# Create a group
def create_group(name, title, description):
    post_parameters = {
        "name": name,
        "title": title,
        "description": description}
    req = requests.post(address + "/input/new_group", data=post_parameters)

# Create a subgroup in some group
def create_subgroup(group, name, title, description):
    post_parameters = {
        "name": name,
        "title": title,
        "description": description}
    req = requests.post("{}/input/{}/new_subgroup".format(address, group),
                        data=post_parameters)

# Create a source in some subgroup
def create_source(subgroup, name, title, description):
    post_parameters = {
        "name": name,
        "title": title,
        "description": description}
    req = requests.post("{}/input/{}/new_source".format(address, subgroup),
                        data=post_parameters)

# Create a source in some subgroup
def create_entry(source, timestamp, body, metatags):
    post_parameters = {
        "timestamp": timestamp,
        "body": body,
        "metatags": metatags}
    req = requests.post("{}/input/{}/new_entry".format(address, source),
                        data=post_parameters)

# Execute test
if __name__ == '__main__':
    create_group('twitter','Twitter','Twitter searches and users.')
    create_group('reddit','Reddit','Reddit subreddits.')

    create_subgroup('twitter', 'twitter_user', 'User', 'Twitter user')
    create_subgroup('twitter', 'twitter_search', 'Search', 'Twitter search')
    create_subgroup('twitter', 'twitter_hashtag', 'Hashtag', 'Twitter hashtag')
    create_subgroup('reddit', 'reddit_subreddit', 'Subreddit',
                    'Reddit subreddit')

    create_source('twitter_search',
                  'twitter_s_crypto',
                  'Search: crypto',
                  'Twitter search for the term \'crypto\'')
    create_source('twitter_hashtag',
                  'twitter_h_bitcoin',
                  'Hashtag: bitcoin',
                  'Twitter search for the hashtag \'bitcoin\'')
    create_source('twitter_user',
                  'twitter_u_crypto',
                  'User: bitcoin',
                  'Twitter tweets of the user \'bitcoin\'')
    create_source('reddit_subreddit',
                  'reddit_s_bitcoin',
                  'Subreddit: Bitcoin',
                  "Submissions and comments in subreddit"
                  "Bitcoin")
    create_source('reddit_subreddit',
                  'reddit_s_btc',
                  'Subreddit: BTC',
                  "Submissions and comments in subreddit"
                  "BTC")
    create_entry('reddit_s_btc',
                 datetime.timestamp(datetime.utcnow()),
                 "New to the club. I bought 0.0004 btc.",
                 "submission")
    
