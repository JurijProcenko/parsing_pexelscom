# I study and optimize script "pythontoday/scrap_pexels" from GitHub
# This is parser images from pexels.com
# in lines 29-30, the code is optimized so that extra parameters '&page=''
# do not accumulate in the url

import requests
import time
import random
import os
from tqdm import tqdm
import math


def parse_pexelscom(query=''):
    authorization_pair = {'Authorization': f'{os.getenv("pexel_token")}'}
    query_line = f'https://api.pexels.com/v1/search?query={query}&per_page=80&orientation=landscape'
    response = requests.get(url=query_line, headers=authorization_pair)
    if response.status_code != 200:
        print(f'ERROR! Error. error...{response.status_code}, {response.json()}')
    imgs_dir_path = '_'.join(s for s in query.split(' ') if s.isalnum())
    if not os.path.exists(imgs_dir_path):
        os.makedirs(imgs_dir_path)
    json_data = response.json()

    images_count = json_data.get('total_results')
    if not json_data.get('next_page'):
        img_urls = [item.get('src').get('original') for item in json_data.get('photos')]
        save_images(img_list=img_urls, imgs_dir_path=imgs_dir_path)
    else:
        print(f'[INFO] Images total: {images_count}. The process may take longer')
        images_list_urls = []
        for page in range(1, math.ceil(images_count/80)+1):
            query_str = f'{query_line}&page={page}'
            response = requests.get(url=query_str, headers=authorization_pair)
            json_data = response.json()
            img_urls = [item.get('src').get('original') for item in json_data.get('photos')]
            images_list_urls.extend(img_urls)
        save_images(img_list=images_list_urls, imgs_dir_path=imgs_dir_path)


def save_images(img_list=[], imgs_dir_path=''):
    for item_url in tqdm(img_list):
        time.sleep(random.randint(1, 10))
        response = requests.get(url=item_url)
        if response.status_code == 200:
            with open(f'./{imgs_dir_path}/{item_url.split("-")[-1]}', 'wb') as f:
                f.write(response.content)
        else:
            print('Something is wrong when downloading images')


def main():
    query = input('Enter one or more keywords for search images: ')
    parse_pexelscom(query=query)


if __name__ == '__main__':
    main()
