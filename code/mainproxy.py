
import requests
import yaml
from concurrent.futures import ThreadPoolExecutor
import json
import pandas
with open('./config/config.yml', 'r') as f:
    config = yaml.safe_load(f)

urlproxy = config['url']['urlproxy']


def getproxy(urlproxy):
    headers = config['headers'] 
    response = requests.get(urlproxy, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for item in data['proxies']:
            listip.append(item['ip'])
            listport.append(item['port'])

if __name__ == '__main__':
    listip = []
    listport = []
    listproxy = []
    for i in range(0, 1000, 15):
        listproxy.append(urlproxy.format(i))

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(getproxy, listproxy)
    df = pandas.DataFrame({'ip': listip, 'port': listport})

    df.to_csv('./data/proxys.csv', index=False)