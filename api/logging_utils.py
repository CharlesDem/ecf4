import logging
import time
from pathlib import Path

from fastapi import FastAPI, Request


def setup_logger(log_file: str = "api.logs") -> logging.Logger:
    logger = logging.getLogger("api")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = logging.FileHandler(Path(log_file), encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


def register_request_logging(app: FastAPI, logger: logging.Logger) -> None:
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            logger.exception("request failed | %s %s", request.method, request.url.path)
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "request | %s %s | status=%s | duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
