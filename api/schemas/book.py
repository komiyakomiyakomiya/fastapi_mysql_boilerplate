from typing import Union
from pydantic import BaseModel
# from uuid import UUID
# import schemas.user as user_schema


class BookBase(BaseModel):
    class Config:
        orm_mode = True


class BookResponse(BookBase):
    id: int
    title: str
    user_id: Union[int, None]


class BookCreate(BaseModel):
    title: str
    user_id: Union[int, None] = None


class BookUpdate(BaseModel):
    title: str
    user_id: Union[int, None]