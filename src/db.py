import asyncio
import re
import uuid

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pydantic import BaseModel
from pymongo import UpdateOne

from src.constants import FAKE_USER_PASSWORD
from src.models import User, ShoppingList, ShoppingItem

client = AsyncIOMotorClient("mongodb://localhost:27017")
client.get_io_loop = asyncio.get_event_loop

shopping_lists = client["shopito"]["shopping_lists"]
shopping_items = client["shopito"]["shopping_items"]
users = client["shopito"]["users"]

async def get_user_by_username(username: str) -> User | None:
    user_doc = await users.find_one({"username": re.compile(username, re.IGNORECASE)})
    if not user_doc:
        return None
    return User(**user_doc)


async def register_user(username: str, password_hash: str):
    await users.insert_one({
        "id": str(uuid.uuid4()),
        "username": username,
        "password_hash": password_hash
    })


async def seed_database():
    if await users.count_documents({}) == 0:
        await register_user(username="KrazyManJ", password_hash=FAKE_USER_PASSWORD)


async def ensure_indexes():
    await shopping_lists.create_index([("owner_id", 1), ("updated_at", 1)])
    await shopping_items.create_index([("owner_id", 1), ("updated_at", 1)])

    await shopping_lists.create_index("id", unique=True)
    await shopping_items.create_index("id", unique=True)


async def _upsert_documents(
        collection: AsyncIOMotorCollection,
        documents: list[BaseModel],
        user_id: str
):
    if not documents:
        return

    operations = []

    for doc in documents:
        doc_data = doc.model_dump()
        doc_data["owner_id"] = user_id

        op = UpdateOne(
            {
                "id": doc.id,
                "owner_id": user_id,
                "$or": [
                    {"updated_at": {"$lt": doc.updated_at}},
                    {"updated_at": {"$exists": False}}
                ]
            },
            {"$set": doc_data},
            upsert=True
        )
        operations.append(op)

    if operations:
        await collection.bulk_write(operations)

async def push_lists(user_id: str, lists: list[ShoppingList]):
    await _upsert_documents(shopping_lists, lists, user_id)

async def push_items(user_id: str, items: list[ShoppingItem]):
    await _upsert_documents(shopping_items, items, user_id)

async def _get_modified(
        collection: AsyncIOMotorCollection,
        user_id: str,
        last_sync_ts: int
) -> list[dict]:
    cursor = collection.find(
        {
            "owner_id": user_id,
            "updated_at": {"$gt": last_sync_ts}
        },
        projection={"_id": False}
    )
    return await cursor.to_list()


async def get_modified_lists(user_id: str, last_sync_ts: int) -> list[dict]:
    return await _get_modified(shopping_lists, user_id, last_sync_ts)


async def get_modified_items(user_id: str, last_sync_ts: int) -> list[dict]:
    return await _get_modified(shopping_items, user_id, last_sync_ts)

async def get_items_of_user(user_id: str) -> list[dict]:
    return await shopping_items.find({"owner_id": user_id}, projection={"_id": False}).to_list()

async def get_lists_of_user(user_id: str) -> list[dict]:
    return await shopping_lists.find({"owner_id": user_id}, projection={"_id": False}).to_list()