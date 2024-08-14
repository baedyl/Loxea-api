from abc import ABC, abstractmethod
from typing import Any

from sqlmodel import Session, select

from app.data.models import IncidentType, Assistance, EmergencyContact, Feedback


class AbstractAssistanceRepo(ABC):

    @abstractmethod
    def create_incidence_record(
        self,
        user_id: int,
        latitude: str,
        longitude: str,
        address_complement: str,
        comment: str,
        type_: IncidentType,
        images: list[bytes] | None
    ): ...

    @abstractmethod
    def create_feedback_record(self, user_id: int, message: str): ...

    @abstractmethod
    def get_emergency_contacts(self): ...


class AssistanceRepo(AbstractAssistanceRepo):
    def __init__(self, session: Session):
        self._session = session

    def create_incidence_record(
        self, user_id: int,
        latitude: str,
        longitude: str,
        address_complement: str,
        comment: str,
        type_: IncidentType,
        images: list[bytes] | None
    ) -> dict[str, Any]:
        record = Assistance(
            user_id=user_id,
            gps_latitude=latitude,
            gps_longitude=longitude,
            address_complement=address_complement,
            incident_type=type_
        )
        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return dict(record)

    def get_emergency_contacts(self) -> list[dict[str, str]]:
        records = self._session.exec(select(EmergencyContact)).all()
        return list(map(lambda record: dict(record), records)) if records else []

    def create_feedback_record(self, user_id: int, message: str) -> dict[str, Any]:
        record = Feedback(user_id=user_id, message=message)

        self._session.add(record)
        self._session.commit()
        self._session.refresh(record)

        return dict(record)




