import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


def clean_market_cap(mc_str):
    mc_str = mc_str.replace('₽', '').replace(' ', '').replace(',', '').strip()
    if mc_str.replace('.', '', 1).isdigit():
        return float(mc_str)
    return None


def write_cmc_top():
    url = 'https://coinmarketcap.com/ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    currencies = []
    for row in soup.find_all('tr')[1:101]:  # Берем только топ-100 криптовалют
        cols = row.find_all('td')
        if cols:
            name = cols[2].text.strip()
            mc = cols[3].text.strip()
            currencies.append({'name': name, 'mc': mc})

    total_market_cap = 0
    for currency in currencies:
        cleaned_mc = clean_market_cap(currency['mc'])
        if cleaned_mc is not None:
            total_market_cap += cleaned_mc

    # Подготовка данных для записи
    for currency in currencies:
        cleaned_mc = clean_market_cap(currency['mc'])
        if cleaned_mc is not None:
            currency['mp'] = f"{cleaned_mc / total_market_cap * 100:.2f}%" if total_market_cap else '0.00%'
        else:
            currency['mp'] = 'N/A'  # Если значение не удается преобразовать в число, помечаем как "N/A"

    now = datetime.datetime.now()
    filename = f"{now.hour}.{now.minute} {now.day}.{now.month}.{now.year}.csv"
    df = pd.DataFrame(currencies)
    df.to_csv(filename, sep=' ', index=False, header=['Name', 'MC', 'MP'])


# Вызов функции
write_cmc_top()
