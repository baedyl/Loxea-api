import json

from fastapi import status
from fastapi.responses import JSONResponse

from app.config.response import HTTPException
from app.utils.logger import get_logger

log = get_logger()


# Override fastapi validation error
def validation_error(error) -> JSONResponse:
    errors: list = []
    for err in json.loads(error.json()):
        errors.append({err["loc"][-1]: err["msg"]})

    message = f"{list(errors[0].keys())[0]}: {list(errors[0].values())[0]}"
    log.error(message)
    response: dict = {
        "statusCode": status.HTTP_400_BAD_REQUEST,
        "message": message,
    }

    return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)


# Override fastapi http error response
def exception_error(exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "Failed",
            "errorBody": {"title": exc.title, "message": exc.message},
        },
    )
