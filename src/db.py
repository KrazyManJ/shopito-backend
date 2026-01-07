import asyncio
import re

from motor.motor_asyncio import AsyncIOMotorClient

from src.constants import FAKE_USER_PASSWORD
from src.models import User

client = AsyncIOMotorClient("mongodb://localhost:27017")
client.get_io_loop = asyncio.get_event_loop

# shopping_lists = client["shopito"]["shopping_lists"]
# shopping_items = client["shopito"]["shopping_items"]
users = client["shopito"]["users"]

async def get_user_by_username(username: str) -> User | None:
    user_doc = await users.find_one({"username": re.compile(username, re.IGNORECASE)})
    if not user_doc:
        return None
    return User(**user_doc)


async def register_user(username: str, password_hash: str):
    await users.insert_one({"username": username, "password_hash": password_hash})


async def seed_database():
    if await users.count_documents({}) == 0:
        await register_user(username="KrazyManJ", password_hash=FAKE_USER_PASSWORD)