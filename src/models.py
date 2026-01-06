from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class UserInfo(BaseModel):
    username: str


class User(UserInfo):
    password_hash: str