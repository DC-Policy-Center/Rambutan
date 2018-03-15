'''
dcpolicycenter_publications.py will scrape all of the publications listed on the main DC Policy Center
website and format the output to a text file for future usage.

'''


from bs4 import BeautifulSoup as bs
import requests as req
import json
import re

file_head = 'title'+';;'+'url'+';;'+'author'+';;'+'date'+';;'+'tags'+'\n'
with open('title_list.txt','w') as f2:
    f2.write(file_head)
    f2.close()
page_int = 1

cont = True
string_to_write_list = []
while cont == True:
    page = str(page_int)
    dcpc_url = "https://www.dcpolicycenter.org/publications/page/%s"%page
    headers={'User-Agent': 'Mozilla/5.0'}

    response = req.get(dcpc_url,headers=headers)
    if response.status_code == 404:
        print('finished')
        cont = False
        break


    soup = bs(response.text,'html.parser')
    pretty = soup.prettify()
    '''
    with open('output.html' , 'w') as f:
         f.write(pretty)
    '''

    all_articles = soup.find_all('article')
    print(len(all_articles))
    title_list = []
    links = soup.find_all('a',{'class':'lightbox hide-for-large'},href=True)
    for i in range(len(all_articles)):
        article_link = links[i]['href']
        article_response = req.get(article_link,headers=headers)
        
        article_soup = bs(article_response.text,'html.parser')
        authors_and_date = article_soup.find_all('span',{'class':'post-meta'})
        tags = article_soup.find_all('p',{'class':'subtitle'})
        
        h1_finding = all_articles[i].find('h1')
        #title_list.append(h1_finding.text)

        with open('title_list.txt','a') as f2:
            try:
                string_to_write_start = h1_finding.text + ';;' + article_link +';;'+authors_and_date[0].text + ';;'+tags[0].text 
                string_to_write_replace_tabs = string_to_write_start.replace('\t','')
                string_to_write_replace_breaks = string_to_write_replace_tabs.replace('\n','')
                string_to_write = string_to_write_replace_breaks + '\n'
                string_to_write = string_to_write.replace('/ ',';;')
               
                string_to_write_list.append(string_to_write)
                f2.write(string_to_write)
            except:
                pass

        f2.close()
    page_int +=1
    print('\n moving to page %s\n'%(str(page_int)))
