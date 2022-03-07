import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import sys

url = "https://www.politiadefrontiera.ro/ro/traficonline/"
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser',)
script = soup.find_all('script', {'type' : 'text/javascript'})[-1]
data = str(script).split('var markers = ')[1].split('];')[0]+ ']'

location_data = list()
for location in data.split('{')[1:]:
    data = dict()
    fields = location.split('\n')
    data['location'] = fields[1].strip().split(':')[1][2:-2]
    data['lat'] = fields[2].strip().split(':')[1][2:-2]
    data['lng'] = fields[3].strip().split(':')[1][2:-2]
    try:
        data['wait_min'] = fields[4].strip().split(':')[1].split('Timp de așteptare ')[1].split(' min')[0]
        data['status'] = ''
    except:
        data['wait_min'] = ''
        data['status'] = fields[4].strip().split(':')[1].split('"iwrow">')[2].split('<')[0]
    data['marker_color'] = fields[5].strip().split(':')[1][2:-1]
    location_data.append(data)

df = pd.DataFrame(location_data)
df.to_csv('romania.csv', encoding = "utf-8-sig")
print('[*] Scraped', len(df), 'locations. Saved to romania.csv')
