'''
This is a single use python script for Rambutan/Waiau.  Please reference
dc-policy-center/dc-city-council github project to see live newLegislationPull.py script


|Signature-------------------------------------------|
|Written for DC Policy Center by Michael Watson; 2017|
|www.DCPolicyCenter.org / DC-Policy-Center.github.io |
|github:M-Watson & MW-DC-Policy-Center               |
|----------------------------------------------------|
'''
#Requests for POST call, json for parsing, pprint for pretty print outputs, pandas for database, csv for csv writing

import requests, json, pprint, pandas, csv,datetime,sys, os
import dcLegislationSTATIC as dcLegislation
os.chdir(sys.path[0])
sep = os.path.sep
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
start_date_full_string_dash_form   =   '%s-%s-%s'%(start_date_month,start_date_day,start_date_year)

final_file_name = 'Daily Legislation'+sep+'Legislation from-'+ start_date_full_string_dash_form + '.csv'
final_file_name_txt = 'Daily Legislation'+sep+'Legislation from-'+ start_date_full_string_dash_form + '.txt'

with open('new_legislation_log','a') as log_file:
    hr = str(time.localtime().tm_hour)
    min =str(time.localtime().tm_min)
    log_file.write('Starting run: '+start_date_full_string_dash_form+'--'+hr+':'+min+'\n')

# Output messages

request_sent_message = '\nRequest sent...'
creating_json_file_message = '\nCreating JSON file...'
json_file_done_message = '\nJSON file done...'
cleaning_up_directory_message = 'Cleaning up directory...'
creating_csv_file_message = '\nCreating CSV file...'
csv_file_done_message = '\nCSV file done...'
building_dataframe_message = '\nBuilding dataframe...'
writing_dataframe_to_csv_message = '\nWriting dataframe to CSV file...'



json_empty_error_break = "data_json len == 0"
#Building Request
with open('new_legislation_log','a') as log_file:
    log_file.write(start_date_full_string_dash_form)

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
if(verbose):print(request_sent_message)
response = dcLegislation.post.advancedSearch(**options)
data_json = response.json()

if(verbose):print(creating_json_file_message)
with open('newLegislation.json','a') as f:
    toWrite = json.dumps(response.json())
    pprint.pprint(toWrite,f)
f.close()
if(verbose):print(json_file_done_message)
if(tic_toc_track):toc_json_write = time.time()



if len(data_json) == 0:
#Cleaning any stry files from the directory after error call
    print(cleaning_up_directory_message)
    try:os.remove('newLegislation.json')
    except: pass
    try: os.remove('tmp.csv')
    except:pass

    with open(final_file_name,'a') as final_file: final_file.write('null,err: data_json len == 0')
    sys.exit(json_empty_error_break)


if(verbose):print(creating_csv_file_message)
with open('tmp.csv','w', newline='',encoding='utf-8') as f:
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
if(verbose):print(csv_file_done_message)
if(tic_toc_track):toc_csv_write = time.time()




if(verbose):print(building_dataframe_message)
df = pandas.read_csv('tmp.csv',encoding='utf-8')

try:
    df = df.sort_values(by='Id',ascending=False)
except:
    df = df.sort(columns='Id',ascending=False)
if(verbose):print(writing_dataframe_to_csv_message)
df.to_csv(final_file_name, index=False, columns=dataHeaders)
df.to_csv(final_file_name_txt,index=False,columns=dataHeaders)
if(tic_toc_track):toc_pandas_write = time.time()



print(cleaning_up_directory_message)
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
