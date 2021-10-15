# Парсинг сайта криптовалют с табличными данными с помощью Selenium.
# Т.к данные подгружаются только при просмотре страницы, используем END, PAGE_DOWN.
# В случае парсинга через requests, html не загружается полностью и парсинг прекращается.

from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

index = 1


def get_html(url):
    time.sleep(1)  # Время задержки между запросами.
    driver = webdriver.Chrome()
    driver.get(url)
    body = driver.find_element_by_css_selector('body')
    body.click()
    for _ in range(10):
        body.send_keys(Keys.PAGE_DOWN)  # Перелистываем страницу для подгрузки.
    body.send_keys(Keys.END)
    time.sleep(10)  # Время на подгрузку страницы.
    html = driver.page_source

    return html


def write_csv(data):  # Запись данных в файл.
    with open('coins.csv', 'a') as f:
        writer = csv.writer(f)

        writer.writerow([data['name'],
                         data['symbol'],
                         data['url'],
                         data['price']])


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')  # Экземпляр класса
    trs = soup.find("div", {"class": "h7vnx2-1 bFzXgL"}).find('tbody').find_all('tr')

    for tr in trs:  # Находим все нужные элементы.
        global index
        tds = tr.find_all('td')
        try:
            name = tds[2].find('div', {'class': 'sc-16r8icm-0 escjiH'}).find("div", {
                "class": "sc-16r8icm-0 sc-1teo54s-1 dNOTPP"}).find('p').text
        except:
            name = ''
        try:
            symbol = tds[2].find('p', class_='sc-1eb5slv-0 gGIpIK coin-item-symbol').text
        except:
            symbol = ''
        try:
            url = 'https://coinmarketcap.com' + tds[3].find('a').get('href')
        except:
            url = ''
        try:
            price = tds[3].find('div', {"class": "sc-131di3y-0 cLgOOr"}).find('a').text
        except:
            price = ''  # В случае отсутствия информации.
        index += 1
        print(index, name, symbol, price)

        data = {
            'name': name,
            'symbol': symbol,
            'url': url,
            'price': price}

        write_csv(data)


def main():
    for i in range(1, 4):  # возьмем первые страницы.
        url = f"https://coinmarketcap.com/?page={str(i)}"
        get_page_data(get_html(url))


if __name__ == '__main__':
    main()
