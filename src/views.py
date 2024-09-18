import json

from src.main_page import (data_frame_xlsx, exchange_rate, get_card_details, greeting_user, greeting_user_input,
                           real_time, stocks_from_the_SP500)


def func_input_data() -> None:
    main_page = {}
    user_input = input("Введите дату в формате ГГГГ-ММ-ДД ЧЧ:ММ:СС")
    if user_input:
        greeting = greeting_user_input(user_input)
    else:
        greeting = greeting_user(real_time())
    main_page["greeting"] = greeting
    main_page["cards"] = get_card_details(data_frame_xlsx)
    main_page["currency_rates"] = exchange_rate()
    main_page["stock_prices"] = stocks_from_the_SP500()
    with open("../data/main_page.json", "w", encoding="UTF-8") as f:
        json.dump(main_page, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    func_input_data()
