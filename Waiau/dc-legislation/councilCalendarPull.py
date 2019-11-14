import requests
from bs4 import BeautifulSoup as bs
import re, time
import os, sys
#os.chdir(sys.path[0])
#sep = os.path.sep



all_hearings = []
previous_date = ''

with open('councilCalendar.html','w') as f:
    style_string = '''
    body {font-family : serif; -webkit-print-color-adjust: exact; color-adjust: exact; }
    h1 {text-align : center;background-color : gray !important;font-family : sans-serif; }
    h2 {font-family : sans-serif;margin-left: 15%;}
    h3 {font-family : sans-serif;margin-left: 15%;}
    .base {max-width : 800px; margin-left: 17%;}
    .hearingHeader {background-color:white;}
'''
    head = "<head><meta charset='UTF-8'> <link rel=\"stylesheet\" type=\"text/css\" href=\"./councilCalendarStyle.css\"><style>{}</style></head> ".format(style_string)
    f.write(head)
    f.close()

for page_number in range(3):
    page_number +=1
    url = "http://dccouncil.us/events/list/?tribe_paged=%s"%str(page_number)

    res = requests.get(url)

    soup = bs(res.content,"lxml")

    calendar_date = soup.find("div",{'class':'listing-header__subhead'})

    articles = soup.find_all('article')
    ul_list = []
    hearing_dict = {}
    article_number = 0
    article_dict_list = []

    for article in articles:
        article_number +=1
        date = 'missing-date'
        committee = 'missing-committee'
        subject = 'missing-subject'


        date = article.time
        #date = re.match(r"<time datetime=\"(.*)\+0000",str(date))
        # change to -400 during daylight savings
        date = re.match(r"<time datetime=\"(.*)\-0500",str(date))
        try:
            date = date.group(1)
        except:
            date = 'NONETYPE'

        try:
            committee = article.a['title']
        except:
            committee = 'missing-committee'

        subj_list = []
        try:
            subj = article.find("div", {"class": "base"})
            subj_2 = subj.find("a", {"class" : "pdfemb-viewer"}).decompose()

            #subj_3 = subj.find("a", {"class" : "button-text-link"}).decompose()
            #subj_4 = re.find(r"\"]",str(subj))
            #pdf_viewer = subj.findAll("a", {"class": "pdfemb-viewer"})
            #button_text = subj.findAll("a", {"class": "button-text-link"})
        except: subj = ['NoneType']

        subject = subj #article.ul
        stripped_date = date[5:16]
        if stripped_date == previous_date: stripped_date = ''
        previous_date = date[5:16]

        hearing_dict={
            'index':article_number,
            'committee':committee,
            'subject':subject,
            'date':date,
            'date_to_show':stripped_date,
            'time':time}


        article_dict_list.append(hearing_dict)
        all_hearings.append(hearing_dict)
        #print(article_dict_list)

        date_header = "\n<!--- Hearing --->\n<h1>{}</h1>".format(hearing_dict["date_to_show"])
        committee_header = "    <div class = \"hearingHeader\"> <h2>{}</h2>".format(hearing_dict["committee"])
        date_subheader = "    <h3>{}</h3> </div>".format(hearing_dict["date"])
        subj_content = "        {}".format(hearing_dict["subject"])

        html = "\n{}\n{}\n{}\n{}\n".format(date_header,committee_header,date_subheader,subj_content)

        with open('councilCalendar.html','a',encoding="utf-8") as f:
            f.write(html)
            f.close()
