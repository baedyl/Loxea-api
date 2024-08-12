from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING
from typing import Any

import bcrypt
from starlette.types import ASGIApp

from app import HTTPErrorResponse, config
from app.data.user_repo import AbstractUserRepo

if TYPE_CHECKING:
    from fastapi import Request

from fastapi.routing import APIRoute
from jose import JWTError
from jose import jwt
from passlib.exc import InvalidTokenError
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

if TYPE_CHECKING:
    from starlette.routing import Route

ALGORITHM = "HS256"


class AuthorizationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, repo: AbstractUserRepo):
        super().__init__(app)
        self._repo = repo

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ):
        route_endpoint = AuthorizationMiddleware._get_route_endpoint(
            current_path=request.url.path,
            routes=(
                request.scope.get("app", None).router.routes
                if request.scope.get("app", None)
                else []
            ),
        )
        if route_endpoint:
            if hasattr(route_endpoint, "_require_authorization"):
                authorization_header = request.headers.get("authorization")
                if not authorization_header:
                    request.state.current_user = None
                    return HTTPErrorResponse(
                        title="Unauthorized Access",
                        details="Authorization missing",
                        status_code=status.HTTP_401_UNAUTHORIZED,
                    ).response()

                else:
                    token = authorization_header.split(" ")[1]
                    payload = AuthorizationMiddleware.get_payload_from_token(token)

                    if not payload:
                        return HTTPErrorResponse(
                            title="Access Token Invalid",
                            details="The provided access token is not valid",
                            status_code=status.HTTP_401_UNAUTHORIZED,
                        ).response()
                    if not self._validate_token_against_db(subject=payload, token=token):
                        return HTTPErrorResponse(
                            title="Access Token Invalid",
                            details="The provided access token is not valid",
                            status_code=status.HTTP_401_UNAUTHORIZED,
                        ).response()

                    current_user = self._get_user_record_from_db(ref_key=payload)
                    request.state.current_user = current_user
                    if not current_user:
                        return HTTPErrorResponse(
                            title="Unauthorized Access",
                            details="The user requesting this resource is not authorized",
                            status_code=status.HTTP_401_UNAUTHORIZED,
                        ).response()
                    return await call_next(request)
            else:
                request.state.current_user = None
            return await call_next(request)
        else:
            request.state.current_user = None
            return await call_next(request)

    @staticmethod
    def _get_route_endpoint(
        current_path: str | None, routes: list[Route | APIRoute]
    ) -> Any | None:
        if current_path is None:
            return None

        for route in routes:
            if isinstance(route, APIRoute) and route.path == current_path:
                return route.endpoint
        return None

    @staticmethod
    def get_payload_from_token(token: str) -> str | None:
        try:
            payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub")
        except InvalidTokenError:
            return None
        except JWTError:
            return None

    def _get_user_record_from_db(self, ref_key) -> dict[str, str] | None:
        record = self._repo.get_user_from_ref_key(ref_key=ref_key)
        return record if record else None

    def _validate_token_against_db(self, subject: str, token: str) -> bool:
        record = self._repo.get_tokens_from_ref_key(ref_key=subject)
        if record:
            return bcrypt.checkpw(token.encode("utf-8"), record["access_token"])
        return False


def require_authorization(function):
    function._require_authorization = True

    @wraps(function)
    async def wrapper(*args, **kwargs):
        return await function(*args, **kwargs)

    return wrapper
