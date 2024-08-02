from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str


class SignUpSchema(BaseModel):
    name: str
    email: str
    chassis: str
    password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class RequestPasswordResetSchema(BaseModel):
    email: str


class ValidateResetCodeSchema(BaseModel):
    code: str


class ResetPasswordSchema(BaseModel):
    email: str
    code: str
    password: str


class RequestAssistanceSchema(BaseModel):
    longitude: str
    latitude: str
    address_complement: str
    comment: str
