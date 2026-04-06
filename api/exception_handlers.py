import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI, logger: logging.Logger) -> None:
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return _error_response(
            logger=logger,
            request=request,
            status_code=exc.status_code,
            detail=exc.detail,
            kind="http error",
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        status_code = 422 if _has_empty_title_error(errors) else 400
        return _error_response(
            logger=logger,
            request=request,
            status_code=status_code,
            detail=errors,
            kind="validation error",
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("unhandled error | %s %s", request.method, request.url.path)
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})


def _error_response(
    logger: logging.Logger,
    request: Request,
    status_code: int,
    detail,
    kind: str,
) -> JSONResponse:
    logger.error(
        "%s | %s %s | status=%s | detail=%s",
        kind,
        request.method,
        request.url.path,
        status_code,
        detail,
    )
    return JSONResponse(status_code=status_code, content={"detail": detail})


def _has_empty_title_error(errors: list[dict]) -> bool:
    return any(error.get("type") == "empty_title" for error in errors)
