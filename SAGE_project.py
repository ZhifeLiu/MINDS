import csv
from bs4 import BeautifulSoup
import requests
from dateutil.parser import parse
import re
import pandas as pd

if __name__ == "__main__":

    html = requests.get("https://en.wikipedia.org/wiki/2019_in_spaceflight#Orbital_launches").text #grabing the html from wikipedia
    soup = BeautifulSoup(html, 'html5lib')

    table = soup.find('table', {'class':'wikitable collapsible'})
    dates = []
    rows = table.find_all('tr')
    for tr in rows:
        if len(tr.find_all('td'))==5:
            td = tr.find_all('td')[0]
            date = td.find_all('span', {"class":"nowrap"})
            dates.append(date[0].text)
    date_array = []
    for each in dates:
        normal = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", each)
        datetime = parse(normal+ '2019')
        date_array.append(datetime.isoformat())

    date1 = '2019-01-01'
    date2 = '2019-12-31'
    mydates = pd.date_range(date1, date2).tolist()
    days_dict = {}
    for each in mydates:
        days_dict[each.isoformat()]=0

    for each in date_array:
        if each in days_dict:
            days_dict[each]+=1

    with open('output.csv', 'w') as f:
        for key in days_dict.keys():
            f.write("%s,%s\n"%(key,days_dict[key]))