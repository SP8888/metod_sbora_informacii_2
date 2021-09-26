#e5e4cd692a72b0b66ea0a6b80255d1c3
from pprint import pprint
import requests
url = 'https://api.openweathermap.org/data/2.5/weather'
appid = 'e5e4cd692a72b0b66ea0a6b80255d1c3'

params = {'q':'Kaliningrad,ru',
          'appid':appid}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

response = requests.get(url,headers=headers,params=params)
j_data = response.json()
# pprint(j_data)
print(f"Погода в городе  {j_data['name']} температура  {j_data['main']['temp'] - 273.15} градусов")