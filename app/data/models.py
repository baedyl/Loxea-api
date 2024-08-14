import enum
from typing import List
from typing import Optional

from sqlmodel import Column
from sqlmodel import Enum
from sqlmodel import Field
from sqlmodel import Relationship

from app.db.base import Base


class EmergencyContact(Base, table=True):
    __tablename__ = "emergency_contacts"

    name: str
    number: str


class Faq(Base, table=True):
    __tablename__ = "faqs"

    question: str
    answer: str


class IncidentType(enum.Enum):
    Accident = "ACCIDENT"
    Assistance = "ASSISTANCE"


class IdentificationDetails(Base, table=True):
    __tablename__ = "identification_details"

    chassis_number: str = Field(index=True, unique=False)
    plate_number: str = Field(index=True, unique=False)
    type: str


class User(Base, table=True):
    __tablename__ = "users"

    name: str
    email: str = Field(index=True, unique=True)
    password: bytes
    code: Optional[str] = None
    is_admin: Optional[bool] = False
    profile_image_url: Optional[str] = None
    chassis_number: Optional[str] = None
    plate_number: Optional[str] = None
    feedbacks: List["Feedback"] = Relationship(back_populates="user")
    assistances: List["Assistance"] = Relationship(back_populates="user")


class Token(Base, table=True):
    subject: str = Field(unique=True)
    access_token: bytes
    refresh_token: bytes


class Feedback(Base, table=True):
    __tablename__ = "feedbacks"

    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    message: str
    user: Optional[User] = Relationship(back_populates="feedbacks")


class Assistance(Base, table=True):
    __tablename__ = "assistances"

    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    gps_latitude: Optional[str] = None
    gps_longitude: Optional[str] = None
    address_complement: Optional[str] = None
    comment: Optional[str] = None
    incident_type: IncidentType = Field(
        sa_column=Column(Enum(IncidentType))
    )
    user: Optional[User] = Relationship(back_populates="assistances")
    images: List["AssistanceImage"] = Relationship(back_populates="assistance")


class AssistanceImage(Base, table=True):
    __tablename__ = "assistance_images"

    image_url: str
    assistance_id: Optional[int] = Field(default=None, foreign_key="assistances.id")
    assistance: Optional[Assistance] = Relationship(back_populates="images")
