from fastapi import APIRouter

router = APIRouter(prefix="/bo")


@router.get("/health")
def health_check():
    return {"ping": "pong"}
