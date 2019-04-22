import pandas as pd
import requests
import filecmp

import os



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


save_path = "~/Documents/data"

i = 0
for i in range(len(data_to_pull)):

    name = data_to_pull['name'][i]
    file_name = data_to_pull['filename'][i]
    url = data_to_pull['endpoint'][i]
    full_file_name = os.path.join(save_path,file_name)


    print("{} : {}".format(data_to_pull['name'][i],data_to_pull['endpoint'][i]))

    request_and_download(url,full_file_name)

    i+=1
