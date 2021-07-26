'''                                
Created By Cason Konzer June 2021
Version 0.6
'''

import requests, json, time, csv, datetime, dependencies #,pandas as pd # import modules

start = dependencies.now() # get program start time
dependencies.um() # print UM art
stallCount = 0 # initialize stall count


def get_pushshift_subm_data(subafter, before, sub, N, stallCount): # make submission request and store as json
    url = 'https://api.pushshift.io/reddit/search/submission/?after={}&before={}&subreddit={}&size={}'.format(str(subafter), str(before), str(sub), str(N))
    time.sleep(1); print(url)
    try:
        time.sleep(1); rs = requests.get(url); subm_status = rs.status_code; print('http response is:', subm_status)
    except:
        subm_status = ' NO HANDSHAKE '; print('http response is:', subm_status)
    retry = 0
    if subm_status != 200:
        while retry <= 100: # retry 5 times; increase wait time with each bad response
            stallCount += 1; retry += 1
            print('\n<<< YOU JUST GOT STALLED! >>>\n')
            print('<<< This is retry #:', retry, '>>>\n')
            dependencies.loader(retry)
            try:
                rs = requests.get(url); subm_status = rs.status_code; print('retry http response is:', subm_status)
            except:
                subm_status = ' NO HANDSHAKE '; print('retry http response is:', subm_status)
            
            if subm_status == 200:
                break
    time.sleep(1); submissiondata = json.loads(rs.text, strict=False)
    return submissiondata['data']


def get_pushshift_comm_data(comafter, before, sub, N, stallCount): # make comment request and store as json
    url = 'https://api.pushshift.io/reddit/search/comment/?after={}&before={}&subreddit={}&size={}'.format(str(comafter), str(before), str(sub), str(N))
    time.sleep(1); print(url)
    try:
        time.sleep(1); rc = requests.get(url); comm_status = rc.status_code; print('http response is:', comm_status)
    except:
        comm_status = ' NO HANDSHAKE '; print('http response is:', comm_status)
    retry = 0
    if comm_status != 200:
        while retry <= 100: # retry 5 times; increase wait time with each bad response
            stallCount += 1; retry += 1
            print('\n<<< YOU JUST GOT STALLED! >>>\n')
            print('<<< This is retry #:', retry, '>>>\n')
            dependencies.loader(retry)
            try:
                rc = requests.get(url); comm_status = rc.status_code; print('retry http response is:', comm_status)
            except:
                comm_status = ' NO HANDSHAKE '; print('retry http response is:', comm_status)
            if comm_status == 200:
                break
    time.sleep(1); commentdata = json.loads(rc.text, strict=False)
    return commentdata['data']


def collect_Data(data, postT): # take relevant data from json and write to dictionary 
    Data = list() # list to store data points
    PostType = postT
    try:
        sub = data['subreddit'] # 
    except KeyError:
        sub = 'NA'
    try:
        Id = data['id'] # Returns the id of the comment or submission
    except KeyError:
        Id = 'NA'
    try:
        parId = data['parent_id'] # Returns the id of the parent post
    except KeyError:
        parId = 'NA'
    try:
        linkId = data['link_id'] # 
    except KeyError:
        linkId = 'NA'
    try:
        url = data['url'] # Returns the url of the post
    except KeyError:
        url = 'NA'
    try:
        perma = data['permalink'] #
    except KeyError:
        perma = 'NA'
    try:
        timestamp = data['created_utc']; date_time = datetime.datetime.fromtimestamp(timestamp); date = date_time.strftime("%m/%d/%Y")
    except KeyError:
        date = 'NA'
    try:
        created_utc = data['created_utc'] # Returns the time of the post in utc
    except KeyError:
        created_utc = 'NA'    
    try:
        retrival = data['retrieved_on'] # 
    except KeyError:
        retrival = 'NA' 
    try:
        score = data['score'] # Returns the sum score of the post
    except KeyError:
        score = 'NA'
    try:
        numComments = data['num_comments'] # Returns the number of comments on the post
    except KeyError:
        numComments = 'NA'
    try:
        title = data['title']; title = r'{}'.format(title) # Returns the title of the post
    except KeyError:
        title = 'NA'
    try:
        body = data['body']; body = r'{}'.format(body) # Returns the body of the post
    except KeyError:
        body = 'NA'
    try:
        author = data['author']; author = r'{}'.format(author) # Returns the author of the post
    except KeyError:
        author = 'NA'
    Data.append((PostType, sub, Id, linkId, parId, url, perma, created_utc, retrival, date, score, numComments, author, title, body)) 
    Stats[Id] = Data
