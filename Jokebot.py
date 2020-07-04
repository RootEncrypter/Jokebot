import pickle
import os
import praw
from keys import *
import time
import tweepy
global currentj


os.chdir('C:\\Users\\Shaun\\Desktop\\python practrice') #change directory to your current working directory

global jokeBook 
jokeBook =[]
jokelimit =500

#### Twitter Code##
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)



os.chdir('C:\\Users\\Shaun\\Desktop\\python practrice') #change directory to your current working directory


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    print('retrieving and replying to tweets...', flush=True)
   
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    
    mentions = api.mentions_timeline( last_seen_id,tweet_mode='extended')
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#dark' in mention.full_text.lower():
            print('found User!', flush=True)
            print('responding back...', flush=True)
            if len(jokeBook) != 0:

                api.update_status('@' + mention.user.screen_name +'\n'+jokeBook[-1], mention.id)
                jokeBook.pop(-1)
            else:
                currentj =get_jokes()
                api.update_status('@' + mention.user.screen_name +'\n'+jokeBook[-1], mention.id)
                jokeBook.pop(-1)     
        else:
            api.update_status('@' + mention.user.screen_name +'\n'+'Add "#dark" at the end to get a dark Joke', mention.id)      
### The Jokes ###


def get_jokes():
    global jokelimit
    
    reddit = praw.Reddit(client_id="ADD HERE",
                     client_secret="ADD HERE",
                     password="ADD HERE",
                     user_agent="ADD HERE",
                     username="ADD HERE")

    print("\n\n\n-- Updating The joke Book .... -- ")
    

    subreddit = reddit.subreddit('darkjokes')  #change to your favorate subreddit

    jokes_content =subreddit.new(limit=jokelimit)
    for jokes in jokes_content:
        jokeBook.append(jokes.title+ "\n"+jokes.selftext)
    return jokeBook[-1]
    


    
while True:

    reply_to_tweets()
    time.sleep(15)
    
     




    


