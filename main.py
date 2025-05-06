import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_shorten_link(url):
    load_dotenv()
    token_api_vk = os.getenv('TOKEN_API_VK')
    parsed = urlparse(url)
    url_netloc = (parsed.netloc)
    netloc = 'vk.cc'
    if url_netloc == netloc:
        try:
            click_count = count_clicks(token_api_vk, url)[
                'response']['stats'][0]['views']
        except KeyError:
            print("Ошибка, введите сокращенную ссылку корректно.")
            exit()
        return ("Всего по ссылке было сделано кликов:", click_count)
    else:
        try:
            short_url = shorten_link(token_api_vk, url)[
                'response']['short_url']
        except KeyError:
            print("Ошибка, введите ссылку.")
            exit()
        return ("Сокращенная ссылка:", short_url)


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
    return short_link


def count_clicks(token, short_url):
    url_vk = 'https://api.vk.ru/method/utils.getLinkStats'
    parsed = urlparse(short_url)
    key = parsed.path.lstrip('/')
    payload = {
        'access_token': token,
        'key': key,
        'interval': 'forever',
        'v': 5.199
    }
    response = requests.get(url_vk, params=payload)
    response.raise_for_status()
    clicks = response.json()
    return clicks


def main():
    url = input("Введите ссылку: ")
    check_url = is_shorten_link(url)
    print(check_url)


if __name__ == '__main__':
    main()
