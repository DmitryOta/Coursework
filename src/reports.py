import datetime
import json
import re
from typing import Optional, Any, Callable

import pandas as pd


def decorator(func: Callable) -> str:
    """Функция декоратор записывает результат работы функции в файл reports.json"""
    def wrapper(*args: Any, **kwargs: Any) -> Callable:
        result = func(*args, **kwargs)
        with open("../data/reports.json", "w", encoding="utf8") as file:
            file.write(result)
        return result

    return wrapper


def spending_by_category(transactions: pd.DataFrame, category: str, user_date: Optional[str] = None) -> str:
    """Функция возвращает отсортированый датафрейм в виде JSON файла"""
    transactions["Категория"] = transactions["Категория"].fillna("Нет категории")
    dict_filter = transactions.to_dict(orient="records")
    pattern = re.compile(category, flags=re.IGNORECASE)
    result = []
    if not user_date:
        user_date = datetime.datetime.today().date()
        first_date = user_date - datetime.timedelta(days=30 * 3 + 2)
        for key in dict_filter:
            if (
                pattern.search(key["Категория"])
                and first_date <= datetime.datetime.strptime(key["Дата операции"], "%d.%m.%Y %H:%M:%S") <= user_date
            ):
                result.append(key)
            else:
                continue
    elif user_date:
        user_date = datetime.datetime.strptime(user_date, "%d.%m.%Y")
        first_date = user_date - datetime.timedelta(days=30 * 3 + 2)
        for key in dict_filter:
            print(key)
            if (
                pattern.search(key["Категория"])
                and first_date <= datetime.datetime.strptime(key["Дата операции"], "%d.%m.%Y %H:%M:%S") <= user_date
            ):
                result.append(key)
            else:
                continue

    if not result:
        return "Транзакции не найдены"
    else:
        json_data = json.dumps(result, indent=4, ensure_ascii=False)
        return json_data
