import traceback

from fastapi import Request
from fastapi import status

from app.config.response import HTTPErrorResponse
from app.config.response import HTTPException
from app.utils.logger import get_logger

log = get_logger()


async def catch_all_exception(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as err:
        log.error(err)
        return HTTPErrorResponse(title=err.title, details=err.message).response()
    except Exception as exc:

        log.error(exc)
        traceback.print_exc()
        return HTTPErrorResponse(
            title="Server Error",
            details="An error occurred. Contact an admin for assistance",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ).response()
