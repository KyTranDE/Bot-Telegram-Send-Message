import requests
import yaml
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import random
import redis
from messageTelegram.app import sendBot
import asyncio
import nest_asyncio
import time

nest_asyncio.apply()

with open('./config/config.yml', 'r') as f:
    config = yaml.safe_load(f)

redis_sv = config['redis_sv']
print(redis_sv)
redis_client = redis.Redis(**redis_sv)

urlproxy = config['url']['urlproxy']
listip = []
listport = []

def getproxy(urlproxy):
    headers = config['headers'] 
    response = requests.get(urlproxy, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data['proxies']:
            listip.append(item['ip'])
            listport.append(item['port'])
            
def getData(urlbonban,df):
    # dfproxy = pd.read_csv('./data/proxys.csv')
    dfproxy = df
    proxies = dfproxy.to_dict('records')
    
    while proxies:
        proxy = random.choice(proxies)
        proxy_dict = {
            "http": f"http://{proxy['ip']}:{proxy['port']}",
            "https": f"http://{proxy['ip']}:{proxy['port']}"
        }
        # print(proxy_dict)
        redis_set_key = "carbonbanh"

        try:
            response = requests.get(url=urlbonban, proxies=proxy_dict, timeout=10)   
            # print(response.status_code)         
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                all_results = soup.find_all('li', class_=['car-item row1','car-item row2'])
                for result in all_results:
                    data = {}
                    data["name"] = result.find('h3').text
                    data["price"] = result.find('div', class_='cb3').text
                    data["location"] = result.find('div', attrs={'class':'cb7'}).text
                    data["urlcar"] = "https://bonbanh.com/" + result.find('a', attrs={'itemprop':'url'}).get('href')
                    data['image'] = result.find('img',attrs={"class":"h-car-img"}).get('src')
                    # print(data)
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
                return  
        except :
            pass        
    
def main():

    listproxy = []
    for i in range(0, 1000, 15):
        listproxy.append(urlproxy.format(i))

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(getproxy, listproxy)
    df = pd.DataFrame({'ip': listip, 'port': listport})

    # df.to_csv('./data/proxys.csv', index=False)
    urlbonban = config['url']['urlbonbanh']
    listUrl = [urlbonban.format(i) for i in range(1, 2)]
    for url in listUrl:
        getData(url,df)

if __name__ == '__main__':
    while True:
        main()
        time.sleep(30*60) # 30 p
        # time.sleep(2)

