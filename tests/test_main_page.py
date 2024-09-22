from unittest.mock import patch, Mock
import pandas as pd
import unittest
import datetime
import pytest
from src.main_page import greeting_user_input, get_card_details, top_five_transaction, exchange_rate, stocks_from_the_SP500


def test_greeting_user_input_morning():
    """Тест для утреннего приветствия"""
    date = "2023-10-26 07:30:00"
    assert greeting_user_input(date) == "Доброе утро"

def test_greeting_user_input_afternoon():
    """Тест для дневного приветствия"""
    date = "2023-10-26 14:00:00"
    assert greeting_user_input(date) == "Добрый день"

def test_greeting_user_input_evening():
    """Тест для вечернего приветствия"""
    date = "2023-10-26 19:15:00"
    assert greeting_user_input(date) == "Добрый вечер"

def test_greeting_user_input_night():
    """Тест для ночного приветствия"""
    date = "2023-10-26 01:00:00"
    assert greeting_user_input(date) == "Доброй ночи"


def test_get_card_details_with_valid_data():
    """Проверяет, что функция правильно обрабатывает валидные данные."""
    test_data = {
        'Номер карты': ['1234567890123456', '1234567890123456', '9876543210123456'],
        'Статус': ['OK', 'OK', 'Error'],
        'Сумма операции': [-100.00, -200.00, -300.00],
    }
    df = pd.DataFrame(test_data)

    result = get_card_details(df)
    assert result == [{'cashback': -3.0, 'last_digits': '3456', 'total_spending': -300.0}]

def test_get_card_details_with_empty_data():
    """Проверяет, что функция возвращает пустой список для пустых данных."""
    df = pd.DataFrame(columns=['Номер карты', 'Статус', 'Сумма операции'])
    assert get_card_details(df) == []


def test_top_five_transaction_with_valid_data():
    """Проверяет, что функция возвращает топ-5 транзакций для валидных данных."""
    test_data = {
        'Дата платежа': ['2023-10-26', '2023-10-25', '2023-10-24', '2023-10-23', '2023-10-22', '2023-10-21'],
        'Сумма операции': [100.00, 200.00, 300.00, 400.00, 500.00, 600.00],
        'Сумма платежа': [100.00, 200.00, 300.00, 400.00, 500.00, 600.00],
        'Категория': ['Продукты', 'Транспорт', 'Развлечения', 'Одежда', 'Еда', 'Прочее'],
        'Описание': ['Покупка продуктов', 'Проезд на метро', 'Билеты в кино', 'Новая куртка', 'Обед в кафе', 'Перевод другу'],
    }
    df = pd.DataFrame(test_data)

    result = top_five_transaction(df)
    assert result == [
        {
         'amount': 100.0,
         'category': 'Продукты',
         'data': '2023-10-26',
         'description': 'Покупка продуктов',
        },
        {
        'amount': 200.0,
        'category': 'Транспорт',
        'data': '2023-10-25',
        'description': 'Проезд на метро',
        },
        {
         'amount': 300.0,
         'category': 'Развлечения',
         'data': '2023-10-24',
         'description': 'Билеты в кино',
        },
        {
         'amount': 400.0,
         'category': 'Одежда',
         'data': '2023-10-23',
         'description': 'Новая куртка',
        },
        {
         'amount': 500.0,
         'category': 'Еда',
         'data': '2023-10-22',
         'description': 'Обед в кафе',
         },
    ]


def test_exchange_rate_with_valid_currencies():
    """Проверяет, что функция возвращает правильный курс для USD и EUR."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "exchange_rates": {"RUB": 75.00, "USD": 1.00, "EUR": 0.90}
    }

    with patch('requests.get', Mock(return_value=mock_response)):
        result = exchange_rate(['USD', 'EUR'])
        assert result == [
            {'currency': 'USD', 'rate': 75.00},
            {'currency': 'EUR', 'rate': 75.00},
        ]


def test_stocks_from_the_SP500_with_valid_stocks():
    """Проверяет, что функция возвращает правильные цены для валидных акций."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [{"low": 100.00}]
    }
    user_stocks = ["AAPL", "MSFT"]

    with patch('requests.get', Mock(return_value=mock_response)):
        result = stocks_from_the_SP500(user_stocks)
        assert result == [
            {'stock': 'AAPL', 'prise': 100.00},
            {'stock': 'MSFT', 'prise': 100.00},
        ]