from abc import ABC
from abc import abstractmethod

from sqlmodel import Session
from sqlmodel import select

from app.data.models import IdentificationDetails, Token
from app.data.models import User


class AbstractUserRepo(ABC):

    @abstractmethod
    def get_user_from_email(self, email: str): ...

    @abstractmethod
    def validate_identification_information(
        self, chassis_number: str, plate_number: str
    ): ...

    @abstractmethod
    def create_user(self, email: str, name: str, password: bytes, is_admin: bool): ...

    @abstractmethod
    def get_user_from_ref_key(self, ref_key: str): ...

    @abstractmethod
    def save_user_reset_code(self, email: str, code: str | None): ...

    @abstractmethod
    def change_user_password(self, new_password: str, email: str): ...

    @abstractmethod
    def get_tokens_from_ref_key(self, ref_key: str): ...

    @abstractmethod
    def save_tokens(self, subject: str, access_token: bytes, refresh_token: bytes): ...


class UserRepo(AbstractUserRepo):
    def __init__(self, session: Session):
        self._session = session

    def get_user_from_email(self, email: str) -> dict[str, str] | None:
        record = self._session.exec(
            select(User).where(User.email == email)
        ).one_or_none()
        return dict(record) if record else None

    def validate_identification_information(
        self, chassis_number: str, plate_number: str
    ) -> dict[str, str] | None:
        query = select(IdentificationDetails).where(
            IdentificationDetails.chassis_number == chassis_number
            and IdentificationDetails.plate_number == plate_number
        )
        record = self._session.exec(query).one_or_none()
        return dict(record) if record else None

    def create_user(self, email: str, name: str, password: bytes, is_admin: bool) -> dict[str, str]:
        user = User(email=email, name=name, password=password, is_admin=is_admin)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)

        return dict(user)

    def get_user_from_ref_key(self, ref_key: str) -> dict[str, str] | None:
        record = self._session.exec(
            select(User).where(User.external_reference == ref_key)
        ).one_or_none()
        return dict(record) if record else None

    def save_user_reset_code(self, email: str, code: str | None):
        user = self._session.exec(select(User).where(User.email == email)).one()
        user.code = code

        self._session.add(user)
        self._session.commit()

    def change_user_password(self, new_password: str, email: str):
        record = self._session.exec(select(User).where(User.email == email)).one()
        record.password = new_password

        self._session.add(record)
        self._session.commit()

    def get_tokens_from_ref_key(self, ref_key: str) -> dict[str, str] | None:
        record = self._session.exec(
            select(Token).where(Token.subject == ref_key)
        ).one_or_none()
        return dict(record) if record else None

    def save_tokens(self, subject: str, access_token: bytes, refresh_token: bytes):
        record = self._session.exec(
            select(Token).where(Token.subject == subject)
        ).one_or_none()
        if not record:
            record = Token(subject=subject, access_token=access_token, refresh_token=refresh_token)
        else:
            record.access_token = access_token
            record.refresh_token = refresh_token

        self._session.add(record)
        self._session.commit()


