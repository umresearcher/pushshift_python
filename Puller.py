'''                                
Created By Cason Konzer July, 26 2021
Version 0.1
'''

import requests, json, time, csv, datetime, Dependencies as dp

s = 'submission'; c = 'comment'; stats = {}



def community():
    print('<<< What subreddit would you like to query? >>>\n<<< Enter name of subreddit [ex. Research] >>>  ::', end = '')
    sub = str(input())
    global name
    name = sub + '.data.csv'
    print('\n<<< You have choosen to que subreddit: "', sub, '" >>>\n\n', '---------------------' * 5, '\n')
    return sub, name




def past():
    print('<<< What is the earliest post you would like to see? *Enter in utc timestamp* >>>\n')
    print('<<< Enter 0 for earliest availiable post >>>  ::', end = '')

    after = str(input())
    if after == '0':
        after = '0000000000'

    print('\n<<< You have choosen to que posts after utc: "', after, '" >>>\n\n', '---------------------' * 5, '\n')
    return after




def future():
    print('<<< What is the latest post you would like to see? *Enter in utc timestamp* >>>\n')
    print('<<< Enter 0 for latest availiable post >>>  ::', end = '')

    before = str(input())
    if before == '0':
        before = '9999999999'
    
    print('\n<<< You have choosen to que posts before utc: "', before, '" >>>\n\n', '---------------------' * 5, '\n')
    return before




def que(a, b, sub, postT):
    global before; global after
    before = b; after = a
    
    if postT == 's':
        postT = s
    elif postT == 'c':
        postT = c

    url = 'https://api.pushshift.io/reddit/search/{}/?after={}&before={}&subreddit={}&size={}'.format(str(postT), str(after), str(before), str(sub), '123456789')
    time.sleep(1); print(url)

    try:
        time.sleep(1); r = requests.get(url); status = r.status_code; print('http response is:', status)
    except:
        status = ' NO HANDSHAKE '; print('http response is:', status)

    if status != 200:
        retry = 0

        while True: # retry 100 times; increase wait time with each bad response
            retry += 1
            print('\n<<< YOU JUST GOT STALLED! >>>\n\n<<< This is retry #:', retry, '>>>\n')
            dp.loader(retry)

            try:
                r = requests.get(url); status = r.status_code; print('retry http response is:', status)
            except:
                status = ' NO HANDSHAKE '; print('retry http response is:', status)
            
            if status == 200:
                break

    data = json.loads(r.text, strict=False)
    return data['data']




def write(to, fro, sc, cc):
    with open(to, 'w', newline = '', encoding = 'utf-8') as file:
        a = csv.writer(file, delimiter = ',')
        headers = ["Post Type", "Subreddit", "ID", "Link Id", "Parent Id", "Url", "Permalink", "UTC", "Retrived On", "Post Date", "Score", "# Comments", "Author", "Title", "Body"]
        a.writerow(headers)

        for stat in fro:
            a.writerow(fro[stat][0])

        print('{} submissions, and {} comments have been uploaded into {} \n'.format(str(sc), str(cc), to))
    time.sleep(1)



def call_data(data, postT): # take relevant data from json and write to dictionary 
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
    stats[Id] = Data




def subs(sub, data, name, sc, cc):
    try:
        print(sub)
    except:
        sub, name = community()

    while len(data) > 0:
        for subm in data:
            call_data(subm, s); sc += 1
        if len(data) > 0: 
            print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
            after = data[-1]['created_utc']
            data = que(after, before, sub, s)
            time.sleep(5)
        write(name, stats, sc, cc); print(('*********************' * 5) + '\n')
    print(('XXXXXXXXXXXXXXXXXXXXX' * 5) + '\n\n<<< submission pull completed; now gathering comments >>>\n\n' + ('XXXXXXXXXXXXXXXXXXXXX' * 5) + '\n')




def coms(sub, data, name, sc, cc):
    try:
        print(sub)
    except:
        sub, name = community()

    while len(data) > 0:
        for comm in data:
            call_data(comm, c); cc += 1
        if len(data) > 0: # Calls get_pushshift_comm_data() with the created data of the last comment
            print(str(datetime.datetime.fromtimestamp(data[-1]['created_utc'])))
            after = data[-1]['created_utc']
            data = que(after, before, sub, c)
            time.sleep(5)
        write(name, stats, sc, cc); print(('*********************' * 5) + '\n')
    print(('XXXXXXXXXXXXXXXXXXXXX' * 5) + '\n\n<<< comment pull completed >>>\n' + ('XXXXXXXXXXXXXXXXXXXXX' * 5) + '\n')
