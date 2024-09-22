from unittest.mock import mock_open, patch

import pandas as pd

from src.reports import decorator, spending_by_category


def test_decorator_writes_to_file():
    """Проверяет, что декоратор записывает результат в файл."""
    with patch("builtins.open", mock_open()) as mock_file:

        @decorator
        def my_function():
            return "Hello, world!"

        my_function()

        mock_file.assert_called_once_with("../data/reports.json", "w", encoding="utf8")
        mock_file.return_value.write.assert_called_once_with("Hello, world!")


def test_spending_by_category_with_valid_data_and_no_date():
    """Проверяет, что функция возвращает правильный результат для валидных данных c переданной датой."""
    test_data = {
        "Дата операции": ["01.10.2023 12:00:00", "02.10.2023 13:00:00", "03.10.2023 14:00:00", "04.10.2023 15:00:00"],
        "Категория": ["Продукты", "Транспорт", "Развлечения", "Продукты"],
        "Сумма операции": [100.00, 200.00, 300.00, 400.00],
    }
    df = pd.DataFrame(test_data)
    category = "Транспорт"
    data = "01.11.2023"

    result = spending_by_category(df, category, data)
    assert result == """[
    {
        "Дата операции": "02.10.2023 13:00:00",
        "Категория": "Транспорт",
        "Сумма операции": 200.0
    }
]"""
