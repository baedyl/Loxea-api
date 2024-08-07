import random
from datetime import datetime
from datetime import timedelta
from typing import Any

import bcrypt
from jose import ExpiredSignatureError
from jose import JWTError
from jose import jwt
from passlib.exc import InvalidTokenError
from starlette import status

from app import HTTPException
from app.data.user_repo import AbstractUserRepo


def login(
    email: str,
    password: str,
    access_token_expiration_time: int,
    refresh_token_expiration_time: int,
    user_repo: AbstractUserRepo,
) -> dict[str, str]:
    user = user_repo.get_user_from_email(email=email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            title="User Not Found",
            message=f"User with email {email} not found",
        )
    if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        raise HTTPException(
            title="Incorrect password", message="Supplied password is incorrect"
        )

    access_token = _create_token(
        subject=user["ref_key"],
        expires_delta=timedelta(minutes=access_token_expiration_time),
    )
    refresh_token = _create_token(
        subject=user["ref_key"],
        expires_delta=timedelta(minutes=refresh_token_expiration_time),
    )

    user["access_token"] = access_token
    user["refresh_token"] = refresh_token
    return user


def sign_up(
    email: str,
    name: str,
    password: str,
    chassis_number: str,
    plate_number: str,
    access_token_expiration_time: int,
    refresh_token_expiration_time: int,
    user_repo: AbstractUserRepo,
):
    if not user_repo.validate_identification_information(
        chassis_number=chassis_number, plate_number=plate_number
    ):
        raise HTTPException(
            title="Invalid chassis number",
            message=f"The submitted chassis number {chassis_number} is invalid",
        )

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user = user_repo.create_user(email=email, name=name, password=str(hashed_password))
    access_token = _create_token(
        subject=user["ref_key"],
        expires_delta=timedelta(minutes=access_token_expiration_time),
    )
    refresh_token = _create_token(
        subject=user["ref_key"],
        expires_delta=timedelta(minutes=refresh_token_expiration_time),
    )

    user["access_token"] = access_token
    user["refresh_token"] = refresh_token
    return user


def refresh_user_token(
    refresh_token: str,
    secret_key: str,
    access_token_expiration_time: int,
    user_repo: AbstractUserRepo,
):
    ref_key = _get_payload_from_token(token=refresh_token, secret_key=secret_key)
    if not ref_key:
        raise HTTPException(
            title="Invalid Refresh Token", message="The provided token is invalid"
        )
    user = user_repo.get_user_from_ref_key(ref_key=ref_key)
    if not user:
        raise HTTPException(
            title="User Not Found",
            message="User associated with the token is not found",
        )

    access_token = _create_token(
        subject=user["external_reference"],
        expires_delta=timedelta(minutes=access_token_expiration_time),
    )
    return access_token


def request_password_reset(email: str, user_repo: AbstractUserRepo):
    user = user_repo.get_user_from_email(email)
    if not user:
        raise HTTPException(
            title="User Not Found",
            message=f"No user associated with the provided email {email}",
        )
    code = _generate_reset_code()
    # Forward email to user
    user_repo.save_user_reset_code(email=email, code=code)
    return code


def validate_password_reset_code(email: str, code: str, user_repo: AbstractUserRepo):
    user = user_repo.get_user_from_email(email=email)
    if not user:
        raise HTTPException(
            title="User Not Found",
            message=f"No user associated with the provided email {email}",
        )
    return user["code"] == code


def reset_password(code: str, email: str, password: str, user_repo: AbstractUserRepo):
    user = user_repo.get_user_from_email(email=email)
    if not user:
        raise HTTPException(
            title="User Not Found",
            message=f"No user associated with the provided email {email}",
        )
    if user["code"] != code:
        raise HTTPException(
            title="Invalid reset code", message="Provided reset code is not valid"
        )

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_repo.save_user_reset_code(email=email, code=None)
    user_repo.change_user_password(new_password=str(hashed_password), email=email)


def _create_token(self, subject: str, expires_delta: timedelta) -> str:
    to_encode: dict[str, Any] = {"sub": subject}
    expire = datetime.utcnow() + expires_delta
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, self._secret_key, algorithm="HS256")
    return encoded_jwt


def _get_payload_from_token(token: str, secret_key: str) -> str | None:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        ref_key = payload.get("sub")
        if ref_key is None:
            return None
        return ref_key
    except ExpiredSignatureError:
        return None
    except InvalidTokenError:
        return None
    except JWTError:
        return None


def _generate_reset_code() -> str:
    return "".join([random.choice("1234567890") for i in range(5)])
