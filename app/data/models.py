from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from app.db.base import Base


class UserChassisLink(SQLModel, table=True):
    __tablename__ = 'user_chassis_link'
    
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", primary_key=True)
    chassis_id: Optional[int] = Field(default=None, foreign_key="chassis.id", primary_key=True)


class Chassis(Base, table=True):
    __tablename__ = 'chassis'
    
    vin: str = Field(index=True, nullable=False)
    
    users: List["User"] = Relationship(back_populates="chassis", link_model=UserChassisLink)


class EmergencyContact(Base, table=True):
    __tablename__ = 'emergency_contacts'
    
    name: str
    number: str


class User(Base, table=True):
    __tablename__ = 'users'
    
    name: str
    email: str = Field(index=True, nullable=False, unique=True)
    password: str
    code: str = Field(index=True, nullable=False, unique=False)
    
    chassis: List[Chassis] = Relationship(back_populates="users", link_model=UserChassisLink)
    assistances: List["Assistance"] = Relationship(back_populates="user")
    accident_declarations: List["AccidentDeclaration"] = Relationship(back_populates="user")
    feedbacks: List["Feedback"] = Relationship(back_populates="user")


class Assistance(Base, table=True):
    __tablename__ = 'assistances'
    
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    gps_latitude: Optional[str] = Field(default=None)
    gps_longitude: Optional[str] = Field(default=None)
    address_complement: Optional[str] = Field(default=None)
    comment: Optional[str] = Field(default=None)
    
    user: Optional[User] = Relationship(back_populates="assistances")


class AccidentDeclaration(Base, table=True):
    __tablename__ = 'accident_declarations'
    
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    description: str
    image_urls: Optional[str] = Field(default=None)
    
    user: Optional[User] = Relationship(back_populates="accident_declarations")


class Feedback(Base, table=True):
    __tablename__ = 'feedbacks'
    
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    category_id: Optional[int] = Field(default=None, foreign_key="feedback_categories.id")
    message: str
    
    user: Optional[User] = Relationship(back_populates="feedbacks")
    category: Optional["FeedbackCategory"] = Relationship(back_populates="feedbacks")


class FeedbackCategory(Base, table=True):
    __tablename__ = 'feedback_categories'
    
    name: str
    
    feedbacks: List[Feedback] = Relationship(back_populates="category")
