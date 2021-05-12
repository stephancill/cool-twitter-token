from sqlalchemy import INTEGER, Column, ForeignKey, String, DateTime
from sqlalchemy.sql.expression import null
from .base import BaseModel

class Like(BaseModel):
    __tablename__ = "like"
    
    account_id = Column(INTEGER(), ForeignKey("account.id"), nullable=False) 
    tweet_id = Column(String(), nullable=False)
    time = Column(DateTime(), nullable=False)

