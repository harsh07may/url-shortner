# app/codes.py
import secrets
import string

ALPHABET = string.ascii_letters + string.digits


def make_code(length: int = 6) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))