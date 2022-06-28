from database import Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
# from sqlalchemy_utils import UUIDType
# from uuid import uuid4
from .mixins import Mixin


class User(Base, Mixin):
    __tablename__ = 'users'

    username = Column(String(128),
                      nullable=False)

    books = relationship('Book',
                         back_populates='user')
