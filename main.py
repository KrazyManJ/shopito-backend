import time
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends

from src import db
from src.models import SyncRequest, User, SyncResponse, ShoppingList, ShoppingItem
from src.routes import api_utils, auth
from src.validation import get_current_user


@asynccontextmanager
async def lifespan(_: FastAPI):
    await db.ensure_indexes()
    await db.seed_database()
    yield


app = FastAPI(
    title="Shopito API",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
)

app.include_router(api_utils.router)

app.include_router(auth.router)


@app.post("/sync")
async def sync(
        payload: SyncRequest,
        user: Annotated[User, Depends(get_current_user)]
):
    # 1. PUSH
    await db.push_lists(user.id, payload.lists)
    await db.push_items(user.id, payload.items)

    # 2. PULL
    new_lists = await db.get_modified_lists(user.id, payload.last_sync_timestamp)
    new_items = await db.get_modified_items(user.id, payload.last_sync_timestamp)

    # disable inspection, because FastAPI will handle conversion
    # noinspection PyTypeChecker
    return SyncResponse(
        new_sync_timestamp=int(time.time() * 1000),
        lists=new_lists,
        items=new_items
    )



@app.get("/items")
async def get_items(
        user: Annotated[User, Depends(get_current_user)]
) -> list[ShoppingItem]:
    # noinspection PyTypeChecker
    return await db.get_items_of_user(user.id)

@app.get("/lists")
async def get_lists(
        user: Annotated[User, Depends(get_current_user)]
) -> list[ShoppingList]:
    # noinspection PyTypeChecker
    return await db.get_lists_of_user(user.id)