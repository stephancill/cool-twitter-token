from sanic import Sanic
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

app = Sanic("my_app")

bind = create_async_engine("postgresql+asyncpg://postgres:postgres@localhost/test", echo=True)

Base = declarative_base()