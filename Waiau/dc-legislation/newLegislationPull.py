'''
Dependencies:
    *Self built methods*
    - dcLegislation.py
        - This method has a dependency on requests as well
    *Libraries*
    - json
    - pprint
    - pandas
    - csv
    - os
API help from DC Council Website:http://lims.dccouncil.us/api/Help
newLegislationPull.py is utilizes the advanced search feature in the LIMS API
specifically to request details on all the legislation from the current (22)
council period.

|Signature-------------------------------------------|
|Written for DC Policy Center by Michael Watson; 2017|
|www.DCPolicyCenter.org / DC-Policy-Center.github.io |
|github:M-Watson & MW-DC-Policy-Center               |
|----------------------------------------------------|
'''
#Requests for POST call, json for parsing, pprint for pretty print outputs, pandas for database, csv for csv writing

import requests, json, pprint, pandas, csv, dcLegislationSTATIC,datetime,sys

#Initial options for user
verbose = True                                      #Prints out statements to command line about the process being run
tic_toc_track = True                                #Keeps track of the time elapsed for each process
if(tic_toc_track == True):
    import time                                     #Import time for tic_toc fuctionality
    tic = time.time()                               # Setting start time of program to do a time elapsed/ tic toc print statement
legislation_number_iteration_statement_mod = 30     #Sets how frequently the legislation print statement runs
todays_date              =  datetime.date.today()
days_to_subtract         =   1
start_date_dateObj       =   todays_date - datetime.timedelta(days=days_to_subtract)
start_date_year          =   str(start_date_dateObj.year)
start_date_month         =   str(start_date_dateObj.month)
start_date_day           =   str(start_date_dateObj.day)
start_date_full_string   =   '%s/%s/%s'%(start_date_month,start_date_day,start_date_year)
#Building Request
#Sets advanced search query to search for current council period (22)

options = {

            'StartDate': start_date_full_string,

            #api wrapper call options section
            'verbose':False,

            #api call options section
            'offSet':'0',
            'rowLimit':'100',


}


csvHeader = []
csvHeader.append('Introducer') #Initialize empty list for headers for CSV writing
dataHeaders = [     'Id','CouncilPeriod','ShortTitle','Introducer',
                    'LegislationNumber','LawNumber','ActNumber',
                    'IntroductionDate','Modified','CommitteeReferral',
                    'CommitteeReferralComments','Deemed','DeemedOn',
                    'LegislationStatus','Category','Subcategory','DocumentUrl']
introducerException = 0
if(tic_toc_track):toc_initialize = time.time()


# Using API helper to send POST request to LIMS
if(verbose):print('\nRequest sent...')
response = dcLegislation.post.advancedSearch(**options)
data_json = response.json()

if(verbose):print('\nCreating JSON file...')
with open('newLegislation.json','w') as f:
    toWrite = json.dumps(response.json())
    pprint.pprint(toWrite,f)
f.close()
if(verbose):print('\nJSON file done...')
if(tic_toc_track):toc_json_write = time.time()




if(verbose):print('\nCreating CSV file...')
with open('tmp.csv','a', newline='',encoding='utf-8') as f:
    csvWriter = csv.writer(f)
    for key, value in data_json[0].items():
        csvHeader.append(key)
    csvWriter.writerow(csvHeader)
    for i in range(len(data_json)):
        if(verbose):
            if(i%legislation_number_iteration_statement_mod == 0):
                print('\n!!! Processing Legislation number:%i of %i'%(i,len(data_json)))
        LN = data_json[i]['LegislationNumber']               # LN: Legislation Number
        LND = dcLegislation.get.details(LN)          # LND; Legislation Number Details
        jLND = LND.json()                                    # jLND: JSON format of Legislation Number Details
        try:
            introducer = jLND['Legislation']['Introducer']   # The introducer of the legislation
        except:
            introducer = 'NONE'    #Some pieces of legislation have no introducer

        row = []
        row.append(introducer)
        for key, value in data_json[i].items():
            row.append(value)
        csvWriter.writerow(row)
        #pprint.pprint(data_json[i]['LegislationNumber'],f)
f.close()
if(verbose):print('\nCSV file done...')
if(tic_toc_track):toc_csv_write = time.time()




if(verbose):print('\nBuilding dataframe...')
df = pandas.read_csv('tmp.csv',encoding='utf-8')
df = df.sort_values(by='Id',ascending=False)
if(verbose):print('\nWriting dataframe to CSV file...')
df.to_csv('New Legislation.csv', index=False, columns=dataHeaders)

if(tic_toc_track):toc_pandas_write = time.time()



print('Cleaning up directory...')
import os                               # Importing os to delete files in directory
os.remove('newLegislation.json')
os.remove('tmp.csv')

if tic_toc_track == True:
    tic_toc_initialize = toc_initialize - tic
    tic_toc_json_write = toc_json_write - tic
    tic_toc_csv_write = toc_csv_write - tic
    tic_toc_pandas_write = toc_pandas_write - tic

    print('\n**********************\n')
    print('Timing metrics...\n')
    print('Tic Toc Initialize:  %s seconds...\n'%(str(tic_toc_initialize)))
    print('Tic Toc JSON:  %s seconds...\n'%(str(tic_toc_json_write)))
    print('Tic Toc CSV:  %s seconds...\n'%(str(tic_toc_csv_write)))
    print('Tic Toc PANDAS:  %s seconds...\n'%(str(tic_toc_pandas_write)))
