'''                                
Created By Cason Konzer July 2021
Version 1.0
'''
import pandas as pd
import datetime
start = datetime.datetime.now()

# function nested in make_auth_list
def make_attrib_stats(Auth,csv):
    for auth in Auth:
        attribs = list()
        coms = 0
        subms = 0
        stats = Auth[auth]
        for stat in stats:
            if stat == 'comment':
                coms += 1
            elif stat == 'submission':
                subms += 1
        com = 'commments: ' + str(coms)
        sub = 'submissions: ' + str(subms)
        red = 'subreddit: ' + str(csv[:-8])
        attribs.append(red)
        attribs.append(sub)
        attribs.append(com)
        Auth[auth] = attribs
    return Auth

# create {} with author as key and storing subreddit, # comments, & # submissions contributed
def make_auth_list(csv):
    
    df = pd.read_csv(csv, low_memory=False)
    Auth = {}
    for row in df.values:
        auth = str(row[6])
        post = str(row[1])
        attrib = str()
        ls = list()
        if post == 'nan':
            attrib = 'comment'
        if post != 'nan':
            attrib = 'submission'
        if auth in Auth:
            ls = Auth[auth]
            ls.append(attrib)
            Auth[auth] = ls
        else:
            ls.append(attrib)
            Auth[auth] = ls
    #print(Auth)
    Auth = make_attrib_stats(Auth,csv)
    return Auth

# finds common authors between 2 communities 
def overlap_auths(Auth1, Auth2):
    OverlapSet = {}
    for auth in Auth1:
        if auth in Auth2:
            print('\n Author: {' + str(auth) + '} is in both [' + str(Auth1[auth][0]) + '] & [' + str(Auth2[auth][0]) + '] \n')
            OverlapSet[auth] = str(Auth1[auth]) + ' && ' + str(Auth2[auth])
    return OverlapSet

# return (submission count, comment count) for given author in a community 
def get_attrib_stats(Auth,auth):
    subs = Auth[auth][1]
    subs = subs[-1]
    coms = Auth[auth][2]
    coms = coms[-1]
    return (int(subs), int(coms))

# example
FE = make_auth_list('flatearthdata.csv')
AV = make_auth_list('antivaxdata.csv')
AVFE = overlap_auths(AV, FE)
print('----------------------------------------------------------')

print(AVFE, '\n ************************')


end = datetime.datetime.now()
print('\nStarted: ', start)
print('Finished: ', end)
