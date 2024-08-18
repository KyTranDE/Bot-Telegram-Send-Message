import requests
import yaml
from bs4 import BeautifulSoup
import json
import time
import redis
from messageTelegram.app import sendBot
import asyncio
import nest_asyncio
from Utils import postgres_tool
nest_asyncio.apply()

with open('./config/config.yml', 'r') as f:
    config = yaml.safe_load(f)

redis_sv = config['redis_sv']
print(redis_sv)
redis_client = redis.Redis(**redis_sv)

def getData(urlchotot):
    try:
        response = requests.get(url=urlchotot)
        soup = BeautifulSoup(response.text, 'html.parser')
        all_results = soup.find_all('div', attrs={'tabindex':"0"})
        db_config = config["database"]    
        conn =  postgres_tool.PostgresTool(**db_config)
        for result in all_results:
            newRequest = requests.get("https://xe.chotot.com"+result.find('a',attrs={'itemprop':'item'}).get('href'))
            newSoup = BeautifulSoup(newRequest.text, 'html.parser')
            data = {}
            data["name"] = newSoup.find('h1').text
            data["price"] = newSoup.find('b', class_='p26z2wb').text
            data["location"] = newSoup.find('span', class_ = "bwq0cbs flex-1").text
            data["urlcar"] = "https://xe.chotot.com"+result.find('a',attrs={'itemprop':'item'}).get('href')
            data['image'] = "https://xe.chotot.com"+newSoup.findAll('img', attrs={'sizes':'100vw'})[1].get('src')
            data['sent'] = False
            conn.push_data('car', data)
        conn.close()
    except :
        pass

