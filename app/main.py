import logging
import secrets

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core import config, load_logging_config
from app.core.exceptions import custom_http_exception_handler
from app.routes import router

load_logging_config()
logger = logging.getLogger(__name__)

IS_LOCAL = config.ENVIRONMENT == "local" or config.ENVIRONMENT == "stg"
DOCS_URL = "/docs" if IS_LOCAL else None
REDOC_URL = "/redoc" if IS_LOCAL else None
OPENAPI_URL = "/openapi.json" if IS_LOCAL else None

app: FastAPI = FastAPI(docs_url=DOCS_URL, redoc_url=REDOC_URL, openapi_url=OPENAPI_URL)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(ValueError, custom_http_exception_handler)

SECRET_KEY = secrets.token_urlsafe(32)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


app.include_router(router)
