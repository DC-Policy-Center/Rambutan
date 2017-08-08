import pandas
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import csv
import sys
a = 'test legislation from 7-11-2017'
b = 'Legislation from-8-3-2017'
all_data = pandas.read_csv("./daily-legislation/csv-files/%s.csv"%a)
all_data.fillna('Not Referred',inplace=True)

list_of_all_committees = []
list_of_unique_committees = []
dictionary_of_unique_committees = {}
if 'null' in all_data.keys():
    print('breaking, no legislation to process...')
    dictionary_of_unique_committees={
                                'Committee on Housing and Neighborhood Revitalization':0,
                                'Committee on Business and Economic Development':0,
                                'Committee of the Whole':0,
                                'Committee on Education':0,
                                'Committee on Finance and Revenue':0,
                                'Committee on Government Operations':0,
                                'Committee on Health':0,
                                'Committee on Human Services':0,
                                'Committee on the Judiciary and Public Safety':0,
                                'Committee on Transportation and the Environment':0,
                                'Committee on Labor and Workforce Development':0,
                                'Retained by the Council':0,
                                'Not Referred':0}
    header = 'Committee,value\n'
    with open('testoutput.csv','w',newline = '\n') as f:
        f.write(header)
        for key,value in dictionary_of_unique_committees.items():
            new_key = ''.join(key)
            print(new_key)
            row = "%s"%(new_key)+",%i"%(value)
            f.write(row+'\n')
    f.close()
    sys.exit('null')



for item in all_data['CommitteeReferral']:
    list_of_all_committees.append(item)

for item in list_of_all_committees:
    if item not in list_of_unique_committees:
        list_of_unique_committees.append(item)
        dictionary_of_unique_committees.setdefault(item,list()).append(0)

for item in all_data['CommitteeReferral']:
    try:
        old_value = dictionary_of_unique_committees[item]
        new_value = old_value + 1
    except:
        old_value = dictionary_of_unique_committees[item][0]
        new_value = old_value + 1
    dictionary_of_unique_committees[item] = new_value

header = 'Committee,value\n'
with open('testoutput.csv','w',newline = '\n') as f:
    f.write(header)
    for key,value in dictionary_of_unique_committees.items():
        new_key = ''.join(key)
        print(new_key)
        row = "%s"%(new_key)+",%i"%(value)
        f.write(row+'\n')
f.close()
