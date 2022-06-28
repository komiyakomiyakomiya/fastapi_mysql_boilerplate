from typing import List
# from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import cruds.book as book_crud
import schemas.book as book_schema

# prefix='/books'
router = APIRouter()


@router.get('/', response_model=List[book_schema.BookResponse])
async def read_books(db: Session = Depends(get_db)):
    return book_crud.read_books(db=db)


@router.get('/{book_id}/', response_model=book_schema.BookResponse)
async def read_book(book_id: int,
                    db: Session = Depends(get_db)):
    return book_crud.read_book(book_id=book_id,
                               db=db)


@router.post('/', response_model=book_schema.BookResponse)
async def create_book(book_body: book_schema.BookCreate,
                      db: Session = Depends(get_db)):
    return book_crud.create_book(book_body,
                                 db=db)


@router.put('/{book_id}/', response_model=book_schema.BookResponse)
async def update_book(book_id: int,
                      book_body: book_schema.BookUpdate,
                      db: Session = Depends(get_db)):
    return book_crud.update_book(book_id=book_id,
                                 book_body=book_body,
                                 db=db)


@router.delete('/{book_id}/', response_model=book_schema.BookResponse)
async def delete_book(book_id: int,
                      db: Session = Depends(get_db)):
    """ 論理削除 """
    return book_crud.delete_book(book_id=book_id,
                                 db=db)


# @router.delete('/{book_id}/', response_model=None)
# async def delete_book(book_id: int,
#                       db: Session = Depends(get_db)):
#     """ 物理削除 """
#     return book_crud.delete_book(book_id=book_id, db=db)
