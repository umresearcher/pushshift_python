'''                                
Created By Cason Konzer July, 29 2021
Version 0.3
'''

# import modules
import requests, json, csv, Dependencies as dp
s = 'submission'; c = 'comment'




# prompt user for subreddit to query
def community():
    global name; global sub
    print('<<< What subreddit would you like to query? >>>\n\n<<< Enter name of subreddit [ex. Research] >>> :: ', end = '')
    sub = str(input())
    name = sub + '.data.csv'
    print('\n<<< You have choosen to que subreddit: ', sub, ' >>>\n\n' + ('-----------------------' * 5), '\n')
    return sub, name




# prompt user for earliest post
def past():
    while True:
        print('<<< What is the earliest post you would like to see? *Enter in utc timestamp* >>>\n\n<<< Enter 0 for earliest availiable post >>> :: ', end = '')
        after = str(input())

        if after == '0':
            after = '0000000000'
            break
        elif len(after) == 10:
            break
        else:
            print('>>> INPUT ERROR <<<')    
            continue

    print('\n<<< You have choosen to que posts after utc: ', after, ' >>>\n\n' + ('-----------------------' * 5), '\n')
    return after




# prompt user for latest post
def future():
    while True:
        print('<<< What is the latest post you would like to see? *Enter in utc timestamp* >>>\n\n<<< Enter 0 for latest availiable post >>> :: ', end = '')
        before = str(input())

        if before == '0':
            before = '9999999999'
            break
        elif len(before) == 10:
            break
        else:
            print('>>> INPUT ERROR <<<')    
            continue
    
    print('\n<<< You have choosen to que posts before utc: ', before, ' >>>\n\n' + ('-----------------------' * 5), '\n')
    return before




# hit pushshift api; grab json and store as 'data'
def que(a, b, sub, postT):
    global before; global after
    before = b; after = a
    
    if postT == 's':
        postT = s
    elif postT == 'c':
        postT = c

    url = 'https://api.pushshift.io/reddit/search/{}/?after={}&before={}&subreddit={}&size={}'.format(str(postT), str(after), str(before), str(sub), '123456789')
    dp.zzz(1); print('\n>> url:', url, '\n')

    try:
        r = requests.get(url); status = r.status_code; print('>> http response is:', status)
    except:
        status = ' NO HANDSHAKE '; print('>> http response is:', status)

    if status != 200:
        retry = 0

        while True: # retry 100 times; increase wait time with each bad response
            retry += 1
            print('\n<<< YOU JUST GOT STALLED! >>>\n\n<<< This is retry #:', retry, '>>>\n')
            dp.loader(retry)

            try:
                r = requests.get(url); status = r.status_code; print('>> retry http response is:', status)
            except:
                status = ' NO HANDSHAKE '; print('>> retry http response is:', status)
            
            if status == 200:
                break

    data = json.loads(r.text, strict=False)
    return data['data']




# write stats from pushshift to csv
def write(to, fro, sc, cc):
    with open(to, 'w', newline = '', encoding = 'utf-8') as file:
        w = csv.writer(file, delimiter = ',')
        headers = ["Post Type", "Subreddit", "ID", "Link Id", "Parent Id", "Url", "Permalink", "UTC", "Retrived On", "Post Date", "Score", "# Comments", "Author", "Title", "Body"]
        w.writerow(headers)

        for stat in fro:
            w.writerow(fro[stat][0])

        print('\n>> {} submissions, and {} comments have been uploaded into {} \n'.format(f'{sc:,}', f'{cc:,}', to))
    dp.zzz(1)




# call 'data' json object and write selctive attributes to stats dict
def call_data(data, postT): 
    Data = list() # list to store data points
    PostType = postT

    try:
        sub = data['subreddit'] # 
    except KeyError:
        sub = 'NA'
    try:
        Id = data['id'] #
    except KeyError:
        Id = 'NA'
    try:
        parId = data['parent_id'] #
    except KeyError:
        parId = 'NA'
    try:
        linkId = data['link_id'] # 
    except KeyError:
        linkId = 'NA'
    try:
        url = data['url'] # 
    except KeyError:
        url = 'NA'
    try:
        perma = data['permalink'] #
    except KeyError:
        perma = 'NA'
    try:
        timestamp = data['created_utc']; t = dp.fts(timestamp); date = dp.nicetime(t) #
    except KeyError:
        date = 'NA'
    try:
        created_utc = data['created_utc'] # 
    except KeyError:
        created_utc = 'NA'    
    try:
        retrival = data['retrieved_on'] # 
    except KeyError:
        retrival = 'NA' 
    try:
        score = data['score'] # 
    except KeyError:
        score = 'NA'
    try:
        numComments = data['num_comments'] # 
    except KeyError:
        numComments = 'NA'
    try:
        title = data['title']; title = r'{}'.format(title) # 
    except KeyError:
        title = 'NA'
    try:
        body = data['body']; body = r'{}'.format(body) # 
    except KeyError:
        body = 'NA'
    try:
        author = data['author']; author = r'{}'.format(author) # 
    except KeyError:
        author = 'NA'

    Data.append((PostType, sub, Id, linkId, parId, url, perma, created_utc, retrival, date, score, numComments, author, title, body)) 
    stats[Id] = Data




