'''                                
Created By Cason Konzer June 2021
Version 1.0
'''
import pandas as pd
import matplotlib.pyplot as plt
import time



def importcsv():
    csvfile = input('Please input full csv filename \n')
    global df
    df = pd.read_csv(csvfile, low_memory=False)

def plot_date_vs_numcomm(kind):
    if kind == 'N':
        df.plot(x='Post Date', y='# Comments')
    if kind == 'S':
        df.plot.scatter(x='Post Date', y='# Comments')
    plt.show()

def plot_date_vs_score(kind):
    if kind == 'N':
        df.plot(x='Post Date', y='Score', color='red')
    if kind == 'S':
        df.plot.scatter(x='Post Date', y='Score', color='red')
    plt.show()

def plot_post_vs_numcomm(kind):
    if kind == 'N':
        df.plot(x='Parent Id', y='# Comments', color='green')
    if kind == 'S':
        df.plot.scatter(x='Parent Id', y='# Comments', color='green')
    plt.show()


if __name__ == '__main__':
    importcsv()
    plot_date_vs_numcomm('S')
