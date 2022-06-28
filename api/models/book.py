from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
# from sqlalchemy_utils import UUIDType
# from uuid import uuid4
from .mixins import Mixin


class Book(Base, Mixin):
    __tablename__ = 'books'

    title = Column(String(256),
                   nullable=False)
    # user_id = Column(UUIDType(binary=False),
    #                  ForeignKey('users.uuid'),
    #                  nullable=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'),
                     nullable=True)

    user = relationship('User',
                        back_populates='books')
