# Мультипроцессорный парсинг сайта www.liveinternet.ru
# 02_ajax для ускорения предыдущего парсинга.

import requests
import csv
from multiprocessing import Pool
from time import sleep


def get_html(url):
    # sleep(1)  # задержа парсинга, защита от бана.
    r = requests.get(url)
    if r.ok:
        return r.text  # возврат html страницы, в случае положительного ответа.
    print(r.status_code)  # при отрицательном ответе - печать статуса ошибки.


def write_csv(data):  # Функция для записи в csv файл.
    with open('websites.csv', 'a') as f:  # Открытие csv файла, сохранение в переменную f.
        order = ['name', 'url', 'description', 'traffic',
                 'percent']  # Список, указывающий последовательность записи колонок из csv в ключи словаря.
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def make_all(url):
    text = get_html(url)
    get_page_data(text)


def get_page_data(text):
    data = text.strip().split('\n')[1:]  # Разбиваем строку на список, кроме первого элемента и пробелов.
    # print(repr(data))  # repr - возвращает строку с непечатуемыми символами.
    for row in data:
        # print(row)
        columns = row.strip().split('\t')  # Убираем табуляцию из каждой строки.
        name = columns[0]
        url = columns[1]
        description = columns[2]
        traffic = columns[3]
        percent = columns[4]

        # Запишем данные в csv файл.
        data = {'name': name,
                'url': url,
                'description': description,
                'traffic': traffic,
                'percent': percent}
        try:  # запись результата в файл, с возможным предупреждение ошибки.
            write_csv(data)
        except:
            print('ошибка записи')


def main():
    url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'
    urls = [url.format(str(i)) for i in range(1, 5000)]  # Список всех требуемых страниц.
    # print(urls)
    with Pool(20) as p:  # Cоздаем 20 процессов, сохраняем в переменную р.
        p.map(make_all, urls)


if __name__ == '__main__':
    main()
