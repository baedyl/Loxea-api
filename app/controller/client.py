from fastapi import APIRouter

from app.data.schemas import LoginSchema
from app.data.schemas import RefreshTokenSchema
from app.data.schemas import RequestAssistanceSchema
from app.data.schemas import RequestPasswordResetSchema
from app.data.schemas import ResetPasswordSchema
from app.data.schemas import SignUpSchema
from app.data.schemas import ValidateResetCodeSchema

router = APIRouter(prefix="/api")


@router.post("/login")
async def login(schema: LoginSchema): ...


@router.post("/signup")
async def sign_up(schema: SignUpSchema): ...


@router.post("/refresh-token")
async def refresh_token(schema: RefreshTokenSchema): ...


@router.post("/request-password-reset")
async def request_password_reset(schema: RequestPasswordResetSchema): ...


@router.post("/validate-reset-code")
async def validate_password_reset_code(schema: ValidateResetCodeSchema): ...


@router.post("/reset-password")
async def reset_password(schema: ResetPasswordSchema): ...


@router.post("/request-assistance")
async def request_assistance(schema: RequestAssistanceSchema): ...


@router.get("/emergency-contacts")
async def get_emergency_contacts(): ...


@router.post("/submit-feedback")
async def submit_feedback(): ...
