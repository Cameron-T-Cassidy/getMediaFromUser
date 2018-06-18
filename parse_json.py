import json
from django.utils.encoding import smart_str, smart_unicode
import csv
import os
import os.path
import requests
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
i = 0
def printToFile (fileName, dirName, altTxt):
    loc = dirName
    completeName = os.path.join(loc, fileName)  
    file1 = open(completeName, "w")
    file1.write(altTxt)
    file1.close()
maxNumPics = 0
with open('a.csv', 'wb') as myfile:
    with open('json.txt', 'r') as in_file:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        topBar = ['username', 'date', 'tweetID' , 'is a retweet', 'text', 'media type']
        lines = []
        createFolder('./media')
        for line in in_file.readlines():
            tweet = json.loads(line)
            if ('extended_entities' in tweet):
                createFolder('./media/'+str(i))
                # username, date, is retweet, text, media type, media
                store = [' ', ' ', ' ', ' ', ' ', ' ']
                store[0] = (smart_str(tweet['user']['screen_name']))
                store[1] = smart_str(tweet['created_at'])
                store [2] = tweet['id_str']
                print store [2]
                if 'retweeted_status' in tweet: #if tweet is retweet
                    store[3] = 'retweet'
                    store[4] = smart_str(tweet['retweeted_status']['full_text'])
                    if 'extended_entities' in tweet['retweeted_status']:
                        store[5] = (tweet['retweeted_status']['extended_entities'])['media'][0]['type']
                        temp = 0
                        for m in tweet['retweeted_status']['extended_entities']['media']:
                            temp += 1
                            workingDir = './media/' + str(i) +'/' + str(temp-1) + '/'
                            store.append(m['media_url_https'])
                            store.append(smart_str(m['ext_alt_text']))
                            if temp > maxNumPics:
                                maxNumPics = temp
                            createFolder(workingDir)
                            if store[-1] != 'None':
                                printToFile('data.txt', workingDir, store[-1])
                            img_data = requests.get(store[-2]).content
                            with open(workingDir + str(temp) + '.jpg', 'wb') as handler:
                                handler.write(img_data)
                            
                else: #if tweet isn't a retweet
                    store[4] = smart_str(tweet['full_text'])
                    if 'extended_entities' in tweet:
                        store[5] = tweet['extended_entities']['media'][0]['type']
                        temp = 0
                        for m in tweet['extended_entities']['media']:
                            temp += 1
                            workingDir = './media/' + str(i) +'/' + str(temp-1) +'/'
                            if temp > maxNumPics:
                                maxNumPics = temp
                            store.append(smart_str(m['media_url_https']))
                            store.append(smart_str(m['ext_alt_text']))
                            createFolder(workingDir)
                            if(store[-1] != 'None'):
                                printToFile('data.txt', workingDir, store[-1])
                            img_data = requests.get(store[-2]).content
                            with open(workingDir + str(temp) + '.jpg', 'wb') as handler:
                                handler.write(img_data)
                i += 1
                lines.append(store)
        for x in range(0, maxNumPics):
            topBar.append('media')
            topBar.append('alt text')
        wr.writerow(topBar)
        for store in lines:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(store)
print i