from pprint import pprint
import json
import pandas as pd
import numpy as np

df = pd.read_csv('vacancy_программист.csv')
df = df.fillna('none')  # заполняем пробелы значением 'none'

df_el = df['zp']


vacancy_zp = []
i = 0
while i < len(df):
    df_zp={}
    elem = df_el[i].split(' ')
    if df_el[i] != 'none':
        if len(elem) == 4:
            df_zp['minim'] = elem[0]
            df_zp['maxim'] = elem[2]
            df_zp['valuta'] = elem[3]
            i += 1
        else:
            if df_el[i].startswith('от'):
                df_zp['minim'] = elem[1]
                df_zp['maxim'] = 'none'
                df_zp['valuta'] = elem[2]
                i += 1
            else:
                if df_el[i].startswith('до'):
                    df_zp['minim'] = 'none'
                    df_zp['maxim'] = elem[1]
                    df_zp['valuta'] = elem[2]
                    i += 1
    else:
        df_zp['minim'] = 'none'
        df_zp['maxim'] = 'none'
        df_zp['valuta'] = 'none'
        i += 1
    vacancy_zp.append(df_zp)

df_vacancy = pd.DataFrame(vacancy_zp)


df_vacancy.insert(0, 'Наименование вакансии', df['name'])
df_vacancy.insert(0, 'Ссылка на вакансию', df['link'])
df_vacancy.insert(0, 'Сайт источник данных', df['site'])
pprint(df_vacancy)