def main():
    urlchotot = config['url']['urlchotot']
    listUrl = ['https://xe.chotot.com/mua-ban-oto-tp-ho-chi-minh?page=1',
    'https://xe.chotot.com/mua-ban-oto-tp-ho-chi-minh?page=2',
    'https://xe.chotot.com/mua-ban-oto-tp-ho-chi-minh?page=3',
    'https://xe.chotot.com/mua-ban-oto-tp-ho-chi-minh?page=4',
    'https://xe.chotot.com/mua-ban-oto-tp-ho-chi-minh?page=5',
    'https://xe.chotot.com/mua-ban-oto-an-giang?page=1',
    'https://xe.chotot.com/mua-ban-oto-an-giang?page=2',
    'https://xe.chotot.com/mua-ban-oto-an-giang?page=3',
    'https://xe.chotot.com/mua-ban-oto-an-giang?page=4',
    'https://xe.chotot.com/mua-ban-oto-an-giang?page=5',
    'https://xe.chotot.com/mua-ban-oto-ba-ria-vung-tau?page=1',
    'https://xe.chotot.com/mua-ban-oto-ba-ria-vung-tau?page=2',
    'https://xe.chotot.com/mua-ban-oto-ba-ria-vung-tau?page=3',
    'https://xe.chotot.com/mua-ban-oto-ba-ria-vung-tau?page=4',
    'https://xe.chotot.com/mua-ban-oto-ba-ria-vung-tau?page=5',
    'https://xe.chotot.com/mua-ban-oto-bac-lieu?page=1',
    'https://xe.chotot.com/mua-ban-oto-bac-lieu?page=2',
    'https://xe.chotot.com/mua-ban-oto-bac-lieu?page=3',
    'https://xe.chotot.com/mua-ban-oto-bac-lieu?page=4',
    'https://xe.chotot.com/mua-ban-oto-bac-lieu?page=5',
    'https://xe.chotot.com/mua-ban-oto-ben-tre?page=1',
    'https://xe.chotot.com/mua-ban-oto-ben-tre?page=2',
    'https://xe.chotot.com/mua-ban-oto-ben-tre?page=3',
    'https://xe.chotot.com/mua-ban-oto-ben-tre?page=4',
    'https://xe.chotot.com/mua-ban-oto-ben-tre?page=5',
    'https://xe.chotot.com/mua-ban-oto-binh-duong?page=1',
    'https://xe.chotot.com/mua-ban-oto-binh-duong?page=2',
    'https://xe.chotot.com/mua-ban-oto-binh-duong?page=3',
    'https://xe.chotot.com/mua-ban-oto-binh-duong?page=4',
    'https://xe.chotot.com/mua-ban-oto-binh-duong?page=5',
    'https://xe.chotot.com/mua-ban-oto-binh-phuoc?page=1',
    'https://xe.chotot.com/mua-ban-oto-binh-phuoc?page=2',
    'https://xe.chotot.com/mua-ban-oto-binh-phuoc?page=3',
    'https://xe.chotot.com/mua-ban-oto-binh-phuoc?page=4',
    'https://xe.chotot.com/mua-ban-oto-binh-phuoc?page=5',
    'https://xe.chotot.com/mua-ban-oto-ca-mau?page=1',
    'https://xe.chotot.com/mua-ban-oto-ca-mau?page=2',
    'https://xe.chotot.com/mua-ban-oto-ca-mau?page=3',
    'https://xe.chotot.com/mua-ban-oto-ca-mau?page=4',
    'https://xe.chotot.com/mua-ban-oto-ca-mau?page=5',
    'https://xe.chotot.com/mua-ban-oto-can-tho?page=1',
    'https://xe.chotot.com/mua-ban-oto-can-tho?page=2',
    'https://xe.chotot.com/mua-ban-oto-can-tho?page=3',
    'https://xe.chotot.com/mua-ban-oto-can-tho?page=4',
    'https://xe.chotot.com/mua-ban-oto-can-tho?page=5',
    'https://xe.chotot.com/mua-ban-oto-dong-nai?page=1',
    'https://xe.chotot.com/mua-ban-oto-dong-nai?page=2',
    'https://xe.chotot.com/mua-ban-oto-dong-nai?page=3',
    'https://xe.chotot.com/mua-ban-oto-dong-nai?page=4',
    'https://xe.chotot.com/mua-ban-oto-dong-nai?page=5',
    'https://xe.chotot.com/mua-ban-oto-dong-thap?page=1',
    'https://xe.chotot.com/mua-ban-oto-dong-thap?page=2',
    'https://xe.chotot.com/mua-ban-oto-dong-thap?page=3',
    'https://xe.chotot.com/mua-ban-oto-dong-thap?page=4',
    'https://xe.chotot.com/mua-ban-oto-dong-thap?page=5',
    'https://xe.chotot.com/mua-ban-oto-hau-giang?page=1',
    'https://xe.chotot.com/mua-ban-oto-hau-giang?page=2',
    'https://xe.chotot.com/mua-ban-oto-hau-giang?page=3',
    'https://xe.chotot.com/mua-ban-oto-hau-giang?page=4',
    'https://xe.chotot.com/mua-ban-oto-hau-giang?page=5',
    'https://xe.chotot.com/mua-ban-oto-kien-giang?page=1',
    'https://xe.chotot.com/mua-ban-oto-kien-giang?page=2',
    'https://xe.chotot.com/mua-ban-oto-kien-giang?page=3',
    'https://xe.chotot.com/mua-ban-oto-kien-giang?page=4',
    'https://xe.chotot.com/mua-ban-oto-kien-giang?page=5',
    'https://xe.chotot.com/mua-ban-oto-long-an?page=1',
    'https://xe.chotot.com/mua-ban-oto-long-an?page=2',
    'https://xe.chotot.com/mua-ban-oto-long-an?page=3',
    'https://xe.chotot.com/mua-ban-oto-long-an?page=4',
    'https://xe.chotot.com/mua-ban-oto-long-an?page=5',
    'https://xe.chotot.com/mua-ban-oto-soc-trang?page=1',
    'https://xe.chotot.com/mua-ban-oto-soc-trang?page=2',
    'https://xe.chotot.com/mua-ban-oto-soc-trang?page=3',
    'https://xe.chotot.com/mua-ban-oto-soc-trang?page=4',
    'https://xe.chotot.com/mua-ban-oto-soc-trang?page=5',
    'https://xe.chotot.com/mua-ban-oto-tay-ninh?page=1',
    'https://xe.chotot.com/mua-ban-oto-tay-ninh?page=2',
    'https://xe.chotot.com/mua-ban-oto-tay-ninh?page=3',
    'https://xe.chotot.com/mua-ban-oto-tay-ninh?page=4',
    'https://xe.chotot.com/mua-ban-oto-tay-ninh?page=5',
    'https://xe.chotot.com/mua-ban-oto-tien-giang?page=1',
    'https://xe.chotot.com/mua-ban-oto-tien-giang?page=2',
    'https://xe.chotot.com/mua-ban-oto-tien-giang?page=3',
    'https://xe.chotot.com/mua-ban-oto-tien-giang?page=4',
    'https://xe.chotot.com/mua-ban-oto-tien-giang?page=5',
    'https://xe.chotot.com/mua-ban-oto-tra-vinh?page=1',
    'https://xe.chotot.com/mua-ban-oto-tra-vinh?page=2',
    'https://xe.chotot.com/mua-ban-oto-tra-vinh?page=3',
    'https://xe.chotot.com/mua-ban-oto-tra-vinh?page=4',
    'https://xe.chotot.com/mua-ban-oto-tra-vinh?page=5',
    'https://xe.chotot.com/mua-ban-oto-vinh-long?page=1',
    'https://xe.chotot.com/mua-ban-oto-vinh-long?page=2',
    'https://xe.chotot.com/mua-ban-oto-vinh-long?page=3',
    'https://xe.chotot.com/mua-ban-oto-vinh-long?page=4',
    'https://xe.chotot.com/mua-ban-oto-vinh-long?page=5'
 ]
    for url in listUrl: 
        getData(url)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(30*60) # 30 p
        # time.sleep(2)
