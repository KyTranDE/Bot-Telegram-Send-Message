import requests
import yaml
from bs4 import BeautifulSoup
import json
import time
import redis
from messageTelegram.app import sendBot
import asyncio
import nest_asyncio

nest_asyncio.apply()

with open('./config/config.yml', 'r') as f:
    config = yaml.safe_load(f)

redis_sv = config['redis_sv']
print(redis_sv)
redis_client = redis.Redis(**redis_sv)

def getData(urlchotot):
    response = requests.get(url=urlchotot)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_results = soup.find_all('div', attrs={'tabindex':"0"})
    redis_set_key = "carchotot"

    for result in all_results:
        newRequest = requests.get("https://xe.chotot.com"+result.find('a',attrs={'itemprop':'item'}).get('href'))
        newSoup = BeautifulSoup(newRequest.text, 'html.parser')
        data = {}
        data["name"] = newSoup.find('h1').text
        data["price"] = newSoup.find('b', class_='p26z2wb').text
        data["location"] = newSoup.find('span', class_ = "bwq0cbs flex-1").text
        data["urlcar"] = "https://xe.chotot.com"+result.find('a',attrs={'itemprop':'item'}).get('href')
        data['image'] = "https://xe.chotot.com"+newSoup.findAll('img', attrs={'sizes':'100vw'})[1].get('src')
        redis_key = f"{data}" 
        exists = redis_client.sismember(redis_set_key, str(data))
        if not exists:
            redis_client.sadd(redis_set_key, str(data))
            redis_client.expire(redis_set_key, 60*60*24)
            redis_client.setex(redis_key, 60*60*24, str(data))

            data = {k: (v if v != "None" else None) for k, v in data.items()}
            # print(json.dumps(data, ensure_ascii=False, indent=2)) # debug
            # send data telegram message
            asyncio.run(sendBot(data))
        else:
            pass

def main():
    urlchotot = config['url']['urlchotot']
    listUrl = [urlchotot.format(i) for i in range(1, 10)]
    for url in listUrl: 
        getData(url)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(30*60) # 30 p
        # time.sleep(2)
