# from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND
import models.book as book_model
import schemas.book as book_schema


def create_book(book_body: book_schema.BookCreate,
                db: Session):
    item = book_model.Book(**book_body.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def read_books(db: Session):
    items = db.query(book_model.Book) \
        .filter(book_model.Book.del_flg != 1) \
        .all()
    if len(items) == 0:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Records not found')
    return items


def read_book(book_id: int,
              db: Session):
    item = db.query(book_model.Book).get(book_id)
    if item is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record not found')
    if item.del_flg == 1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record deleted')
    return item


def update_book(book_id: int,
                book_body: book_schema.BookUpdate,
                db: Session):
    original = db.query(book_model.Book).get(book_id)
    if original is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record not found')
    if original.del_flg == 1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record deleted')
    original.title = book_body.title
    original.user_id = book_body.user_id
    db.add(original)
    db.commit()
    db.refresh(original)
    return original


def delete_book(book_id: int,
                db: Session):
    """ 論理削除 """
    original = db.query(book_model.Book).get(book_id)
    if original is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record not found')
    if original.del_flg == 1:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,
                            detail='Record deleted')
    original.del_flg = 1
    db.add(original)
    db.commit()
    db.refresh(original)
    return original


# def delete_book(book_id: int,
#                 db: Session) -> None:
#     """ 物理削除 """
#     item = db.query(book_model.Book).get(book_id)
#     if item is None:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND,
#                             detail='Record not found')
#     db.delete(item)
#     db.commit()
