'''                                
Created By Cason Konzer June 2021
Version 0.7
'''

import Dependencies as dp

start = dp.now() # get program start time
dp.um() # print UM art


print(('#####################' * 5) + '\n')


sub, name = dp.pull.community()
after = dp.pull.past(); before = dp.pull.future()

sc = 0; cc = 0

subdata = dp.pull.que(after, before, sub, 's')
comdata = dp.pull.que(after, before, sub, 'c')


print('\n<<< Variables Initialized >>>\n\n' + ('#####################' * 5) + '\n\n')


dp.pull.subs(sub, subdata, name, sc, cc)
dp.pull.coms(sub, comdata, name, sc, cc)


print('<<< your program has finished and your data is available in the run directory, stored in /' + name + ' >>>')


end = dp.now(); print('\n\n\nStarted: ' + str(start) + '\n\nFinished: ' + str(end) + '\n\n')


if __name__ == '__main__': 
    exit()
