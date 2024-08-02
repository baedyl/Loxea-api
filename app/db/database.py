from sqlalchemy import Engine
from sqlmodel import SQLModel
from sqlmodel import create_engine

from app.config.config import config

engine: Engine = create_engine(
    str(config.SQLALCHEMY_DATABASE_URI), echo=config.ENVIRONMENT == "dev"
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
