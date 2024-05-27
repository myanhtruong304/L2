import logging

from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

app = FastAPI()

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"detail": str(exc), "status_code": 400}, status_code=400)


class MigrationException(HTTPException):
    def __init__(self, detail: str, status_code: int = HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)


async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)
