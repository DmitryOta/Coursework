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
                and first_date <= datetime.datetime.strptime(key["Дата операции"], "%d.%m.%Y %H:%M:%S") < user_date
            ):
                result.append(key)
            else:
                continue
    elif user_date:
        user_date = datetime.datetime.strptime(user_date, "%d.%m.%Y")
        first_date = user_date - datetime.timedelta(days=30 * 3 + 2)
        for key in dict_filter:
            if (
                pattern.search(key["Категория"])
                and first_date <= datetime.datetime.strptime(key["Дата операции"], "%d.%m.%Y %H:%M:%S") < user_date
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
    # user_date = datetime.datetime.today().date()
    data = "11.09.2020"
    # user_date = datetime.datetime.strptime(data, "%d-%m-%Y")
    # mounth = user_date.month - 3
    # first_date = user_date - datetime.timedelta(days=30 * 3 + 2)
    # print(first_date)
    category = "красота"
    # user_date = datetime.datetime.today().date()
    # user_date_2 = datetime.datetime.now().date()
    result = spending_by_category(data_frame_xlsx, category, data)
    print(result)
    # print(user_date)
    # print(user_date_2)
    # data = "11-05-2023"
    # user_date = datetime.datetime.strptime(data, "%d-%m-%Y")
    # print(user_date)
    # first_day = user_date - datetime.timedelta(weeks=13, days=1)
    # print(first_day)

    # category = "Красота"
    # result = spending_by_category(data_frame_xlsx, category)
    # print(result)
