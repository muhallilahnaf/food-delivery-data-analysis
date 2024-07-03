from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
import os
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))
gcount = 0
retry = 15

def get_driver():
    ff_options = webdriver.FirefoxOptions()
    ff_options.add_argument('--blink-settings=imagesEnabled=false')
    seleniumwire_options = {
        'disable_encoding': True
    }
    driver = webdriver.Firefox(seleniumwire_options=seleniumwire_options, options=ff_options)
    return driver


def get_rest_list(driver):
    selector = os.environ.get('CSS_SELECTOR')
    return driver.find_elements(By.CSS_SELECTOR, selector)


def save(data):
    global ROOT_DIR
    folder_path = os.path.join(ROOT_DIR, 'data')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, 'restaurant_list.json')
    with open(file_path, 'w') as f:
        json.dump(data, f)
        print('saved')


def read():
    global ROOT_DIR
    file_path = os.path.join(ROOT_DIR, 'data', 'restaurant_list.json')
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except:
        data = dict()
    return data


def check(driver):
    global retry
    retry = retry - 1
    if retry == 0:
        return True
    restaurants = get_rest_list(driver)
    q = len(restaurants)
    print('count=', q)
    return q > gcount


def process_rest(restaurants, data):
    count = len(restaurants)
    print('fetched=', count)
    saved_rest = data.keys()
    new_count = 0
    for restaurant in restaurants:
        href = restaurant.get_attribute('href')
        # print(href)
        name_index = href.rfind('/')
        if name_index != -1:
            rest_name = href[name_index+1:]
            rest_id = href[name_index-4: name_index]
            if rest_id not in saved_rest:
                new_count = new_count + 1
                data[rest_id] = rest_name
    print('new restaurant=', new_count)
    save(data)
    global gcount
    gcount = len(data.keys())


def get_url(city, lat, lng):
    url = os.environ.get('URL')
    url = url.replace('city/city', f'city/{city}').replace('lng=lng', f'lng={lng}').replace('lat=lat', f'lat={lat}')
    return url



def main():
    global retry
    try:
        retry = int(input('Enter no. of retries (default=15): '))
    except ValueError:
        pass

    city = 'dhaka'
    lat = '23.74622'
    lng = '90.3774'
    city = input(f'Enter city name (example={city}): ')
    lat = input(f'Enter latitude (example={lat}): ')
    lng = input(f'Enter longitude (example={lng}): ')

    driver = get_driver()
    url = get_url(city, lat, lng)
    driver.get(url)
    
    while (retry > 0):
        print('---next---')
        data = read()
        global gcount
        gcount = len(data.keys())
        restaurants = get_rest_list(driver)
        process_rest(restaurants, data)
        
        last_element = restaurants[-1]
        driver.execute_script("arguments[0].scrollIntoView();", last_element)
        
        retry = 15
        WebDriverWait(driver, 60).until(check)

    driver.quit()


main()

