'''                                
Created By Cason Konzer June 2021
Version 1.0
'''
import pandas as pd
import requests
import json
import datetime
import time 
import csv
start = datetime.datetime.now()

# make request and store as json
def get_pushshift_subm_data(after, before, sub, N):
    url = 'https://api.pushshift.io/reddit/search/submission/?after='+str(after)+'&before='+str(before)+'&subreddit='+str(sub)+'&size='+str(N)
    print(url)
    r = requests.get(url)
    print('http response is:',r.status_code)
    submissiondata = json.loads(r.text, strict=False)
    return submissiondata['data']


# take relevant data from json and write to dictionary 
def collect_subData(subm):
    subData = list() # list to store data points

    subreddit = subm['subreddit']
    subId = subm['subreddit_id']
    submId =subm['id']
    title = subm['title']
    try:
        body = subm['body'] # Returns the body of the post
    except KeyError:
        body = ''
    url = subm['url']
    http_link = subm['full_link']
    author = subm['author']
    score = subm['score']
    date_time = datetime.datetime.fromtimestamp(subm['created_utc'])
    created_utc = subm['created_utc']
    numComments = subm['num_comments']
    try:
        flair_text = subm['link_flair_text']
    except KeyError:
        flair_text = "NaN"

    subData.append((subreddit,subId,submId,title,body,url,http_link,author,score,date_time,created_utc,numComments,flair_text))
    subStats[submId] = subData

    # author_fullname = subm['author_fullname']
    # ratio = subm['upvote_ratio']
    # numAwards = subm['total_awards_recieved']
    # hint = subm['post_hint']

# take data from dictionary and write to csv
def update_subFile():
    upload_count = 0
    with open(name, 'w', newline = '', encoding = 'utf-8') as file:
        a = csv.writer(file, delimiter = ',')
        headers = ["Post ID", "Title", "Body", "Url", "Author", "Score", "Publish Date", "Total No. of Comments", "Permalink", "Flair"]
        a.writerow(headers)
        for sub in subStats:
            a.writerow(subStats[sub][0])
            upload_count += 1
        
        print(str(upload_count) + " submissions have been uploaded into a csv file")


# Create Global Dictionary to hold 'subData'
subStats = {}
# track # of submissions
subCount = 0
# Subreddit to query 
sub = 'flatearth'
# get queries after 1/1/15
after = '1420088400'
# get queries before 6/30/21
before = '1625108400'
# N queries to at a time
N = 100
# create file name
name = sub + 'submissiondata.csv'



# initialize submission request 
submissiondata = get_pushshift_subm_data(after, before, sub, N)

while len(submissiondata) > 0:
    for submission in submissiondata:
        collect_subData(submission)
        subCount += 1
    # Calls get_pushshift_subm_data() with the created data of the last submission
    update_subFile() # call to write submissiondata to csv file
    print(str(datetime.datetime.fromtimestamp(submissiondata[-1]['created_utc'])))
    after = submissiondata[-1]['created_utc']
    submissiondata = get_pushshift_subm_data(after, before, sub, N)
    # make program wait to keep from getting booted
    time.sleep(7)
end = datetime.datetime.now()
print('\nStarted: ', start)
print('Finished: ', end)
