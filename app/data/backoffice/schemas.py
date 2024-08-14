from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

from app.data.models import IncidentType, AssistanceStatusType
from app.data.schemas import LoginSchema as BaseLoginSchema
from app.data.schemas import LoginResponse as BaseLoginResponse
from app.data.schemas import RefreshTokenSchema as BaseRefreshTokenSchema
from app.data.schemas import ResetPasswordSchema as BaseResetPasswordSchema
from app.data.schemas import RequestPasswordResetSchema as BaseRequestPasswordResetSchema
from app.data.schemas import ValidateResetCodeSchema as BaseValidateResetCodeSchema


# ======= User Schemas =========

class LoginSchema(BaseLoginSchema):
    pass 

class LoginResponse(BaseLoginResponse):
    pass 

class CreateUserSchema(BaseModel):
    name: str
    email: str 
    password: str 

class UpdateUserSchema(BaseModel):
    name: str 
    email: str

class CreateUserResponse(BaseModel):
    id: int 
    name: str 
    email: str 

class RefreshTokenSchema(BaseRefreshTokenSchema):
    pass

class RequestPasswordResetSchema(BaseRequestPasswordResetSchema):
    pass 

class ValidateResetCodeSchema(BaseValidateResetCodeSchema):
    pass

class ResetPasswordSchema(BaseResetPasswordSchema):
    pass 

class UserDetailSchema(BaseModel):
    id: int 
    external_reference: str
    name: str 
    email: str 
    is_admin: bool
    profile_image_url: Optional[str] = None
    chassis_number: Optional[str] = None
    plate_number: Optional[str] = None
    created_at: datetime
    last_updated: datetime


class UserListSchema(BaseModel):
    users: List[UserDetailSchema]


# ========== Identification Schemas =======

class IdentificationSchema(BaseModel):
    id: int 
    chassis_number: str
    plate_number: str
    type: str 
    created_at: datetime
    last_updated: datetime


class IdentificationListSchema(BaseModel):
    identifications: List[IdentificationSchema]


class UpdateIdentificationSchema(BaseModel):
    id: int
    chassis_number: str
    plate_number: str 
    type: str 

class IdentificationFileUploadResponseSchema(BaseModel):
    processed_records: Optional[int] = 0
    

# ========== Assistance Schema ======

class AssistanceImageSchema(BaseModel):
    image_url: str

class AssistanceSchema(BaseModel):
    id: int
    gps_latitude: str
    gps_longitude: str
    address_complement: str
    comment: str
    incident_type: IncidentType
    user: UserDetailSchema
    images: List[AssistanceImageSchema]
    status: AssistanceStatusType 
    created_at: datetime
    last_updated: datetime

class UpdateAssistanceSchema(BaseModel): 
    status: AssistanceStatusType

class AssistanceListSchema(BaseModel):
    assistance: List[AssistanceSchema]


# ===== Feedback Schemas ========
class FeedbackSchema(BaseModel):
    id: int 
    user: UserDetailSchema
    message: str 
    created_at: datetime
    last_updated: datetime


class FeedbackListSchema(BaseModel):
    feedbacks: List[FeedbackSchema]


# ===== Contact Schemas ========

class CreateEmmergencyContactSchema(BaseModel):
    name: str
    number: str 

class EmmergencyContactSchema(BaseModel):
    id: int 
    name: str
    number: str 
    created_at: datetime
    last_updated: datetime

class EmmergencyContactListSchema(BaseModel):
    contacts: List[EmmergencyContactSchema]

class UpdateEmmergencyContactSchema(BaseModel):
    name: str
    number: str


# ======= FAQ Schemas =======

class FAQSchema(BaseModel):
    id: int
    question: str 
    answer: str 
    created_at: datetime
    last_updated: datetime

class FAQListSchema(BaseModel):
    faqs: List[FAQSchema]

class CreateFAQSchema(BaseModel):
    question: str 
    answer: str 

class UpdateFAQSchema(BaseModel):
    id: int 
    question: str
    answer: str 





