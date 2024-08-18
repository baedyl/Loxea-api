from typing import Annotated
from typing import Optional

from fastapi import APIRouter
from fastapi import Query
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from sqlmodel import Session

from app.config.config import config
from app.controller.dependencies import get_user_repo
from app.data.backoffice import schemas
from app.data.backoffice.schemas import LoginResponse
from app.data.backoffice.schemas import LoginSchema
from app.data.user_repo import AbstractUserRepo
from app.db.session_hook import get_db
from app.domain import auth_service

router = APIRouter(prefix="/bo")


# Health Check
@router.get("/health")
async def health_check():
    return {"ping": "pong"}


# User Routes


@router.post("/login", response_model=LoginResponse, description="Back Office Login")
async def login(
    schema: LoginSchema, user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)]
):
    user = auth_service.login(
        email=schema.email,
        password=schema.password,
        secret_key=config.SECRET_KEY,
        access_token_expiration_time=config.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expiration_time=config.REFRESH_TOKEN_EXPIRE_MINUTES,
        user_repo=user_repo,
        is_admin=True,
    )
    return LoginResponse(
        name=user["name"],
        email=user["email"],
        access_token=user["access_token"],
        refresh_token=user["refresh_token"],
    )


@router.post("/users", response_model=schemas.UserDetailSchema)
async def create_user(schema: schemas.CreateUserSchema): ...


@router.get("/users/{id}", response_model=schemas.UserDetailSchema)
async def get_user(id: int): ...


@router.put("/users/{id}", response_model=schemas.UserDetailSchema)
async def update_user(id: int, schema: schemas.UpdateUserSchema): ...


@router.delete("/users/{id}")
async def delete_user(id: int): ...


@router.get("/users", response_model=schemas.UserListSchema)
async def get_users(offset: Optional[int] = Query(0), size: Optional[int] = Query(30)): ...


# Feedback Routes
@router.get("/feedbacks", response_model=schemas.FeedbackListSchema)
async def get_feedbacks(offset: Optional[int] = Query(0), size: Optional[int] = Query(30)): ...


@router.get("/feedbacks/{id}", response_model=schemas.FeedbackSchema)
async def get_feedback(id: int): ...


# Emmergency contact routes
@router.get("/contacts", response_model=schemas.EmmergencyContactListSchema)
async def get_contacts(offset: Optional[int] = Query(0), size: Optional[int] = Query(30)): ...


@router.get("/contacts/{id}", response_model=schemas.EmmergencyContactSchema)
def get_contact(id: int): ...


@router.post("/contacts", response_model=schemas.EmmergencyContactSchema)
async def create_contact(schema: schemas.CreateEmmergencyContactSchema): ...


@router.put("/contacts/{id}", response_model=schemas.EmmergencyContactSchema)
async def update_contact(id: int, schema: schemas.UpdateEmmergencyContactSchema): ...


@router.delete("/contact/{id}")
async def delete_contact(id: int): ...


# FAQs Routes
@router.post("/faqs", response_model=schemas.FAQSchema)
async def create_faq(schema: schemas.CreateFAQSchema): ...


@router.get("/faqs", response_model=schemas.FAQListSchema)
async def get_faqs(offset: Optional[int] = Query(0), size: Optional[int] = Query(30)): ...


@router.get("/faqs/{id}", response_model=schemas.FAQListSchema)
async def get_faq(id: int): ...


@router.put("/faqs/{id}", response_model=schemas.FAQSchema)
async def update_faq(id: int, schema: schemas.UpdateFAQSchema): ...


@router.delete("/faqs/{id}")
async def delete_faq(id: int): ...


# Assistance Routes
@router.get("/assistance", response_model=schemas.AssistanceListSchema)
async def get_assistance_list(
    offset: Optional[int] = Query(0), size: Optional[int] = Query(30), type: Optional[str] = Query(None)
): ...


@router.get("/assistance/{id}", response_model=schemas.AssistanceSchema)
async def get_assistance(id: int, type: Optional[str] = Query(None)): ...


@router.put("/assistance/{id}", response_model=schemas.AssistanceSchema)
async def update_assistance(id: int, schema: schemas.UpdateAssistanceSchema): ...


# Identification Routes
@router.put("/identifications/{id}", response_model=schemas.IdentificationSchema)
async def update_identification(
    id: int, schema: schemas.UpdateIdentificationSchema
): ...


@router.get("/identifications/{id}", response_model=schemas.IdentificationSchema)
async def get_identification(id: int): ...


@router.get("/identifications", response_model=schemas.IdentificationListSchema)
async def get_identifications(offset: Optional[int] = Query(0), size: Optional[int] = Query(30)): ...


@router.post(
    "/identifications/upload-file",
    response_model=schemas.IdentificationFileUploadResponseSchema,
)
async def upload_identification_file(
    file: UploadFile = File(...), db: Session = Depends(get_db)
): ...
