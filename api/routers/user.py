from typing import List
# from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import cruds.user as user_crud
import schemas.user as user_schema

# prefix='/users',
router = APIRouter()


@router.post('/', response_model=user_schema.UserResponse)
async def create_user(user_body: user_schema.UserCreate,
                      db: Session = Depends(get_db)):
    return user_crud.create_user(user_body=user_body,
                                 db=db)


@router.get('/', response_model=List[user_schema.UserResponse])
async def read_users(db: Session = Depends(get_db)):
    return user_crud.read_users(db=db)


@router.get('/{user_id}/', response_model=user_schema.UserResponse)
async def read_user(user_id: int,
                    db: Session = Depends(get_db)):
    return user_crud.read_user(user_id=user_id,
                               db=db)


@router.put('/{user_id}/', response_model=user_schema.UserResponse)
async def update_user(user_id: int,
                      user_body: user_schema.UserUpdate,
                      db: Session = Depends(get_db)):
    return user_crud.update_user(user_id=user_id,
                                 user_body=user_body,
                                 db=db)


@router.delete('/{user_id}/', response_model=user_schema.UserResponse)
async def delete_user(user_id: int,
                      db: Session = Depends(get_db)):
    """ 論理削除 """
    return user_crud.delete_user(user_id=user_id,
                                 db=db)


# @router.delete('/{user_id}/', response_model=None)
# async def delete_user(user_id: int,
#                       db: Session = Depends(get_db)):
#     """ 物理削除 """
#     return user_crud.delete_user(user_id=user_id,
#                                  db=db)
