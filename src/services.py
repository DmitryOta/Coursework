import logging
import re

import pandas as pd

from src.main_page import data_frame_xlsx

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("services_log")


def sorting_transactions(data_frame_xlsx: pd.DataFrame, search_bar_user: str) -> list[dict] | str:
    """Функция принимает список словарей с данными о банковских операциях и строку поиска, а возвращает
    список словарей, у которых в описании есть данная строка"""
    logger.info("Замена всех пустых категорий на значение нет категории")
    data_frame_xlsx["Категория"] = data_frame_xlsx["Категория"].fillna("Нет категории")
    logger.info("Перевод датафрейма в словарь")
    dict_filter = data_frame_xlsx.to_dict(orient="records")
    pattern = re.compile(search_bar_user, flags=re.IGNORECASE)
    result = []
    logger.info('Проверяем есть ли переданная строка в словаре в значении "Категория"')
    for key in dict_filter:
        category = key["Категория"]
        if pattern.search(category):
            result.append(key)
        else:
            continue
    logger.info("Возвращаем список с вложенными словарями")
    if len(result) > 1:
        return result
    else:
        logger.info("Возвращаем пустой список так, как значения небыли найдены")
        return f"Транзакций с названием {search_bar_user} нет"


if __name__ == "__main__":
    print(sorting_transactions(data_frame_xlsx, "такси"))
