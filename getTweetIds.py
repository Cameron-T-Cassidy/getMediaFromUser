#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = "VUBCnPJQUyCTEMPwwzyukbHqO"
consumer_secret = "tX3l5NZYbVwManCv1ZzonzIxg1UbG5pnMAnhnoNrZkrkmHhOA2"
access_key = "970196590945185792-35kOr7KDXhinMqeWyFBn74So8HJ8ao9"
access_secret = "67oFhv6UXb6itKWQAi7cmuZwniyXEXxZSvfzq1SCZ4wvS"


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str] for tweet in alltweets]
	
	#write the csv	
	with open('tweetIds.txt', 'a') as f:
		writer = csv.writer(f)
		writer.writerows(outtweets)
	pass


if __name__ == '__main__':
    
	#pass in the username of the account you want to download
    name = 'jeffbigham'
    get_all_tweets(name)