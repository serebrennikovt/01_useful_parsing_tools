# Парсинг сайта, на которых используют ajax (обход стандартного URL адреса не позволяет производить парсинг)
# Во вкладке Network - вкладка XHR - отображение ajax запросов.
# Во вкладке Headers берем URL адрес для дальнейшего парсинга.
# С html получаем строку, обходимся без BeautifulSoup.

import requests
import csv


def get_html(url):
    r = requests.get(url)
    if r.ok:
        return r.text  # возврат html страницы, в случае положительного ответа.
    print(r.status_code)  # при отрицательном ответе - печать статуса ошибки.


def write_csv(data):  # Функция для записи в csv файл.
    with open('websites.csv', 'a') as f:  # Открытие csv файла, сохранение в переменную f.
        order = ['name', 'url', 'description', 'traffic',
                 'percent']  # Список, указывающий порядок записи колонок из csv в ключи словаря.
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def main():
    page = 1
    for i in range(0, 115):  # Диапазон требуемого количества страниц.
        url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'.format(str(i))
        response = get_html(url)  # Ответ сервера
        data = response.strip().split('\n')[1:]  # Разбиваем строку на список, кроме первого элемента и пробелов.
        # print(repr(data))  # repr - возвращает строку с непечатуемыми символами.

        for row in data:
            # print(row)
            columns = row.strip().split('\t')  # Убираем табуляцию из каждой строки.
            name = columns[0]
            url = columns[1]
            description = columns[2]
            traffic = columns[3]
            percent = columns[4]
            print(page, name, url, description, traffic, percent)  # Вывод результата парсинга на консоль.
            page += 1  # Нумерация для наглядности.

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


if __name__ == '__main__':
    main()
