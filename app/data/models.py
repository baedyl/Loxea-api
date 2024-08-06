from typing import List, Optional
from sqlmodel import Field, Relationship
from app.db.base import Base


class EmergencyContact(Base, table=True):
    __tablename__ = "emergency_contacts"

    name: str
    number: str

class Faq(Base, table=True):
    __tablename__ = "faqs"

    question: str
    answer: str


class IdentificationDetails(Base, table=True):
    __tablename__ = "identification_details"

    chassis_number: str = Field(index=True, unique=False)
    plate_number: str = Field(index=True, unique=False)
    type: str


class User(Base, table=True):
    __tablename__ = "users"

    name: str
    email: str = Field(index=True, unique=True)
    password: str
    code: str
    is_admin: Optional[bool] = False
    profile_image_url: Optional[str] = None
    chassis_number: Optional[str] = None
    plate_number: Optional[str] = None
    feedbacks: List["Feedback"] = Relationship(back_populates="user")
    assistances: List["Assistance"] = Relationship(back_populates="user")


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
    type: str
    user: Optional[User] = Relationship(back_populates="assistances")
    images: List["AssistanceImage"] = Relationship(back_populates="assistance")


class AssistanceImage(Base, table=True):
    __tablename__ = "assistance_images"

    image_url: str
    assistance_id: Optional[int] = Field(default=None, foreign_key="assistances.id")
    assistance: Optional[Assistance] = Relationship(back_populates="images")