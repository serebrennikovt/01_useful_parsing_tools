# Парсинг сайта free-proxy-list.net для сбора Proxy, для парсинга.
# http://httpbin.org/ip - проверка текущего ip адреса.
# Для парсинга сайта с https/http, нужны соответствующие proxy.

import requests
from bs4 import BeautifulSoup
from random import choice


def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')
    proxies = []  # Пустой список для proxy.
    trs = soup.find('table', {'class': 'table table-striped table-bordered'}).find_all('tr')[
          1:21]  # Возьмем первый 20 proxy

    for tr in trs:
        tds = tr.find_all('td')
        if 'no' in tds[6].text.strip():  # Собираем http proxy
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            schema = 'http:'
            proxy = {'schema': schema, 'address': "http://" + ip + ':' + port}
            proxies.append(proxy)
    return choice(proxies)  # случайный элемент из списка proxies.


def get_html(url):  # Нужно передать в качестве аргумента proxy.
    p = get_proxy()  # {'schema': 'https', 'address': '64.124.38.141:8080'} словарь с ключами.
    proxy = {p['schema']: p['address']}  # создадим нужный нам словарь.
    print(proxy)
    r = requests.get(url, proxies=proxy, timeout=5)  # Таймаут 5 сек, в случае, если сервер не отвечает.
    return r.text


def main():
    url = 'http://httpbin.org/ip'
    print(get_html(url))  # текущий ip адрес


if __name__ == "__main__":
    main()
