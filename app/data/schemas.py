from pydantic import BaseModel


class LoginSchema(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    name: str
    email: str
    access_token: str
    refresh_token: str


class SignUpSchema(BaseModel):
    name: str
    email: str
    chassis_number: str
    plate_number: str
    password: str


class SignUpResponse(BaseModel):
    name: str
    email: str
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class RequestPasswordResetSchema(BaseModel):
    email: str


class ValidateResetCodeSchema(BaseModel):
    code: str
    email: str


class ResetPasswordSchema(BaseModel):
    email: str
    code: str
    password: str


class RequestAssistanceSchema(BaseModel):
    longitude: str
    latitude: str
    address_complement: str
    comment: str
