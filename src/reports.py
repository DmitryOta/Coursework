import json
import pandas as pd
import re
import datetime
from typing import Optional

from src.main_page import data_frame_xlsx

wey_to_file = "../data/reports.json"
def decorator_wey_to_file(wey_to_file: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(wey_to_file, "w", encoding="utf8") as file:
                json.dumps(result, file, indent=4, ensure_ascii=False)
            return result
        return wrapper
    return decorator


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         user_date: Optional[str] = None) -> str:
    transactions["Категория"] = transactions["Категория"].fillna("Нет категории")
    transactions["Дата платежа"] = transactions["Дата платежа"].fillna("Нет даты")
    dict_filter = transactions.to_dict(orient="records")
    pattern = re.compile(category, flags=re.IGNORECASE)
    if not user_date:
        user_date = datetime.datetime.today().date()
        for key in dict_filter:
            if key["Дата платежа"] and datetime.datetime.strptime(key["Дата платежа"], "%d-%m-%Y") < user_date:
                print(key)



    return user_date


if __name__ == "__main__":
    category = "Красота"
    user_date = datetime.datetime.today().date()
    user_date_2 = datetime.datetime.now().date()
    result = spending_by_category(data_frame_xlsx,category)
    print(result)
    print(user_date)
    print(user_date_2)
    data = "11-05-2023"
    user_date = datetime.datetime.strptime(data, "%d-%m-%Y")
    print(user_date)
    first_day = user_date - datetime.timedelta(weeks=13, days=1)
    print(first_day)

    # category = "Красота"
    # result = spending_by_category(data_frame_xlsx, category)
    # print(result)
