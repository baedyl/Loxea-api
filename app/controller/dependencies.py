from fastapi import Depends

from app.data.user_repo import AbstractUserRepo
from app.data.user_repo import UserRepo
from app.db.session_hook import get_db


def get_user_repo(session=Depends(get_db)) -> AbstractUserRepo:
    return UserRepo(session=session)
