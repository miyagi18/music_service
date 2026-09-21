import json
from typing import Any


def load_json(filename: str) -> list[dict[str, Any]]:
    """Загружает данные из JSON-файла.

    Args:
        filename: Путь к файлу.

    Returns:
        Список словарей. Если файл не найден или повреждён, возвращает [].
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f'Файл {filename} не найден. Будет создан новый при сохранении.')
        return []
    except json.JSONDecodeError:
        print(f'Файл {filename} содержит некорректный JSON.')
        return []


def save_json(filename: str, data: list[dict[str, Any]]) -> None:
    """Сохраняет данные в JSON-файл.

    Args:
        filename: Путь к файлу.
        data: Список словарей для сохранения.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

