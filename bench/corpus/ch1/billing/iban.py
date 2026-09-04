"""Нормализация IBAN: верхний регистр, без пробелов."""


def normalize_iban(raw: str) -> str:
    return raw.replace(" ", "").upper()
