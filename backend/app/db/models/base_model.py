from sqlalchemy import Column
from sqlalchemy_utils import UUIDType


class DBModel:
    uuid = Column(UUIDType(binary=False), primary_key=True)
