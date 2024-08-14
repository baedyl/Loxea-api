from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends, Request
from starlette import status

from app import config
from app.controller.dependencies import get_user_repo, get_assistance_repo, get_storage
from app.data.assistance_repo import AbstractAssistanceRepo
from app.data.schemas import LoginResponse
from app.data.schemas import LoginSchema
from app.data.schemas import RefreshTokenSchema
from app.data.schemas import RequestAssistanceSchema
from app.data.schemas import RequestPasswordResetSchema
from app.data.schemas import ResetPasswordSchema
from app.data.schemas import SignUpResponse
from app.data.schemas import SignUpSchema
from app.data.schemas import ValidateResetCodeSchema
from app.data.user_repo import AbstractUserRepo
from app.domain import auth_service, assistance_service
from app.domain.authorization import require_authorization
from app.domain.storage import StorageBase

router = APIRouter(prefix="/api")


@router.post("/login", response_model=LoginResponse)
async def login(
    schema: LoginSchema,
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)]
):
    user = auth_service.login(
        email=schema.email,
        password=schema.password,
        secret_key=config.SECRET_KEY,
        access_token_expiration_time=config.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expiration_time=config.REFRESH_TOKEN_EXPIRE_MINUTES,
        user_repo=user_repo,
    )
    return LoginResponse(
        name=user["name"],
        email=user["email"],
        access_token=user["access_token"],
        refresh_token=user["refresh_token"],
    )


@router.post("/signup", response_model=SignUpResponse)
async def sign_up(
    schema: SignUpSchema, user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)]
):
    user = auth_service.sign_up(
        name=schema.name,
        email=schema.email,
        password=schema.password,
        chassis_number=schema.chassis_number,
        plate_number=schema.plate_number,
        secret_key=config.SECRET_KEY,
        access_token_expiration_time=config.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expiration_time=config.REFRESH_TOKEN_EXPIRE_MINUTES,
        user_repo=user_repo,
    )
    return SignUpResponse(
        name=user["name"],
        email=user["email"],
        access_token=user["access_token"],
        refresh_token=user["refresh_token"],
    )


@router.post("/refresh-token")
async def refresh_token(
    schema: RefreshTokenSchema,
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
):
    token = auth_service.refresh_user_token(
        refresh_token=schema.refresh_token,
        secret_key=config.SECRET_KEY,
        access_token_expiration_time=config.ACCESS_TOKEN_EXPIRE_MINUTES,
        user_repo=user_repo,
    )
    return {"access_token": token}


@router.post("/request-password-reset")
async def request_password_reset(
    schema: RequestPasswordResetSchema,
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
):
    code = auth_service.request_password_reset(email=schema.email, user_repo=user_repo)
    return {"code": code}


@router.post("/validate-reset-code")
async def validate_password_reset_code(
    schema: ValidateResetCodeSchema,
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
):
    is_valid = auth_service.validate_password_reset_code(
        email=schema.email, code=schema.code, user_repo=user_repo
    )
    return {"is_valid": is_valid}


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(
    schema: ResetPasswordSchema,
    user_repo: Annotated[AbstractUserRepo, Depends(get_user_repo)],
):
    auth_service.reset_password(
        code=schema.code,
        password=schema.password,
        email=schema.email,
        user_repo=user_repo,
    )


@router.post("/request-assistance", status_code=status.HTTP_201_CREATED)
@require_authorization
async def request_assistance(
    request: Request,
    schema: RequestAssistanceSchema,
    assistance_repo: Annotated[AbstractAssistanceRepo, Depends(get_assistance_repo)],
    storage: Annotated[StorageBase, Depends(get_storage)]
):
    assistance_service.request_assistance(
        user_id=request.state.current_user,
        latitude=schema.latitude,
        longitude=schema.longitude,
        address_complement=schema.address_complement,
        comment=schema.comment,
        images=None,
        image_extensions=None,
        type_=schema.type,
        assistance_repo=assistance_repo,
        storage=storage
    )


@router.post("/declare-accident")
@require_authorization
async def declare_accident(request: Request): ...


@router.get("/emergency-contacts")
@require_authorization
async def get_emergency_contacts(
    assistance_repo: Annotated[AbstractAssistanceRepo, Depends(get_assistance_repo)]
):
    return assistance_service.get_emergency_contacts(assistance_repo=assistance_repo)


@router.post("/submit-feedback")
@require_authorization
async def submit_feedback(): ...


@router.get("/faqs")
async def get_faqs(): ...