# loop to collect all submissions in given timeframe
def subs(sub, data, name, sc, cc):
    try:
        sub
    except:
        sub, name = community()

    while len(data) > 0:
        for subm in data:
            call_data(subm, s); sc += 1

        if len(data) > 0: 
            print('\n>> current time:', dp.now())
            print('\n>> posting time:', str(dp.fts(data[-1]['created_utc'])))
            after = data[-1]['created_utc']
            data = que(after, before, sub, s)
            dp.zzz(2.5)

        write(name, stats, sc, cc); dp.zzz(2.5); print(('***********************' * 5) + '\n')
    print(('XXXXXXXXXXXXXXXXXXXXXXX' * 5) + '\n\n<<< submission pull completed >>>\n\n' + ('XXXXXXXXXXXXXXXXXXXXXXX' * 5) + '\n')

    return sc, cc




# loop to collect all comments in given timeframe
def coms(sub, data, name, sc, cc):
    try:
        print(sub)
    except:
        sub, name = community()

    while len(data) > 0:
        for comm in data:
            call_data(comm, c); cc += 1

        if len(data) > 0:
            print('\n>> current time:', dp.now())
            print('\n>> posting time:', str(dp.fts(data[-1]['created_utc'])))
            after = data[-1]['created_utc']
            data = que(after, before, sub, c)
            dp.zzz(2.5)

        write(name, stats, sc, cc); dp.zzz(2.5); print(('***********************' * 5) + '\n')
    print(('XXXXXXXXXXXXXXXXXXXXXXX' * 5) + '\n\n<<< comment pull completed >>>\n\n' + ('XXXXXXXXXXXXXXXXXXXXXXX' * 5) + '\n')

    return sc, cc




# call loops for desired post type
def pull(subm, comm, sub, name, after, before, sc, cc):

    if subm == True:
        subdata = que(after, before, sub, 's')
        sc, cc = subs(sub, subdata, name, sc, cc)

    if comm == True:
        comdata = que(after, before, sub, 'c')
        sc, cc = coms(sub, comdata, name, sc, cc)

    print('<<< your program has finished and your data is available in the run directory, stored in /' + name + ' >>>')




# initialize variables and start data grab
def start(subm, comm):
    sc = 0; cc = 0
    global stats; stats = {}
    sub, name = community()
    after = past()
    before = future()

    print('<<< Would you like to abort? (0 = no; else = yes) >>> :: ', end='')
    abort = input()

    if abort == '0':
        print('\n' + ('-----------------------' * 5))
        print('\n<<< Variables Initialized >>>\n\n' + ('#######################' * 5))
        pull(subm, comm, sub, name, after, before, sc, cc)
    else:
        print('\n<<< Your pull has been cancled >>>\n')
    




# call start; make multiple pulls? 
def starter():
    print(('#######################' * 5) + '\n')
    dp.um()
    print(('#######################' * 5) + '\n')
    again = '0'

    while again == '0':
        t = dp.now()

        while True:
            print('\n<<< Would you like to retrive reddit submissions? (0 = yes; else = no) >>> :: ', end = '')
            subm = input()

            if subm == '0':
                subm = True
                break
            else:
                print('>>> INPUT ERROR <<<')
                continue
        print('\n', '-----------------------' * 5, '\n')
        
        while True:
            print('\n<<< Would you like to retrive reddit comment? (0 = yes; else = no) >>> :: ', end = '')
            comm = input()

            if comm == '0':
                comm = True
                break
            else: 
                print('>>> INPUT ERROR <<<')
                continue
        print('\n', '-----------------------' * 5, '\n')
        
        start(subm, comm)

        print("\n<<< This pull's run time >>>")
        dp.timer(t)
        print('\n<<< Would you like to make a new query? (0 = yes; else = no) >>> :: ', end = '')
        again = input()

    print('\n<<< Thank you, Goodbye >>>')




if __name__ == '__main__': 
    start_time = dp.now()
    starter()
    print('\n\n\n<<< Total Run Time >>>')
    dp.timer(start)
    exit()
