import pandas as pd


def make_auth_list(csv):
    
    df = pd.read_csv(csv, low_memory=False)
    df = df.head(10000)
    Auth = {}
    for row in df.values:
        auth = str(row[6])
        Auth[auth] = csv
    return Auth

def compare_auth(Auth1, Auth2):
    OverlapSet = {}
    for auth in Auth1:
        if auth in Auth2:
            print('\n Author: {' + auth + '} is in both [' + Auth1[auth] + '] & [' + Auth2[auth] + '] \n')
            OverlapSet[auth] = Auth1[auth] + ' && ' + Auth2[auth]
    return OverlapSet
