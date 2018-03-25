#!/usr/local/bin/python

import sys
import csv
import json
import shutil
import os
from os import path,rename, access, R_OK
from  tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import time
import datetime 

#import twitter keys and config from the config file in the current working directory

consumer_key ='v7MHYadkuukmkpOVsLFCNx4NB'
consumer_secret ='5e0WROZ9gU1fxl1V5I5sEdyzzq2TW2G5bMsj050BzVWKnSU33j'
access_token ='720858982747799552-yJ5KABRjzmfWPWK74iCBSd4lLJEZgsg'
access_token_secret ='eRGf391y2j3L1H0RphKl5VufZ0uXO0PzkD904hEd4b4BY'

#file manipilation
dt = str(datetime.datetime.now())
filename='bitcointweets.csv'
backupname='bitcointweets_'+dt+'.csv'
destination=os.getcwd()

#backup existing file 

if path.isfile(filename) and access(filename,R_OK):
	shutil.move(filename, backupname)

class TweetStreamListener(StreamListener):

	def on_data(self,data):
		try:

			tweets=json.loads(data) #the twitter data is in json format so we use the json library loads function to write to the variable tweets.
			text=tweets['text'].encode('utf8') #get's the text field of the json 
			screen_name=tweets['user']['screen_name'] #screen_name is the username which is an entity that exists inside 'user'
			followers_count=tweets['user']['followers_count'] #followers count
			device_used=tweets['source'] #prints the device used to make the tweet
			favourite_count=tweets['favorite_count'] #number of times a tweet was favourited
			created_at=tweets['created_at'] #date and time stamp when tweet was made

			feelings=[]
			tweetstring=TextBlob(tweets['text']) #parse with TextBlob for nlp
			if tweetstring.sentiment.polarity <0:
				feelings.append("negative")
			elif tweetstring.sentiment.polarity == 0:
				feelings.append("neutral")
			else:
				feelings.append("positive")
				
			hashtaglist=[] #empty list to store hashtags
			hashtags=tweets['entities']['hashtags'] #the json field that contains the hashtag

			for hashtag in hashtags: #we iterate through a loop that appends the hashtag list
				hashtags=hashtag['text']
				hashtaglist.append(hashtags)

			#Begin writing the csv file here
			print created_at,text,screen_name,followers_count,favourite_count,hashtaglist,device_used,feelings
			tweet_list=[[created_at,text,screen_name,followers_count,favourite_count,hashtaglist,device_used,feelings]]
			with open(filename, 'a') as csvtweets: #writes the results of the json into a csv which we can process later.
				writer=csv.writer(csvtweets)
				writer.writerows(tweet_list)
		except:
			time.sleep(2) # take a break
			pass
			
		

	def on_error(self,data):
		return True
	
	def on_timeout(self):
		return True


if __name__ == '__main__':

	listener = TweetStreamListener()
	auth= OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token,access_token_secret)
	stream =  Stream(auth, listener, wait_on_rate_limit=True,wait_on_rate_limit_notify=True,retry_count=3,retry_delay=5,retry_errors=set([401, 404, 500, 503]),monitor_rate_limit=True)
	stream.filter(languages=['en'],track=['bitcoin'],stall_warnings=False)

