import random
from datetime import date, timedelta


def calculate_iin_checksum(digits11: list[int]) -> int:
    """Официальный алгоритм вычисления 12-й контрольной цифры ИИН РК."""
    w1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    s1 = sum(d * w for d, w in zip(digits11, w1))
    remainder = s1 % 11

    if remainder < 10:
        return remainder

    # Второй весовой ряд, если остаток равен 10
    w2 = [3, 4, 5, 6, 7, 8, 9, 10, 11, 1, 2]
    s2 = sum(d * w for d, w in zip(digits11, w2))
    remainder2 = s2 % 11

    return remainder2 if remainder2 < 10 else 0


def generate_valid_kazakhstan_iin(birth_date: date, gender: str) -> str:
    """Генерация 100% валидного казахстанского ИИН для заданной даты и пола."""
    year_str = f"{birth_date.year % 100:02d}"
    month_str = f"{birth_date.month:02d}"
    day_str = f"{birth_date.day:02d}"

    # Определение 7-го разряда (пол и век)
    is_male = gender.upper() in ("M", "MALE", "МУЖ", "МУЖСКОЙ")
    if birth_date.year < 2000:
        century_gender = 3 if is_male else 4  # XX век (1900-1999)
    else:
        century_gender = 5 if is_male else 6  # XXI век (2000-2099)

    order_num = f"{random.randint(1, 9999):04d}"

    iin_prefix_str = f"{year_str}{month_str}{day_str}{century_gender}{order_num}"
    digits11 = [int(c) for c in iin_prefix_str]

    checksum = calculate_iin_checksum(digits11)
    return f"{iin_prefix_str}{checksum}"