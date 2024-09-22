import json
import pandas as pd
import re
import datetime
from typing import Optional

from src.main_page import data_frame_xlsx


def decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("../data/reports.json", "w", encoding="utf8") as file:
            file.write(result)
        return result

    return wrapper


@decorator
def spending_by_category(transactions: pd.DataFrame, category: str, user_date: Optional[str] = None) -> str:
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


if __name__ == "__main__":
    test_data = {
        'Дата операции': ['01.10.2023 12:00:00', '02.10.2023 13:00:00', '03.10.2023 14:00:00', '04.10.2023 15:00:00'],
        'Категория': ['Продукты', 'Транспорт', 'Развлечения', 'Продукты'],
        'Сумма операции': [100.00, 200.00, 300.00, 400.00],
    }
    df = pd.DataFrame(test_data)
    print(df)
    category = "транспорт"
    data = '01.11.2023'

    result = spending_by_category(df, category, data)
    print(result)