# Other possible pushshift pulls I have not implemented
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
    #  ------------------------------------
    # try:
    #     flair_text = data['link_flair_text']
    # except KeyError:
    #     flair_text = "NA"


def update_File(): # take data from dictionary and write to csv
    upload_count = 0
    with open(name, 'w', newline = '', encoding = 'utf-8') as file:
        a = csv.writer(file, delimiter = ',')
        #         <PostType> : <sub> : <Id> : <linkId> : <parId> : <url> : <perma> : <created_utc> : <retrival> : <date> : <score> : <numComments> : <author> : <title> : <body>
        headers = ["Post Type", "Subreddit", "ID", "Link Id", "Parent Id", "Url", "Permalink", "UTC", "Retrived On", "Post Date", "Score", "# Comments", "Author", "Title", "Body"]
        a.writerow(headers)
        for stat in Stats:
            a.writerow(Stats[stat][0]); upload_count += 1
        print('{} submissions, and {} comments have been uploaded into {} \n'.format(str(subCount), str(comCount), name))
    time.sleep(1)


print(('#####################' * 5) + '\n')

Stats = {} # Create Global Dictionary to hold 'subData' & 'comData'
subCount = 0; comCount = 0 # track # of submissions & comments

print('<<< What subreddit would you like to query? >>>\n<<< Enter name of subreddit [ex. Research] >>>  ::', end = '')
sub = str(input()) # Subreddit to query 
print('\n<<< You have choosen to que subreddit: "', sub, '" >>>\n\n', '---------------------' * 5, '\n')

print('<<< What is the earliest post you would like to see? *Enter in utc timestamp* >>>\n')
print('<<< Enter 0 for earliest availiable post >>>  ::', end = '')
after = str(input()) # get queries after beginning of time
if after == '0':
    after = '0000000000'
subafter = after; comafter = after
print('\n<<< You have choosen to que posts after utc: "', after, '" >>>\n\n', '---------------------' * 5, '\n')

print('<<< What is the latest post you would like to see? *Enter in utc timestamp* >>>\n')
print('<<< Enter 0 for latest availiable post >>>  ::', end = '')
before = str(input()) # get queries before end of time
if before == '0':
    before = '9999999999'
print('\n<<< You have choosen to que posts before utc: "', before, '" >>>\n\n', '---------------------' * 5, '\n')

N = 123456789 # N queries to at a time
name = sub + '.data.csv' # create file name
submissiondata = get_pushshift_subm_data(subafter, before, sub, N, stallCount); commentdata = get_pushshift_comm_data(comafter, before, sub, N, stallCount) # initialize submission & commentrequest 
sublen = len(submissiondata); comlen = len(commentdata) # initialize lengths 

print('\n<<< Variables Initialized >>>\n\n' + ('#####################' * 5) + '\n\n')
def getsubs():
    while sublen > 0:
        for submission in submissiondata:
            collect_Data(submission, 'submission'); subCount = subCount + 1
        if sublen > 0: # Calls get_pushshift_sub_data() with the created data of the last submission
            print(str(datetime.datetime.fromtimestamp(submissiondata[-1]['created_utc'])))
            subafter = submissiondata[-1]['created_utc']
            submissiondata = get_pushshift_subm_data(subafter, before, sub, N, stallCount)
            sublen = len(submissiondata); time.sleep(5 * (stallCount + 1))
        update_File() ; print(('*********************' * 5) + '\n')
    print(('XXXXXXXXXXXXXXXXXXXXX' * 5) + '\n\n<<< submission pull completed; now gathering comments >>>\n\n' + ('XXXXXXXXXXXXXXXXXXXXX' * 5) + '\n')


def getcoms():
    while comlen > 0:
        for comment in commentdata:
            collect_Data(comment, 'comment'); comCount = comCount + 1
        if comlen > 0: # Calls get_pushshift_comm_data() with the created data of the last comment
            print(str(datetime.datetime.fromtimestamp(commentdata[-1]['created_utc'])))
            comafter = commentdata[-1]['created_utc']
            commentdata = get_pushshift_comm_data(comafter, before, sub, N, stallCount)
            comlen = len(commentdata); time.sleep(5 * (stallCount + 1))
        update_File(); print(('*********************' * 5) + '\n')
    print(('XXXXXXXXXXXXXXXXXXXXX' * 5) + '\n\n<<< comment pull completed >>>\n' + ('XXXXXXXXXXXXXXXXXXXXX' * 5) + '\n')


getsubs()
getcoms()

print('<<< your program has finished and your data is available in the run directory, stored in /' + name + ' >>>')

end = dependencies.now(); print('\n\n\nStarted: ' + str(start) + '\n\nFinished: ' + str(end) + '\n\n') # print out start/end time
if __name__ == '__main__': 
    exit()
