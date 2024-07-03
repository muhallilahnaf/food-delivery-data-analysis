import json
import requests
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9"
}

def save(data):
    global ROOT_DIR
    folder_path = os.path.join(ROOT_DIR, 'data')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, 'restaurant_data.json')
    with open(file_path, 'w') as f:
        json.dump(data, f)
        print('saved')


def read():
    global ROOT_DIR
    file_path = os.path.join(ROOT_DIR, 'data', 'restaurant_data.json')
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except:
        data = dict()
    return data


def get_rest_list():
    global ROOT_DIR
    file_path = os.path.join(ROOT_DIR, 'data', 'restaurant_list.json')
    try:
        with open(file_path, 'r') as f:
            rest = json.load(f)
            return rest.keys()
    except:
        return []


def main():
    data = read()
    saved_rest = data.keys()
    
    restaurants = get_rest_list()
    total = len(restaurants)
    remaining = total - len(saved_rest)

    api_url = os.environ.get('API_RESTAURANT')

    for restaurant in restaurants:
        if restaurant not in saved_rest:
            print('remaining=', remaining)
            print('fetching restaurant data of', restaurant)
            sleep(3)
            res = requests.get(api_url.replace('rest_code', restaurant), headers=headers)
            # print(res)
            if res.ok:
                resdata = res.json()
                data[restaurant] = resdata
                save(data)
                print(restaurant, 'fetched')
                remaining = remaining - 1


main()
