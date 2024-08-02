import uuid
from datetime import datetime

from sqlmodel import Field
from sqlmodel import SQLModel


class Base(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    ref_key: str = Field(
        default_factory=lambda: str(uuid.uuid4()).replace("-", ""), index=True
    )
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    last_edited: datetime = Field(default_factory=datetime.now, nullable=False)
