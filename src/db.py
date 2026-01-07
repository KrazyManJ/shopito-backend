from src.constants import FAKE_USER_PASSWORD
from src.models import User

DB_USERS = [
    User(username="KrazyManJ", password_hash=FAKE_USER_PASSWORD),
]

def get_user_by_username(username: str) -> User | None:
    return None if len(DB_USERS) == 0 else [user for user in DB_USERS if user.username.lower() == username.lower()][0]


def register_user(username: str, password_hash: str):
    DB_USERS.append(User(username=username, password_hash=password_hash))