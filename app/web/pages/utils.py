from datetime import date
from typing import Literal

TIME = {
    "г": 365,
    "м": 30,
    "д": 1,
}
FORMS = {
    "г": ("год", "года", "лет"),
    "м": ("месяц", "месяца", "месяцев"),
    "д": ("день", "дня", "дней"),
}


def correct_date(number: int, key: Literal["г", "м", "д"]) -> str:
    if not number:
        return ""

    # Определяем форму по последним цифрам
    last_two = number % 100
    last_digit = number % 10

    if 11 <= last_two <= 14:
        form_index = 2  # лет/месяцев/дней
    else:
        if last_digit == 1:
            form_index = 0  # год/месяц/день
        elif 2 <= last_digit <= 4:
            form_index = 1  # года/месяца/дня
        else:
            form_index = 2  # лет/месяцев/дней

    return f"{number} {FORMS[key][form_index]} "


def days_to_str(days: int) -> str:
    """Реализует текстовое представление времени."""
    st = ""
    for key, value in TIME.items():
        delta = days // value
        days -= delta * value
        if st or delta:
            st += correct_date(delta, key)
    return st or "0 дней"


def days_since(date_: date) -> str:
    today = date.today()
    days = (date(year=today.year, month=today.month, day=today.day) - date_).days
    return days_to_str(days)
