'''                                
Created By Cason Konzer June 2021
Version 1.0
'''
import pandas as pd
import requests
import json
import time 
import csv
import logo
import datetime
start = datetime.datetime.now()

logo.um()

# initialize stall count
global stallCount
stallCount = 0

# make request and store as json
def get_pushshift_subm_data(subafter, before, sub, N, stallCount):
    url = 'https://api.pushshift.io/reddit/search/submission/?after={}&before={}&subreddit={}&size={}'.format(str(subafter), str(before), str(sub), str(N))
    print(url)
    rs = requests.get(url)
    subm_status = rs.status_code
    print('http response is:',subm_status)
    if subm_status == 200:
        submissiondata = json.loads(rs.text, strict=False)
        return submissiondata['data']
    else: # if status bad; wait and retry
        stallCount += 1
        print()
        print('<<< YOU JUST GOT STALLED! STALL COUNT IS:', stallCount, '>>>')
        print()
        time.sleep(30*stallCount)
        rs = requests.get(url)
        subm_status = rs.status_code
        print('new http response is:',subm_status)
        submissiondata = json.loads(rs.text, strict=False)
        return submissiondata['data']
        
def get_pushshift_comm_data(comafter, before, sub, N, stallCount):
    url = 'https://api.pushshift.io/reddit/search/comment/?after={}&before={}&subreddit={}&size={}'.format(str(comafter), str(before), str(sub), str(N))
    print(url)
    rc = requests.get(url)
    comm_status = rc.status_code
    print('http response is:',comm_status)
    if comm_status == 200:
        commentdata = json.loads(rc.text, strict=False)
        return commentdata['data']
    else: # if status bad; wait and retry
        stallCount += 1
        print()
        print('<<< YOU JUST GOT STALLED! STALL COUNT IS:', stallCount, '>>>')
        print()
        time.sleep(30*stallCount)
        rc = requests.get(url)
        comm_status = rc.status_code
        print('new http response is:',comm_status)
        commentdata = json.loads(rc.text, strict=False)
        return commentdata['data']


# take relevant data from json and write to dictionary 
def collect_Data(data):
    Data = list() # list to store data points
    try:
        Id = data['id'] # Returns the id of the comment or submission
    except KeyError:
        Id = 'NA'
    try:
        parId = data['parent_id'] # Returns the id of the parent post
    except KeyError:
        parId = 'NA'
    try:
        url = data['url'] # Returns the url of the post
    except KeyError:
        url = 'NA'
    try:
        timestamp = data['created_utc'] 
        date_time = datetime.datetime.fromtimestamp(timestamp)
        date = date_time.strftime("%m/%d/%Y")
    except KeyError:
        date = '0'    
    try:
        score = data['score'] # Returns the sum score of the post
    except KeyError:
        score = 'NA'
    try:
        numComments = data['num_comments'] # Returns the number of comments on the post
    except KeyError:
        numComments = 'NA'
    try:
        title = data['title'] # Returns the title of the post
    except KeyError:
        title = 'NA'
    try:
        body = data['body'] # Returns the body of the post
    except KeyError:
        body = 'NA'
    try:
        author = data['author'] # Returns the author of the post
    except KeyError:
        author = 'NA'
    Data.append((Id,parId,url,date,score,numComments,author,title,body))
    Stats[Id] = Data

    # try:
    #     created_utc = data['created_utc'] # Returns the time of the post in utc
    # except KeyError:
    #     created_utc = 'NA'
    # try:
    #     http_link = data['full_link']
    # except KeyError:
    #     http_link = "NA"
    #  ------------------------------------
    # try:
    #     subId = data['subreddit_id']
    # except KeyError:
    #     subId = "NA"
    #  ------------------------------------
    # try:
    #     date_time = datetime.datetime.fromtimestamp(data['created_utc'])
    # except KeyError:
    #     date_time = "NA"
    #  ------------------------------------
    # try:
    #     subreddit = data['subreddit']
    # except KeyError:
    #     subreddit = "NA"
    #  ------------------------------------
    # try:
    #     author_fullname = data['author_fullname']
    # except KeyError:
    #     author_fullname = "NA"
    #  ------------------------------------
    # try:
    #     ratio = data['upvote_ratio']
    # except KeyError:
    #     ratio = "NA"
    #  ------------------------------------
    # try:
    #     numAwards = data['total_awards_recieved']
    # except KeyError:
    #     numAwards = "NA"
    #  ------------------------------------
    # try:
    #     hint = data['post_hint']
    # except KeyError:
    #     hint = "NA"
    # ------------------------------------
    # try:
    #     flair_text = data['link_flair_text']
    # except KeyError:
    #     flair_text = "NA"


