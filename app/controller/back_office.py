from fastapi import APIRouter
from app.data.models import Assistance

router = APIRouter(prefix="/bo")

@router.get("/health")
def health_check():
    return {
        "ping": "pong"
    }