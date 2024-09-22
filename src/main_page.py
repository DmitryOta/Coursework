import datetime
import json
import os
from time import sleep

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
KEY_API = os.getenv("KEY_API_EXCHANGE_RATE")
api_key = f"?api_key={KEY_API}"

KEY_API_SP500 = os.getenv("KEY_API_S&P_500")


WEY_TO_FILE_XL = os.path.join(os.path.dirname(__file__), "../data/operations.xlsx")


def reading_financial_transactions_xl(WEY_TO_FILE_XL: str) -> pd.DataFrame:
    """Функция считывает финансовые операции из xlsx файла и фозвращает список словарей с транзакциями"""
    df = pd.read_excel(WEY_TO_FILE_XL)

    return df


data_frame_xlsx = reading_financial_transactions_xl(WEY_TO_FILE_XL)


def real_time() -> int:
    """Функция возвращает настоящее время в часах"""
    hour = datetime.datetime.now().hour
    return hour


hour = real_time()


def greeting_user(hour: int) -> str:
    """Функция выводит приветствие в зависимости от времени суток"""
    if 5 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 17:
        greeting = "Добрый день"
    elif 17 <= hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"
    return greeting


def greeting_user_input(date: str) -> str:
    """Функция выводит приветствие в зависимости от переданной даты"""
    dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    dt_hour = dt.hour
    if 5 <= dt_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= dt_hour < 17:
        greeting = "Добрый день"
    elif 17 <= dt_hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"
    return greeting


def get_card_details(data_frame_xlsx: pd.DataFrame) -> list[dict]:
    """Функция сортирует операции и выводит каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)"""
    sort = data_frame_xlsx.loc[(data_frame_xlsx["Статус"] == "OK") & (data_frame_xlsx["Сумма операции"] < 0)]
    filter_cards = sort.groupby("Номер карты")["Сумма операции"].sum()
    dict_filter = filter_cards.to_dict()

    card_data = []
    for key, velue in dict_filter.items():
        if key not in card_data:
            last_digits = key
            total_spending = velue
            cashback = round(velue / 100, 2)

            card_data.append(
                {"last_digits": last_digits[-4:], "total_spending": round(total_spending, 3), "cashback": cashback}
            )
    return card_data


def top_five_transaction(data_frame_xlsx: pd.DataFrame) -> list[dict]:
    """Функция выводит топ-5 транзакций"""
    top_five = []
    sorted_by_price_desc = data_frame_xlsx.sort_values(by="Сумма операции", ignore_index=True).head()
    sorted_five_transaction = sorted_by_price_desc.to_dict(orient="records")
    for key in sorted_five_transaction:
        top = {}
        top["data"] = key["Дата платежа"]
        top["amount"] = key["Сумма платежа"]
        top["category"] = key["Категория"]
        top["description"] = key["Описание"]
        top_five.append(top)
    return top_five


def exchange_rate() -> list[dict]:
    """Функция аозвращает курс USD и EUR к RUB"""
    currency = []
    with open("../data/user_settings.json") as f:
        stock = json.load(f)

    USER_CURRENCIES = stock["user_currencies"]
    url = "https://exchange-rates.abstractapi.com/v1/live/"
    for i in USER_CURRENCIES:
        base = f"&base={i}"
        response = requests.get(f"{url}{api_key}{base}")
        status_code = response.status_code
        result = response.json()
        sleep(1)

        if status_code == 200:
            exchange_rates = result["exchange_rates"]
            for key, velue in exchange_rates.items():
                dict_currensy = {}
                if key == "RUB":
                    dict_currensy["currency"] = i
                    dict_currensy["rate"] = round(velue, 2)
                else:
                    continue
                currency.append(dict_currensy)
        else:
            print("Произошла ошибка")
    return currency


def stocks_from_the_SP500() -> list[dict]:
    """Функция возвращает топ 5 акций S&P 500"""
    stocks_price = []
    with open("../data/user_settings.json") as f:
        stock = json.load(f)

    USER_STOCKS = stock["user_stocks"]
    for i in USER_STOCKS:
        api_url = f"https://api.marketstack.com/v1/intraday?access_key={KEY_API_SP500}&symbols={i}"
        response = requests.get(api_url)
        prices = response.json()
        price = prices["data"][0]["low"]
        stocks_price.append({"stock": i, "prise": price})

    return stocks_price
