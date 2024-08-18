import uuid
from datetime import datetime
from datetime import timezone

from sqlmodel import Field
from sqlmodel import SQLModel


class Base(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    external_reference: str = Field(
        default_factory=lambda: str(uuid.uuid4()).replace("-", ""), index=True
    )
    is_deleted: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    last_updated: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )
    deleted_at: datetime | None = Field(nullable=True)
