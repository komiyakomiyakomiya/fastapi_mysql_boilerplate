from sqlalchemy import Column, Integer, text
from sqlalchemy.dialects.mysql import TIMESTAMP as Timestamp
# from sqlalchemy_utils import UUIDType
# from uuid import uuid4


class Mixin(object):
    # uuid = Column(UUIDType(binary=False), primary_key=True, default=uuid4)
    id = Column(Integer,
                primary_key=True,
                nullable=False,
                autoincrement=True,
                index=True)
    created_at = Column(Timestamp,
                        server_default=text('current_timestamp'),
                        nullable=False)
    updated_at = Column(Timestamp,
                        server_default=text('current_timestamp on update current_timestamp'),
                        nullable=False)
    del_flg = Column(Integer,
                     default=0,
                     nullable=False)
