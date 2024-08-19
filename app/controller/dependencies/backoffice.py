from fastapi import Depends 

from app.data.backoffice.identification_repo import AbstractIdentificationRepo, IdentificationRepo
from app.db.session_hook import get_db



def get_identification_repo(session=Depends(get_db)) -> AbstractIdentificationRepo:
    return IdentificationRepo(session)
