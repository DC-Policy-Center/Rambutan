import pandas
import matplotlib.pyplot as plt
import numpy as np
from operator import itemgetter
import csv
import os, sys, datetime, time
os.chdir(sys.path[0])
sep = os.path.sep

todays_date              =  datetime.date.today()
days_to_subtract         =   1
start_date_dateObj       =   todays_date - datetime.timedelta(days=days_to_subtract)

start_date_year          =   str(start_date_dateObj.year)
start_date_month         =   str(start_date_dateObj.month)
start_date_day           =   str(start_date_dateObj.day)
start_date_full_string   =   '%s/%s/%s'%(start_date_month,start_date_day,start_date_year)
start_date_full_string_dash_form   =   '%s-%s-%s'%(start_date_month,start_date_day,start_date_year)
''' To be added later
week_ago_date_dateObj = todays_date - datetime.timedelta(days=7)
week_ago_start_date_year          =   str(week_ago_start_date_dateObj.year)
week_ago_start_date_month         =   str(week_ago_start_date_dateObj.month)
week_ago_start_date_day           =   str(week_ago_start_date_dateObj.day)
week_ago_start_date_full_string   =   '%s/%s/%s'%(week_ago_start_date_month,week_ago_start_date_day,week_ago_start_date_year)
week_ago_start_date_full_string_dash_form   =   '%s-%s-%s'%(week_ago_start_date_month,week_ago_start_date_day,week_ago_start_date_year)
'''

log_file_name = 'daily-legislation'+sep+'processed_leg_log.txt'
with open(log_file_name,'a') as log_file:
    hr = str(time.localtime().tm_hour)
    min =str(time.localtime().tm_min)
    log_file.write('Starting run: '+start_date_full_string_dash_form+'--'+hr+':'+min+'\n')


a = 'test legislation from 7-11-2017'
b = 'Legislation from-8-3-2017'
final_file_name = 'daily-legislation'+sep+'csv-files'+sep+'Legislation from-'+ start_date_full_string_dash_form + '.csv'
print(final_file_name)
all_data = pandas.read_csv(final_file_name)
all_data.fillna('Not Referred',inplace=True)

list_of_all_committees = []
list_of_unique_committees = []
dictionary_of_unique_committees = {}
if 'null' in all_data.keys():
    print('breaking, no legislation to process...')
    with open(log_file_name,'a') as log_file:
        log_file.write('breaking, no legislation to process...\n')
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
    with open('.'+sep+'daily-legislation'+sep+'csv-files'+sep+'daily_legislation_committee_count_DUMP_ZERO_LEG.csv','w',newline = '\n') as f:
        f.write(header)
        for key,value in dictionary_of_unique_committees.items():
            new_key = ''.join(key)
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
with open(log_file_name,'a') as log_file:
    log_file.write('Writting committee count\n')
with open('.'+sep+'daily-legislation'+sep+'csv-files'+sep+'daily_legislation_committee_count.csv','w',newline = '\n') as f:
    f.write(header)
    for key,value in dictionary_of_unique_committees.items():
        new_key = ''.join(key)
        row = "%s"%(new_key)+",%i"%(value)
        f.write(row+'\n')
f.close()