# take data from dictionary and write to csv
def update_File():
    upload_count = 0
    with open(name, 'w', newline = '', encoding = 'utf-8') as file:
        a = csv.writer(file, delimiter = ',')
    #              <Id>   :   <parId>   :   <url>   :   <date>   :   <score>   :   <numComments>   :   <author>   :   <title>   :   <body>
        headers = ["ID",    "Parent Id",    "Url",   "Post Date",    "Score",      "# Comments",       "Author",      "Title",      "Body"]
        a.writerow(headers)
        for stat in Stats:
            a.writerow(Stats[stat][0])
            upload_count += 1
        
        print('{} submissions, and {} comments have been uploaded into {} \n'.format(str(subCount), str(comCount), name))

# Create Global Dictionary to hold 'subData' & 'comData'
Stats = {}
# track # of submissions & comments
subCount = 0
comCount = 0
# Subreddit to query 
print('<<< What subreddit would you like to query? >>>')
sub = str(input())
print('<<< You have choosen to que', sub, '>>>', '\n')
# get queries after beginning of time
print('<<< What is the earliest post you would like to see? *Enter in utc timestamp* >>>')
print('<<< Enter 0 for earliest availiable comment >>>')
after = str(input())
if after == '0':
    after = '0000000000'
subafter = after
comafter = after
print('<<< You have choosen to que comments after', after, '>>>', '\n')
# get queries before 6/30/21
print('<<< What is the latest post you would like to see? *Enter in utc timestamp* >>>')
print('<<< Enter 0 for latest availiable comment >>>')
before = str(input())
if before == '0':
    before = '9999999999'
print('<<< You have choosen to que comments before', before, '>>>', '\n')
# N queries to at a time
N = 100
# create file name
name = sub + 'data.csv'
# initialize submission & commentrequest 
submissiondata = get_pushshift_subm_data(subafter, before, sub, N, stallCount)
commentdata = get_pushshift_comm_data(comafter, before, sub, N, stallCount)
# initialize lengths 
sublen = len(submissiondata)
comlen = len(commentdata)
print('<<< Variables Initialized >>>', '\n')

while ((sublen > 0) or (comlen > 0)):
    for submission in submissiondata:
        collect_Data(submission)
        subCount += 1
    for comment in commentdata:
        collect_Data(comment)
        comCount += 1
    if sublen > 0: # Calls get_pushshift_sub_data() with the created data of the last submission
        print(str(datetime.datetime.fromtimestamp(submissiondata[-1]['created_utc'])))
        subafter = submissiondata[-1]['created_utc']
        submissiondata = get_pushshift_subm_data(subafter, before, sub, N, stallCount)
        sublen = len(submissiondata)
        time.sleep(1 + stallCount)
    if comlen > 0:# Calls get_pushshift_comm_data() with the created data of the last comment
        print(str(datetime.datetime.fromtimestamp(commentdata[-1]['created_utc'])))
        comafter = commentdata[-1]['created_utc']
        commentdata = get_pushshift_comm_data(comafter, before, sub, N, stallCount)
        comlen = len(commentdata)
        time.sleep(1 + stallCount)
    update_File() # call to write submission & comment data to csv file
    # make program wait to keep from getting booted
    time.sleep(1 + stallCount)

print('<<< your program has finished and your data is available in the run directory, stored in /' + name + ' >>>')

end = datetime.datetime.now()
print('\nStarted: ', start)
print('Finished: ', end)

if __name__ == '__main__':
    exit()
