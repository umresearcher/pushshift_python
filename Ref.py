'''                                
Created By Cason Konzer July 2021
Version 1.0
'''
import pandas as pd
import csv
import datetime
start = datetime.datetime.now()

def compile_subs():
    df = pd.read_csv('ultimatelist.csv', low_memory=False)
    global Subs
    Subs = {}
    num = 0
    for row in df.values:
        sub = str(row[1])
        sub = sub.lower()
        Subs[sub] = True
        num += 1
        print(num, num, num, num, num)
compile_subs()

def build_post_text(csv):
    df = pd.read_csv(csv, low_memory=False)
    text = {}
    for row in df.values:
        PostId = str(row[0])
        auth = str(row[6])
        title = str(row[-2])
        body = str(row[-1])
        infos = list()
        infos.append(auth)
        infos.append(title)
        infos.append(body)
        text[PostId] = infos
    return text

def grep_text(Text):
    Refs = {}
    num = 0
    for text in Text:
        print('$$$ ' * 5)
        PostId = Text[text][0]
        Post = Text[text]
        for post in Post:
            if 'r/' in post:
                post = str(post)
                split = post.split('r/')
                split = split[1]
                split = split.split('/')
                for item in split:
                    item.lower()
                    if item in Subs:
                        print('\n' * 5)
                        num += 1
                        Refs[PostId] = item
    return Refs

def Make_Ref_File(name,Refs):
    count = 0
    name = name[:-8] + 'ref.csv'
    with open(name, 'w', newline = '', encoding = 'utf-8') as file:
        a = csv.writer(file)
        headers = ["Community-Referenced"]
        a.writerow(headers)
        for ref in Refs:

            a.writerow([Refs[ref]])
            count += 1
    print(count, 'refrenced uploaded into:', name)


#example
name = 'flatearthdata.csv'
B = build_post_text('flatearthdata.csv')
b = grep_text(B)
Make_Ref_File(name, b)

end = datetime.datetime.now()
print('\nStarted: ', start)
print('Finished: ', end)
