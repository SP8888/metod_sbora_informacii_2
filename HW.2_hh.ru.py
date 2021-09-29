from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pprint import pprint
import json
import pandas as pd

url = 'https://hh.ru/search/vacancy'

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}


zapros = input('Введите требуемую професию (если несколько слов, то вводите через +) - ')
i = 0
vacancy = []
while True:
    response = requests.get(f'{url}?clusters=true&enable_snippets=true&search_field=name&text={zapros}&L_save_area=true&area=113&from=cluster_area&showClusters=true&page={i}', headers=headers)
    soup = bs(response.text,'html.parser')
    vacancy_list = soup.find_all('div',{'class':'vacancy-serp-item'})
    if not vacancy_list or not response.ok:
        break

    for vac in vacancy_list:
            vac_data={}
            vac_link = url + vac.find('a', class_='bloko-link').get('href')
            vac_name = vac.find('div',{'class':'g-user-content'}).getText()
            vac_site = url
            vac_zp_info = vac.find('div',{'class':'vacancy-serp-item__sidebar'})
            if vac_zp_info != None:
                vac_zp = vac_zp_info.text
            vac_data['name'] = vac_name
            vac_data['link'] = vac_link
            vac_data['site'] = vac_site
            vac_data['zp'] = vac_zp
            vacancy.append(vac_data)

    i = i + 1

df_vacancy = pd.DataFrame(vacancy)
df_vacancy.to_csv(f'vacancy_{zapros}.csv')
pprint(type(df_vacancy[zp]))


