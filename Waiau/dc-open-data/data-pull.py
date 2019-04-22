import csv
import requests
import filecmp

import os


def read_pull_list():
    data_list = []
    with open('open-data-pull-list.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data_list.append(row)
    return(data_list)

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


data_to_pull = read_pull_list()


save_path = "~/Documents/data"

i = 0
for i in range(len(data_to_pull)):

    name = data_to_pull[i]['name']
    file_name = data_to_pull[i]['filename']
    url = data_to_pull[i]['endpoint']
    full_file_name = os.path.join(save_path,file_name)

    request_and_download(url,full_file_name)

    i+=1
