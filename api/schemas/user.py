from typing import List
from pydantic import BaseModel
# from uuid import UUID
import schemas.book as book_schema


class UserBase(BaseModel):
    class Config:
        orm_mode = True


class UserResponse(UserBase):
    id: int
    username: str
    del_flg: int
    books: List[book_schema.BookResponse]


class UserCreate(BaseModel):
    username: str


class UserUpdate(BaseModel):
    username: str