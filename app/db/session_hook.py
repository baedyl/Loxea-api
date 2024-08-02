import logging
from typing import Annotated
from typing import Generator

from fastapi import Depends
from sqlmodel import Session

from app.db.database import engine

log = logging.getLogger("server")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
