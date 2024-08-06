import requests
import yaml
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor

with open('./config/config.yml', 'r') as f:
    config = yaml.safe_load(f)

def getData(urlbonban):
    response = requests.get(url=urlbonban)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_results = soup.find_all('li', class_=['car-item row1','car-item row2'])
    for result in all_results:
        data = {}
        data["name"] = result.find('h3').text
        data["year"] = result.find('div', class_='cb1').find('b').text
        data["price"] = result.find('div', class_='cb3').text
        data["description"] = result.find('div', attrs={'itemprop':'description'}).text
        data["urlcar"] = "https://bonbanh.com/"+result.find('a',attrs={'itemprop':'url'}).get('href')
        print(json.dumps(data, ensure_ascii=False, indent=2))

def main():
    urlbonban = config['url']['urlbonbanh']
    listUrl = [urlbonban.format(i) for i in range(1, 1000)]

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(getData, listUrl)

if __name__ == '__main__':
    main()

