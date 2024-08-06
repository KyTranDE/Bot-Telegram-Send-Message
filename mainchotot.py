import requests
import yaml
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from Utils.postgres_tool import PostgresTool

with open('./config/config.yml', 'r') as f:
    config = yaml.safe_load(f)
    
def getData(urlchotot):
    response = requests.get(url=urlchotot)
    soup = BeautifulSoup(response.text, 'html.parser')
    all_results = soup.find_all('div', attrs={'tabindex':"0"})
    db_params = config['database']
    conn = PostgresTool(**db_params)
    for result in all_results:
        data = {}
        data["name"] = result.find('h3',class_="adonovt").text
        data["year"] = result.find('span', class_='c1u6gyxh').text
        data["price"] = result.find('span', class_='bfe6oav').text
        newRequest = requests.get("https://xe.chotot.com"+result.find('a',attrs={'itemprop':'item'}).get('href'))
        newSoup = BeautifulSoup(newRequest.text, 'html.parser')
        data["description"] = newSoup.find('p', attrs={'itemprop':'description'}).text
        data["urlcar"] = "https://xe.chotot.com"+result.find('a',attrs={'itemprop':'item'}).get('href')
        # print(data)
        conn.push_data("car", data)
    conn.close()

def main():

    urlchotot = config['url']['urlchotot']
    listUrl = [urlchotot.format(i) for i in range(1, 1000)]

    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(getData, listUrl)

if __name__ == '__main__':
    main()
