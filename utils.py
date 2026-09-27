"""Вспомогательные функции безопасного ввода."""
from datetime import datetime


def input_int(prompt: str) -> int | None:
    """Безопасный ввод целого числа."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Ошибка: нужно ввести целое число.")
        return None


def input_date(prompt: str) -> str | None:
    """Безопасный ввод даты в формате YYYY-MM-DD."""
    value = input(prompt).strip()
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return value
    except ValueError:
        print("Ошибка: дата должна быть в формате YYYY-MM-DD.")
        return None
