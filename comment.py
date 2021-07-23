'''                                
Created By Cason Konzer June 2021
Version 1.0
'''
import pandas as pd
import requests
import json
import time 
import csv
import datetime
start = datetime.datetime.now()

# make request and store as json
def get_pushshift_comm_data(after, before, sub, N):
    url = 'https://api.pushshift.io/reddit/search/comment/?after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)+'&size='+str(N)
    print(url)
    r = requests.get(url)
    print('http response is:',r.status_code)
    commentdata = json.loads(r.text, strict=False)
    return commentdata['data']


# take relevant data from json and write to dictionary 
def collect_comData(comm):
    comData = list() # list to store data points
    
    subreddit = comm['subreddit']
    subId = comm['subreddit_id']
    comId = comm['id']
    parId = comm['parent_id']

    try:
        body = comm['body'] # Returns the body of the post
    except KeyError:
        body = ''
    author = comm['author']
    score = comm['score']
    date_time = datetime.datetime.fromtimestamp(comm['created_utc'])
    created_utc = comm['created_utc']
    try:
        flair = comm['author_flair_text']
    except KeyError:
        flair = "NaN"

    comData.append((subreddit,subId,comId,parId,body,author,score,date_time,created_utc,flair))
    comStats[comId] = comData

    # author_fullname = comm['author_fullname']

# take data from dictionary and write to csv
def update_comFile():
    upload_count = 0
    with open(name, 'w', newline = '', encoding = 'utf-8') as file:
        a = csv.writer(file, delimiter = ',')
        headers = ["Post ID", "Title", "Body", "Url", "Author", "Score", "Publish Date", "Total No. of Comments", "Permalink", "Flair"]
        a.writerow(headers)
        for comm in comStats:
            a.writerow(comStats[comm][0])
            upload_count += 1
        
        print(str(upload_count) + " comments have been uploaded into a csv file")


# Create Global Dictionary to hold 'comData'
comStats = {}
# track # of comments
comCount = 0
# Subreddit to query 
sub = 'flatearth'
# get queries after 1/1/15
after = '1420088400'
# get queries before 6/30/21
before = '1625108400'
# N queries to get at a time
N = 500
# create file name
name = sub + 'commentdata.csv'



# initialize comment request 
commentdata = get_pushshift_comm_data(after, before, sub, N)

while len(commentdata) > 0:
    for comment in commentdata:
        collect_comData(comment)
        comCount += 1
    # Calls get_pushshift_comm_data() with the created data of the last comment
    update_comFile() # call to write commentdata to csv file
    print(str(datetime.datetime.fromtimestamp(commentdata[-1]['created_utc'])))
    after = commentdata[-1]['created_utc']
    commentdata = get_pushshift_comm_data(after, before, sub, N)
    # make program wait to keep from getting booted
    time.sleep(7)
end = datetime.datetime.now()
print('\nStarted: ', start)
print('Finished: ', end)
