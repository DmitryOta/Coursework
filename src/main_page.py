import datetime
import logging
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


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("main_page_log")


def reading_financial_transactions_xl(WEY_TO_FILE_XL: str) -> pd.DataFrame:
    """Функция считывает финансовые операции из xlsx файла и фозвращает список словарей с транзакциями"""
    logger.info("Переводим excel файл в dataFrame")
    df = pd.read_excel(WEY_TO_FILE_XL)
    return df


data_frame_xlsx = reading_financial_transactions_xl(WEY_TO_FILE_XL)


def greeting_user() -> str:
    """Функция выводит приветствие в зависимости от времени суток"""
    logger.info("Получаем актуальные дату и время")
    time = datetime.datetime.now()
    logger.info("Достаем из полученной даты часы")
    hour = time.hour
    logger.info("Сверям полученное значение")
    if 5 <= hour < 12:
        greeting = "Доброе утро"
    elif 12 <= hour < 17:
        greeting = "Добрый день"
    elif 17 <= hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"
    logger.info("Возвращаем приветствие")
    return greeting


def greeting_user_input(date: str) -> str:
    """Функция выводит приветствие в зависимости от переданной даты"""
    logger.info("Переводим полученную дату в формат datetime")
    dt = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    logger.info("Достаем из полученной даты часы")
    dt_hour = dt.hour
    logger.info("Сверям полученное значение")
    if 5 <= dt_hour < 12:
        greeting = "Доброе утро"
    elif 12 <= dt_hour < 17:
        greeting = "Добрый день"
    elif 17 <= dt_hour < 22:
        greeting = "Добрый вечер"
    else:
        greeting = "Доброй ночи"
        logger.info("Возвращаем приветствие")
    return greeting


def get_card_details(transaction: pd.DataFrame) -> list[dict]:
    """Функция сортирует операции и выводит каждой карте:
    последние 4 цифры карты;
    общая сумма расходов;
    кешбэк (1 рубль на каждые 100 рублей)"""
    logger.info("Сортируем dataFrame по статусу операции и сумме операции")
    sort = transaction.loc[(data_frame_xlsx["Статус"] == "OK") & (data_frame_xlsx["Сумма операции"] < 0)]
    logger.info("Групперуем по номерам карт и складываем суммы всех операций в каждой группе")
    filter_cards = sort.groupby("Номер карты")["Сумма операции"].sum()
    logger.info("Переводим отсортированный и сгрупированный dataFrame в словарь")
    dict_filter = filter_cards.to_dict()

    card_data = []
    logger.info("Записываем в список наши словари предварительно вычеслив кешбэк")
    for key, velue in dict_filter.items():
        if key not in card_data:
            last_digits = key
            total_spending = velue
            cashback = round(velue / 100, 2)

            card_data.append(
                {"last_digits": last_digits[-4:], "total_spending": round(total_spending, 3), "cashback": cashback}
            )
    logger.info("Возвращаем список словарей")
    return card_data


def top_five_transaction(transaction: pd.DataFrame) -> list[dict]:
    """Функция выводит топ-5 транзакций"""
    top_five = []
    logger.info("Сортируем dataFrame по сумме операции")
    sorted_by_price_desc = transaction.sort_values(by="Сумма операции", ignore_index=True).head()
    logger.info("Переводим отсорированый dataFrame в словарь")
    sorted_five_transaction = sorted_by_price_desc.to_dict(orient="records")
    logger.info("Достаем нужные значения из словаря")
    for key in sorted_five_transaction:
        top = {}
        top["data"] = key["Дата платежа"]
        top["amount"] = key["Сумма платежа"]
        top["category"] = key["Категория"]
        top["description"] = key["Описание"]
        top_five.append(top)
    logger.info("Возвращаем топ 5 транзакций")
    return top_five


def exchange_rate(list_currencies: list) -> list[dict]:
    """Функция возвращает курс USD и EUR к RUB"""
    currency = []
    url = "https://exchange-rates.abstractapi.com/v1/live/"
    logger.info("Достаем каждое значени из переданного списка и оправляем запрос на API сервис")
    for i in list_currencies:
        base = f"&base={i}"
        response = requests.get(f"{url}{api_key}{base}")
        status_code = response.status_code
        result = response.json()
        sleep(1)
        logger.info("Проверяем код ответа")
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
            logger.info("Возвращаем сообщение об ошибке")
            print("Произошла ошибка")
    logger.info("Возвращаем список словарей с конвертированными валютами")
    return currency


def stocks_from_the_SP500(user_stocks: list) -> list[dict]:
    """Функция возвращает топ 5 акций S&P 500"""
    stocks_price = []
    logger.info("Достаем каждое значени из переданного списка и оправляем запрос на API сервис")
    for i in user_stocks:
        api_url = f"https://api.marketstack.com/v1/intraday?access_key={KEY_API_SP500}&symbols={i}"
        response = requests.get(api_url)
        prices = response.json()
        price = prices["data"][0]["low"]
        stocks_price.append({"stock": i, "prise": price})
    logger.info("Возвращаем список словарей с 5-ю акциями компаний")
    return stocks_price
