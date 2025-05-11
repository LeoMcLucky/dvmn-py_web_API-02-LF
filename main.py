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
    short_link = response.json()
    return short_link['response']['short_url']


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
    counted_clicks = response.json()
    return counted_clicks['response']['stats'][0]['views']


def main():
    load_dotenv()
    api_vk_token = os.getenv('API_VK_TOKEN')
    url = input("Введите ссылку: ")
    if is_shorten_link(api_vk_token, url):
        try:
            click_count = count_clicks(api_vk_token, url)
            print("Всего по ссылке было сделано кликов:", click_count)
        except KeyError:
            print("Ошибка, введите сокращенную ссылку корректно.")
    else:
        try:
            short_url = shorten_link(api_vk_token, url)
            print("Сокращенная ссылка:", short_url)
        except KeyError:
            print("Ошибка, введите ссылку.")


if __name__ == '__main__':
    main()
