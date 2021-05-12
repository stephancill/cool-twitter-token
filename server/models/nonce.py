
from sqlalchemy import INTEGER, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from session import Base

class Nonce(Base):
    __tablename__ = "nonce"
    
    nonce = Column(INTEGER(), default=0, primary_key=True)

