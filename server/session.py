from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import config

engine = create_engine(
    config.DATABASE_URI,
)
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)

Base = declarative_base()

