from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from app.db.base import Base

class IdentificationDetailsUserLink(SQLModel, table=True):
    __tablename__ = "identification_details_user_link"

    user_id: Optional[int] = Field(
        default=None, foreign_key="users.id", primary_key=True
    )
    identification_details_id: Optional[int] = Field(
        default=None, foreign_key="identification_details.id", primary_key=True
    )

class EmergencyContact(Base, table=True):
    __tablename__ = "emergency_contacts"

    name: str
    number: str

class Faq(Base, table=True):
    __tablename__ = "faqs"

    question: str
    answers: List["FaqAnswer"] = Relationship(back_populates="faq")

class FaqAnswer(Base, table=True):
    __tablename__ = "faq_answers"

    answer: str
    faq_id: Optional[int] = Field(default=None, foreign_key="faqs.id")
    faq: Optional[Faq] = Relationship(back_populates="answers")

class IdentificationDetails(Base, table=True):
    __tablename__ = "identification_details"

    chassis_number: str = Field(index=True, unique=False)
    plate_number: str = Field(index=True, unique=False)
    type: str
    users: List["User"] = Relationship(back_populates="identification_details", link_model=IdentificationDetailsUserLink)

class User(Base, table=True):
    __tablename__ = "users"

    name: str
    email: str = Field(index=True, unique=True)
    password: str
    code: str
    profile_image_url: Optional[str] = None

    identification_details: List[IdentificationDetails] = Relationship(back_populates="users", link_model=IdentificationDetailsUserLink)
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