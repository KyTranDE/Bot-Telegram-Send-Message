import requests
import yaml
from bs4 import BeautifulSoup
import json
import time
import redis
from app import sendBot
import asyncio
import nest_asyncio
from Utils import postgres_tool
nest_asyncio.apply()

with open('./config/config.yml', 'r') as f:
    config = yaml.safe_load(f)

# redis_sv = config['redis_sv']
# print(redis_sv)
# redis_client = redis.Redis(**redis_sv)

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
    listUrl = ['https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tp-ho-chi-minh-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tp-ho-chi-minh-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tp-ho-chi-minh-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tp-ho-chi-minh-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tp-ho-chi-minh-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-an-giang-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-an-giang-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-an-giang-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-an-giang-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-an-giang-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ba-ria-vung-tau-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ba-ria-vung-tau-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ba-ria-vung-tau-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ba-ria-vung-tau-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ba-ria-vung-tau-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-bac-lieu-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-bac-lieu-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-bac-lieu-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-bac-lieu-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-bac-lieu-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ben-tre-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ben-tre-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ben-tre-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ben-tre-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ben-tre-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-duong-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-duong-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-duong-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-duong-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-duong-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-phuoc-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-phuoc-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-phuoc-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-phuoc-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-binh-phuoc-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ca-mau-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ca-mau-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ca-mau-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ca-mau-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-ca-mau-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-can-tho-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-can-tho-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-can-tho-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-can-tho-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-can-tho-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-nai-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-nai-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-nai-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-nai-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-nai-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-thap-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-thap-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-thap-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-thap-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-dong-thap-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-hau-giang-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-hau-giang-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-hau-giang-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-hau-giang-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-hau-giang-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-kien-giang-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-kien-giang-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-kien-giang-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-kien-giang-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-kien-giang-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-long-an-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-long-an-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-long-an-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-long-an-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-long-an-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-soc-trang-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-soc-trang-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-soc-trang-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-soc-trang-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-soc-trang-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tay-ninh-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tay-ninh-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tay-ninh-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tay-ninh-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tay-ninh-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tien-giang-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tien-giang-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tien-giang-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tien-giang-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tien-giang-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tra-vinh-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tra-vinh-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tra-vinh-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tra-vinh-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-tra-vinh-sdpr1?page=5',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-vinh-long-sdpr1?page=1',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-vinh-long-sdpr1?page=2',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-vinh-long-sdpr1?page=3',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-vinh-long-sdpr1?page=4',
    'https://xe.chotot.com/mua-ban-oto-gia-duoi-200-trieu-vinh-long-sdpr1?page=5'
 ]
    for url in listUrl: 
        getData(url)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(30*60) # 30 p
        # time.sleep(2)
