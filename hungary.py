from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import pandas as pd

options = Options()
options.headless = True

driver = webdriver.Firefox(options = options)
driver.get("https://www.police.hu/hu/hirek-es-informaciok/hatarinfo?field_hat_rszakasz_value=ukr%C3%A1n+hat%C3%A1rszakasz")
driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
divs = soup.find_all('div', {'class' : 'panel panel-primary'})
crossing_data = list()
for div in divs:
    data = dict()
    header = div.find('h5').get_text().strip().split('\n')
    data['crossing'] = header[0][:-2]
    data['crossing_times'] = header[1]
    inner_divs = div.find_all('div', {'class' : 'col-xs-12'})
    try:
        data['waiting_time_outgoing_car'] = inner_divs[0].find('div', {'class' : 'szgk'}).get_text().strip()
    except:
        pass
    try:
        data['waiting_time_incoming_car'] = inner_divs[1].find('div', {'class' : 'szgk'}).get_text().strip()
    except:
        pass
    try:
        data['waiting_time_outgoing_bus'] = inner_divs[0].find('div', {'class' : 'busz'}).get_text().strip()
    except:
        pass
    try:
        data['waiting_time_incoming_bus'] = inner_divs[1].find('div', {'class' : 'busz'}).get_text().strip()
    except:
        pass
    data['traffic_type'] = inner_divs[2].find_all('div')[1].get_text().strip()
    data['alternate_crossings'] = inner_divs[3].find_all('div')[1].get_text().strip()
    crossing_data.append(data)

df = pd.DataFrame(crossing_data)
df.to_csv('hungary.csv')
print('[*] Scraped', len(df), '- Saved to https://www.youtube.com/watch?v=dQw4w9WgXcQ')
