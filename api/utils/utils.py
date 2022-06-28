import models.user as user_model
import models.book as book_model


user_objs = [
    user_model.User(
        username='Sousou',
        books=[
            book_model.Book(title='book1'),
            book_model.Book(title='book2'),
        ],
        del_flg=0
    ),
    user_model.User(
        username='Ryubi',
        books=[],
        del_flg=1
    ),
    user_model.User(
        username='Sonken',
        books=[],
        del_flg=0
    ),
]


def create_users(objs, db):
    db.add_all(objs)
    db.commit()


def create_user_by_username(usernames, db):
    users = [user_model.User(username=username) for username in usernames]
    db.add(users)
    db.commit()


def update_users_delflg_by_ids(ids, del_flg, db):
    users = db.query(user_model.User).filter(user_model.User.id.in_(ids)).all()
    for user in users:
        user.del_flg = del_flg
        db.add(user)
    db.commit()


def delete_users_by_usernames(usernames, db):
    db.query(user_model.User).filter(
        user_model.User.username.in_(usernames)).delete()
    db.commit()


def update_books_user_id_by_ids(ids, user_id, db):
    books = db.query(book_model.Book).filter(book_model.Book.id.in_(ids)).all()
    for book in books:
        book.user_id = user_id
        db.add(book)
    db.commit()
