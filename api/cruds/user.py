from typing import List
# from uuid import UUID
from tkinter.messagebox import NO
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
import models.user as user_model
import models.book as book_model
import schemas.user as user_schema


def create_user(user_body: user_schema.UserCreate,
                db: Session) -> user_model.User:
    """
    * 引数としてスキーマuser_bodyを受け取る
    * これをDBモデルであるuser_model.User に変換する
    * DBにコミットする
    * DB上のデータを元にUserインスタンス`item`を更新する（この場合、作成したレコードの id を取得する）
    * 作成したDBモデルを返却する
    """
    item = user_model.User(**user_body.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def read_users(db: Session) -> List[user_model.User]:
    items = db.query(user_model.User) \
        .filter(user_model.User.del_flg != 1) \
        .all()
    if len(items) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Records not found')
    return items


def read_user(user_id: int,
              db: Session) -> user_model.User:
    item = db.query(user_model.User).get(user_id)
    if item is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record not found')
    if item.del_flg == 1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record deleted')
    return item


def update_user(user_id: int,
                user_body: user_schema.UserUpdate,
                db: Session) -> user_model.User:
    original = db.query(user_model.User).get(user_id)
    if original is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record not found')
    if original.del_flg == 1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record deleted')
    original.username = user_body.username
    db.add(original)
    db.commit()
    db.refresh(original)
    return original


def delete_user(user_id: int,
                db: Session) -> user_model.User:
    """ 論理削除 """
    original = db.query(user_model.User).get(user_id)
    if original is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record not found')
    if original.del_flg == 1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record deleted')
    original.del_flg = 1

    # userに紐づく全てのbookのuser_idをnullにする 
    books = db.query(book_model.Book) \
                .filter(book_model.Book.user_id==user_id) \
                .all()
    for book in books:
        book.user_id = None
        db.add(book)

    db.add(original)
    db.commit()
    db.refresh(original)
    return original


# def delete_user(user_id: int, 
#                 db: Session) -> None:
#     """ 物理削除 """
#     item = db.query(user_model.User).get(user_id)
#     if item is None:raise HTTPException(status_code=HTTP_404_NOT_FOUND,
#                                         detail='Record not foudnd')
#     db.delete(item)
#     db.commit()
