
from sqlalchemy import INTEGER, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from .base import BaseModel

class Account(BaseModel):
    __tablename__ = "account"
    
    twitter_id = Column(String(), unique=True)
    eth_address = Column(String())
    balance = Column(INTEGER(), default=0)

    likes = relationship("Like")

