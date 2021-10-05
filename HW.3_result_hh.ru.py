from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import json
import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient

# функция обрабатывает данные о з/п и выводит минимальную и максимальную з/п для каждой вакансии
def clean_zp(df_vacanc):
    df_vacanc = df_vacanc.fillna('none')
    df_el = df_vacanc['zp']
    vacancy_zp = []
    i = 0
    while i < len(df_vacanc):
        df_zp={}
        elem = df_el[i].split(' ')

        if  df_el[i] != '':
            if len(elem) == 4:
                df_zp['minim'] = float_return(elem[0])
                df_zp['maxim'] = float_return(elem[2])
                df_zp['valuta'] = elem[3]
                i += 1
            else:
                if df_el[i].startswith('от'):
                    df_zp['minim'] = float_return(elem[1])
                    df_zp['maxim'] = 'none'
                    df_zp['valuta'] = elem[2]
                    i += 1
                else:
                    if df_el[i].startswith('до'):
                        df_zp['minim'] = 'none'
                        df_zp['maxim'] = float_return(elem[1])
                        df_zp['valuta'] = elem[2]
                        i += 1
        else:
            df_zp['minim'] = 'none'
            df_zp['maxim'] = 'none'
            df_zp['valuta'] = 'none'
            i += 1
        vacancy_zp.append(df_zp)


    return(vacancy_zp)

# функция переводит строковые данные о з/п в тип целого числа
def float_return(str):

    l = len(str)
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = str[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = str[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))
    return integ[0]*1000

# функция возвращает уникальное id для каждой записи, берет данные для него из ссылки 'link'

def get_id(str):
    l = len(str)
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = str[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = str[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))
    print(integ[0])
    return (integ[0])

# функция вставляет новый документ, если его еще нет в колекции, проверка идет по полю '_id'

def add_new_doc(vac,df):
    try:
        for index, row in df.iterrows():
            vac.insert_one({
                "_id": get_id(row['link']),
                "name": row['name'],
                "link": row['link'],
                "site": row['site'],
                "min_zp": row['min_zp'],
                "max_zp": row['max_zp'],
                "valuta": row['valuta']
            })
    except pymongo.errors.DuplicateKeyError:
        print('Document already exist')

# функция которая ищет значение зарплат выше заданной

def search_zp (vacancy_pr):
    zp_min_search = input('Введите нижнее значение зарплаты ')

    for doc in vacancy_pr.find({'$or': [{'min_zp': {'$gt' : zp_min_search}},
                                        {'max_zp': {'$gt' : zp_min_search}}
                                        ]
                                }):
        pprint(doc)

# основная часть программы


url = 'https://hh.ru/search/vacancy'

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'}

# сбор информации в интернете по запросу наименовании професии

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

vacancy_zp = clean_zp(df_vacancy)  # обрабатывает данные о зарплате в функции

df_vacancy_zp = pd.DataFrame(vacancy_zp)

del df_vacancy['zp']   # удаляет старый столбик с зарплатой

df_vacancy.insert(3, 'min_zp', df_vacancy_zp['minim'])  #обновляет данные о з/п
df_vacancy.insert(4, 'max_zp', df_vacancy_zp['maxim'])
df_vacancy.insert(5, 'valuta', df_vacancy_zp['valuta'])


df_vacancy.to_csv(f'vacancy_{zapros}.csv')  # запись в файл


client = MongoClient('127.0.0.1', 27017)   # создает базу данных
db = client['vacancy']
vacancy_pr = db.vacancy_pr

add_new_doc(vacancy_pr,df_vacancy)  # добавляет данные в базу данных через функцию, которая проверяет наличие повторной записи документа через "_id"

for doc in vacancy_pr.find({}):    # распечатывает что получилось
    pprint(doc)

search_zp(vacancy_pr)  # вызов функции которая ищет зарплаты выше заданной






