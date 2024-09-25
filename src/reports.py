import datetime
import json
import logging
import re
from typing import Any, Callable, Optional

import pandas as pd

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("reports_log")


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
    logger.info("Замена всех пустых категорий на значение нет категории")
    transactions["Категория"] = transactions["Категория"].fillna("Нет категории")
    logger.info("Перевод датафрейма в словарь")
    dict_filter = transactions.to_dict(orient="records")
    pattern = re.compile(category, flags=re.IGNORECASE)
    result = []
    logger.info("Проверяем передал ли пользователь дату")
    if not user_date:
        logger.info("Получаем сегодняшнюю дату")
        user_date = datetime.datetime.today().date()
        first_date = user_date - datetime.timedelta(days=30 * 3 + 2)
        logger.info("Сортируем транзакции за 3 месяца по настоящую дату")
        for key in dict_filter:
            if (
                pattern.search(key["Категория"])
                and first_date <= datetime.datetime.strptime(key["Дата операции"], "%d.%m.%Y %H:%M:%S") <= user_date
            ):
                result.append(key)
            else:
                continue
    elif user_date:
        logger.info("Переводим полученную строку с датой в формат datatime")
        user_date = datetime.datetime.strptime(user_date, "%d.%m.%Y")
        first_date = user_date - datetime.timedelta(days=30 * 3 + 2)
        logger.info("Сортируем транзакции за 3 месяца до переданной даты")
        for key in dict_filter:
            if (
                pattern.search(key["Категория"])
                and first_date <= datetime.datetime.strptime(key["Дата операции"], "%d.%m.%Y %H:%M:%S") <= user_date
            ):
                result.append(key)
            else:
                continue
    logger.info("Проверяем словарь с транзакциями на наличие транзакций")
    if not result:
        logger.info("Выводим сообщение так, как транзакций с переданными параметрами за 3 месяцы небыло")
        return "Транзакции не найдены"
    else:
        logger.info("Переводим список словарей в JSON формат и возвращаем результат")
        json_data = json.dumps(result, indent=4, ensure_ascii=False)
        return json_data


if __name__ == "__main__":
    test_data = {
        "Дата операции": ["01.10.2023 12:00:00", "02.10.2023 13:00:00", "03.10.2023 14:00:00", "04.10.2023 15:00:00"],
        "Категория": ["Продукты", "Транспорт", "Развлечения", "Продукты"],
        "Сумма операции": [100.00, 200.00, 300.00, 400.00],
    }
    df = pd.DataFrame(test_data)
    category = "Транспорт"
    data = "01.11.2023"
    print(spending_by_category(df, category, data))
