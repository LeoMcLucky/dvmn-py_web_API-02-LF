import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(token, url):
    link_short = True
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
    check_response = response.json()
    if 'error' in check_response:
        link_short = False
    return link_short


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
    clicks_counted = response.json()
    return clicks_counted['response']['stats'][0]['views']


def main():
    load_dotenv()
    token_api_vk = os.getenv('TOKEN_API_VK')
    url = input("Введите ссылку: ")
    check_url = is_shorten_link(token_api_vk, url)
    if check_url:
        try:
            click_count = count_clicks(token_api_vk, url)
            print("Всего по ссылке было сделано кликов:", click_count)
        except KeyError:
            print("Ошибка, введите сокращенную ссылку корректно.")
    else:
        try:
            short_url = shorten_link(token_api_vk, url)
            print("Сокращенная ссылка:", short_url)
        except KeyError:
            print("Ошибка, введите ссылку.")


if __name__ == '__main__':
    main()
