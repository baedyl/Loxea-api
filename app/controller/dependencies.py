from fastapi import Depends

from app.data.assistance_repo import AbstractAssistanceRepo, AssistanceRepo
from app.data.user_repo import AbstractUserRepo
from app.data.user_repo import UserRepo
from app.db.session_hook import get_db
from app.domain.storage import GCPStorage, StorageBase


def get_user_repo(session=Depends(get_db)) -> AbstractUserRepo:
    return UserRepo(session=session)


def get_assistance_repo(session=Depends(get_db)) -> AbstractAssistanceRepo:
    return AssistanceRepo(session=session)


def get_storage() -> StorageBase:
    return GCPStorage()
