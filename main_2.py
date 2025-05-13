import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(token, url):
    url_vk = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed_url = urlparse(url)
    key = parsed_url.path.lstrip('/')
    payload = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': 5.199
    }
    response = requests.get(url_vk, params=payload)
    response.raise_for_status()
    link_stats = response.json()
    return 'error' not in link_stats


def shorten_link(token, url):
    url_vk = 'https://api.vk.ru/method/utils.getShortLink'
    payload = {
        'access_token': token,
        'url': url,
        'v': 5.199
    }
    response = requests.get(url_vk, params=payload)
    response.raise_for_status()
    dict_short_link = response.json()
    return dict_short_link


def count_clicks(token, short_url):
    url_vk = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed_url = urlparse(short_url)
    key = parsed_url.path.lstrip('/')
    payload = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': 5.199
    }
    response = requests.get(url_vk, params=payload)
    response.raise_for_status()
    dict_counted_clicks = response.json()
    return dict_counted_clicks


def main():
    load_dotenv()
    api_vk_token = os.environ['API_VK_TOKEN']
    url = input("Введите ссылку: ")
    if is_shorten_link(api_vk_token, url):
        try:
            dict_click_count = count_clicks(api_vk_token, url)
            clicks = dict_click_count['response']['stats'][0]['views']
            print("Всего по ссылке было сделано кликов:", clicks)
        except KeyError:
            print("Ошибка, код ошибки:",
                  dict_click_count['error']['error_code'],
                  "Тип ошибки:",
                  dict_click_count['error']['error_msg'])
    else:
        try:
            dict_short_url = shorten_link(api_vk_token, url)
            short_url = dict_short_url['response']['short_url']
            print("Сокращенная ссылка:", short_url)
        except KeyError:
            print("Ошибка, код ошибки:",
                  dict_short_url['error']['error_code'],
                  "Тип ошибки:",
                  dict_short_url['error']['error_msg'])


if __name__ == '__main__':
    main()
