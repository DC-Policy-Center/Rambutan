import csv
import requests
import filecmp

import time
import os
import sys

def read_pull_list(full_path):
    data_list = []
    pullListPath = os.path.join("open-data-pull-list.csv")
    with open(pullListPath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_list.append(row)
    return(data_list)


def download_file(url,file_name):
    # NOTE the stream=True parameter below
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                # f.flush()
    return(file_name)


def request_and_download(url,file_name):
    response = requests.get(url)
    if response.status_code != 200:
        return('Invalid response code')
    else:
        content = response.content

    with open(file_name,'wb') as f:
        f.write(content)
    f.close()
    return('Valid response, written')


date = time.strftime("%m-%d-%y")
time = time.strftime("%H:%M:%S")

with open("dc-data-log.txt",'a') as log_start:
    log_start.write("\n{} -- {} -- Starting dataPull.py\n\t".format(date,time))
    log_start.close()   

os.chdir(sys.path[0])
full_path = os.path.join("~","Documents","github","Rambutan","Waiau","dc-open-data")
data_to_pull = read_pull_list(full_path)

#date = time.strftime("%m-%d-%y")
save_path = "../../data/{}".format(date)



try:
    os.mkdir(save_path)
except:
    print('Dir Exists')

i = 0
for i in range(len(data_to_pull)):

    name = data_to_pull[i]['name']
    file_name = data_to_pull[i]['filename']
    url = data_to_pull[i]['endpoint']
    full_file_name = os.path.join(save_path,file_name)

    download_file(url,full_file_name)

    i+=1


with open("dc-data-log.txt",'a') as f:
    line = "{} :: Wrote out {} files\n".format(date,str(i))
    f.write(line)
    f.close()


