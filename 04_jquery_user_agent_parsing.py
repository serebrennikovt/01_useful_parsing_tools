# Парсинг сайта, на котором используется User - Agent и не применима обычная пагинация страниц.
# Во вкладке Network - вкладка XHR - отображение ajax запросов.
# Во вкладке Headers берем URL адрес для дальнейшего парсинга.

import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    # user_agent получен из: Сеть - XHR - Заголовки.
    user_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36'}
    r = requests.get(url, headers=user_agent)
    if r.ok:
        return r.text  # возврат html страницы, в случае положительного ответа.
    print(r.status_code)


def write_csv(data):  # Функция для записи в csv файл.
    with open('testimonials.csv', 'a') as f:  # Открытие csv файла, сохранение в переменную f.
        order = ['author', 'since']  # Список, указывающий порядок записи колонок из csv в ключи словаря.
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_articles(html):
    soup = BeautifulSoup(html, 'lxml')  # lxml - тип парсера.
    ts = soup.find('div', {'class': 'module module-testimonial testimonial-2364-3-0-0 testimonial-container'}).find_all(
        'article')
    return ts  # [] or [a ,b ,c] возврат пустого списка в случае когда отзывы закончились.


def get_page_data(ts):
    for t in ts:  # Для каждого отзыва ищем:
        try:
            since = t.find('p', {'class': 'traxer-since'}).text.strip()  # Год отзыва.
        except:
            since = ''  # На случай, если не будет данных.
        try:
            author = t.find('p', {'class': 'testimonial-author'}).text.strip()  # Должность
        except:
            author = ''
        # print(since, author)
        data = {'author': author, 'since': since}
        write_csv(data)


def main():
    # 1. Получение контейнера с отзывами и списка отзывов.
    # 2. Если список есть, то парсим отзывы.
    # 3. Если список пустой - цикл прерывается.
    while True:
        page = 1  # Начальный номер страницы
        url = f'https://catertrax.com/why-catertrax/traxers/page/{str(page)}/?themify_builder_infinite_scroll=yes'

        articles = get_articles(get_html(url))  # [] or [a, b, a]
        if articles:
            get_page_data(articles)
            page += 1
        else:
            break


if __name__ == '__main__':
    main()
