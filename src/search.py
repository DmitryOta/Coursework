import re

import pandas as pd

from src.main_page import data_frame_xlsx


def sorting_transactions(data_frame_xlsx: pd.DataFrame, search_bar_user: str) -> list[dict] | str:
    """Функция принимает список словарей с данными о банковских операциях и строку поиска, а возвращает
    список словарей, у которых в описании есть данная строка"""
    data_frame_xlsx["Категория"] = data_frame_xlsx["Категория"].fillna("Нет категории")
    dict_filter = data_frame_xlsx.to_dict(orient="records")
    pattern = re.compile(search_bar_user, flags=re.IGNORECASE)
    result = []
    for key in dict_filter:
        category = key["Категория"]
        print(type(category))
        if pattern.search(category):
            result.append(key)
        else:
            continue
    if len(result) > 1:
        return result
    else:
        return f"Транзакций с названием {search_bar_user} нет"


if __name__ == "__main__":
    print(sorting_transactions(data_frame_xlsx, "такси"))
