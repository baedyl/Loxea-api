from typing import Any

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class HTTPResponse(BaseModel):
    status_code: int = status.HTTP_200_OK
    message: str = "Success"
    data: Any


class HTTPErrorResponse:
    def __init__(
        self, title: str, details: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        self.__error_body = {"title": title, "details": details}
        self.__status_code = status_code
        self.__result = {"status": "Failed", "errorBody": self.__error_body}

    def response(self) -> object:
        return JSONResponse(
            content=jsonable_encoder(self.__result),
            status_code=self.__status_code,
            headers={"Access-Control-Allow-Origin": "*"},
        )


class HTTPException(Exception):
    def __init__(
        self, title: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> None:
        self.message = message
        self.title = title
        self.status_code = status_code
        super().__init__(self.message)
