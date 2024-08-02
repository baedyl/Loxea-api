from logging.config import dictConfig

from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware

from app.config.catch_all_exception import catch_all_exception
from app.config.config import config
from app.config.http import exception_error
from app.config.http import validation_error
from app.config.logs import LogConfig
from app.config.response import HTTPErrorResponse
from app.config.response import HTTPException
from app.controller.back_office import router as bo_router
from app.controller.client import router as client_router
from app.db.database import create_db_and_tables

create_db_and_tables()


def create_app():
    main_app = FastAPI(title=config.SERVER_NAME)

    dictConfig(LogConfig().model_dump())

    # Static Folder
    main_app.mount("/static", StaticFiles(directory="static"), name="static")
    main_app.include_router(bo_router)
    main_app.include_router(client_router)

    # Route Context Configuration
    main_app.add_middleware(
        RawContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
    )
    main_app.middleware("http")(catch_all_exception)

    # Cors Middleware Configuration
    main_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Endpoints

    # Override Validation Error Response
    @main_app.exception_handler(RequestValidationError)
    async def request_validation_error(_, error):
        return validation_error(error)

    # Override HTTP Error Response
    @main_app.exception_handler(HTTPException)
    async def http_exception(_, exc: HTTPException):
        return exception_error(exc)

    # Override 404 Error Response
    @main_app.exception_handler(404)
    async def custom_404_handler(_, __):
        return HTTPErrorResponse(
            title="Not Found",
            details="The requested response has not been found",
            status_code=status.HTTP_404_NOT_FOUND,
        ).response()

    return main_app
