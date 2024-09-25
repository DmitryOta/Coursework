import json

from src.main_page import (
    data_frame_xlsx,
    exchange_rate,
    get_card_details,
    greeting_user,
    greeting_user_input,
    stocks_from_the_SP500,
)

with open("../data/user_settings.json") as f:
    stock = json.load(f)


USER_STOCKS = stock["user_stocks"]
USER_CURRENCIES = stock["user_currencies"]


def func_input_data() -> None:
    """Функция формирует JSON файл на основе собранных данных"""
    main_page = {}
    user_input = input("Введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    if user_input:
        greeting = greeting_user_input(user_input)
    else:
        greeting = greeting_user()
    main_page["greeting"] = greeting
    main_page["cards"] = get_card_details(data_frame_xlsx)
    main_page["currency_rates"] = exchange_rate(USER_CURRENCIES)
    main_page["stock_prices"] = stocks_from_the_SP500(USER_STOCKS)
    with open("../data/main_page.json", "w", encoding="UTF-8") as f:
        json.dump(main_page, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print(func_input_data())
