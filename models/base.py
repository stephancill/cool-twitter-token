from sqlalchemy import INTEGER, Column, ForeignKey, String
from sqlalchemy.orm import declarative_base, relationship
from session import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(INTEGER(), primary_key=True)