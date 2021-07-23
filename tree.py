'''                                
Created By Cason Konzer July 2021
Version 1.0
'''
import pandas as pd
import matplotlib.pyplot as plt
import datetime
start = datetime.datetime.now()


# HASH MAP PSEUDOCODE

# (parentID, [NumberForParent, NumberForChild])
# largestNumberForParent = 0
# if not present in hashmap, add (p, [++largestNumberForParent, 1]
# get_val & set_val
# also add (id, [pDeweyID.1, 0])

# key = ID
# value = [deweyID, NumberOfChildren]
# look at a tuple.. you get parentID..

# parentID key is present; parentID key is not present; parentID is NA
# if NA -- deweyID for id = ++largestNumberForParent
# if present -- parentID, [pDID, NOfCh] -- (id, [pDID + "." + ++NOfCh, 0] -- parentID, [pDID, ++NOfCh]
# id not-present -- introduce unknowparentID -- U.100.1

df = pd.read_csv('flatearthdata.csv', low_memory=False)
df = df.head(10000)
tree = {}
dui = 0

for row in df.values:
    Post_Id = str(row[0])
    Parent_Id = str(row[1])
    if Parent_Id == 'nan':
        tree[Post_Id] = 'OG_' + str(Post_Id) + '__' + str(dui) + '.0'
        dui+=1
    else:
        try: 
            Parent_Id = Parent_Id[3:]
            dex = int(str(tree[Parent_Id])[-1])
            dex += 1
            tree[Parent_Id] = str(tree[Parent_Id])[:-1] + str(dex)
            print(str(Parent_Id) + '__' + tree[Parent_Id])
            
        except KeyError:
            #print('parent post non-existant')
            tree[Parent_Id] = 'NA_' + str(dui) + '.0'
            dui+=1

x =tree['3k6yl8']
print('\n \n \n', x)

end = datetime.datetime.now()
print('\nStarted: ', start)
print('Finished: ', end)
