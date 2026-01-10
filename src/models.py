import uuid
from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str


class UserInfo(BaseModel):
    username: str


class User(UserInfo):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    password_hash: str


class RegisterForm(BaseModel):
    username: str
    password: str



class Location(BaseModel):
    latitude: float
    longitude: float


class ShoppingList(BaseModel):
    id: str
    name: str
    description: str = ""
    created_at: int
    updated_at: int
    is_deleted: bool


class ShoppingItem(BaseModel):
    id: str
    item_name: str
    amount: int
    is_done: bool
    buy_time: Optional[int] = None
    location: Optional[Location] = None
    list_id: str
    created_at: int
    updated_at: int
    is_deleted: bool


class SyncRequest(BaseModel):
    last_sync_timestamp: int
    lists: list[ShoppingList] = []
    items: list[ShoppingItem] = []


class SyncResponse(BaseModel):
    new_sync_timestamp: int
    lists: list[ShoppingList] = []
    items: list[ShoppingItem] = []