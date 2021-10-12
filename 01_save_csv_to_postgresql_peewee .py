# Запись файла csv в PostgreSQL с помощью библиотеки peewee.
# В качестве исходного файла использован файл парсинга сайта криптовалют.

import csv
from peewee import *

db = PostgresqlDatabase(database='test', user='postgres',  # Связь с базой данной.
                        password='1', host='localhost')


class Coin(Model):  # Наследование от класса Model
    name = CharField()  # Поля класса: колонки в таблице базы данных. CharField() - макс.длина 255 символов.
    url = TextField()
    price = CharField()

    class Meta:  # Связываем класс с базой данных.
        database = db


def main():
    db.connect()  # Соединение с базой данных.
    db.create_tables([Coin])  # Создание таблицы в базе данных.

    with open('cmc.csv') as f:  # Открытие csv файла, сохранение в переменную f. В качестве csv - парсинг сайта криптовалют.
        order = ['name', 'url', 'price']  # Список, указывающий порядок записи колонок из csv в ключи словаря.
        reader = csv.DictReader(f, fieldnames=order)  # Создаем читателя для файла f.

        coins = list(reader)  # Приводим к типу list.

        with db.atomic():  # Запись с помощью контекстного менеджера.

            for index in range(0, len(coins), 100):  # Запись частями по 100 шт. - для имеющегося массива данных.
                Coin.insert_many(coins[index: index + 100]).execute()


if __name__ == '__main__':
    main()

