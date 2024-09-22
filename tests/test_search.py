import pandas as pd

from src.search import sorting_transactions


def test_sorting_transactions_with_valid_data():
    """Проверяет, что функция возвращает правильный список транзакций для валидных данных."""
    test_data = {
        "Категория": ["Продукты", "Транспорт", "Развлечения", "Продукты"],
        "Сумма операции": [100.00, 200.00, 300.00, 400.00],
    }
    df = pd.DataFrame(test_data)
    search_bar_user = "продукты"
    expected_result = [
        {"Категория": "Продукты", "Сумма операции": 100.00},
        {"Категория": "Продукты", "Сумма операции": 400.00},
    ]

    result = sorting_transactions(df, search_bar_user)
    assert result == expected_result


def test_sorting_transactions_with_no_matching_data():
    """Проверяет, что функция возвращает правильное сообщение, если нет совпадений."""
    test_data = {
        "Категория": ["Продукты", "Транспорт", "Развлечения", "Продукты"],
        "Сумма операции": [100.00, 200.00, 300.00, 400.00],
    }
    df = pd.DataFrame(test_data)
    search_bar_user = "Кино"
    expected_result = "Транзакций с названием Кино нет"

    result = sorting_transactions(df, search_bar_user)
    assert result == expected_result
