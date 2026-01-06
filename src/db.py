from dataclasses import dataclass

from src.constants import FAKE_USER_PASSWORD


@dataclass
class User:
    username: str
    password: str

DB_USERS = [
    User(username="KrazyManJ", password=FAKE_USER_PASSWORD),
]