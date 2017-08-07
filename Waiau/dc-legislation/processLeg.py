import pandas
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import csv

all_data = pandas.read_csv("./daily-legislation/csv-files/test legislation from 7-11-2017.csv")

list_of_all_committees = []
list_of_unique_committees = []
dictionary_of_unique_committees = {}

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


with open('testoutput.csv','w') as f:
    w = csv.DictWriter(f,dictionary_of_unique_committees.keys(),delimiter=',',lineterminator='\n')
    w.writeheader()
    w.writerow(dictionary_of_unique_committees)
