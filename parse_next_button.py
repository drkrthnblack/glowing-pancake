#!usr/bin/env python
#Загружает комиксы XKCD
import os, requests, bs4
from time import sleep

url = 'https://xkcd.com'
# url = 'https://xkcd.com/5'
os.makedirs('saved_images', exist_ok=True)
headers = {  
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0',
}
while not url.endswith('#'):
  print(f'Загружается страница {url}')

  response = requests.get(url, headers=headers)
  response.raise_for_status()
  soup = bs4.BeautifulSoup(response.text, 'lxml')
  img_elem = soup.select('#comic img')
  sleep(1)

  if img_elem == []:
    print('Не удалось найти изображение')
  else:
    img_url = 'https:' + img_elem[0].get('src')
    # img_url = 'https:' + img_elem[0].get('srcset').rstrip(' 2x')
    print(f'Загружается изображение {img_url}')
    response = requests.get(img_url, headers=headers)
    response.raise_for_status()
#Сохранение изображения
    with open(os.path.join('saved_images', os.path.basename(img_url)), 'wb') as file:
      for chunk in response.iter_content(75000):
        file.write(chunk)
    
  sleep(3)  
  prev_link = soup.select('a[rel="prev"]')[0]
  url = 'https://xkcd.com' + prev_link.get('href')

print('Готово')