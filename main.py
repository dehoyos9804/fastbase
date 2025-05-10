# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException
from Secweb import SecWeb
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import status

# Iniciar variables de entornos
load_dotenv()

from config.server import lifespan
from extensions.rest.rest import Rest
from config.error_handlers import custom_http_exceptions
from config.error_handlers import internal_server_error
from config.error_handlers import not_allowed
from config.error_handlers import not_found
from config.error_handlers import request_entity_to_large
from config.error_handlers import validation_exception_handler
from config.settings import ENDPOINT_API
from config.security.csp import CSP_FOR_SECWEB
from config.settings import CORS_CONFIG
from config.settings import USE_SECWEB
#from extensions.middleware.log_request_middleware import LogRequestMiddleware

# Iniciar la app de FastApi
app = FastAPI(
    title='🏗️ Backend Base para desarrollo ágil en el Ciberespacio',
    description='Backend Bae robusto y modular, diseñado para el desarrollo acelerado de aplicaciones '
                'y servicios seguros que operan e interactúan dentro del dinámico ciberespacio',
    version='1.0.1',
    openapi_url=f'{ENDPOINT_API}/openapi.json',
    docs_url=f'{ENDPOINT_API}/docs',
    redoc_url=f'{ENDPOINT_API}/redocs',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

# register middlewares
app.add_middleware(GZipMiddleware, minimum_size=100, compresslevel=6)

# register cors
# - https://github.com/tiangolo/fastapi/issues/1663
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_CONFIG.get('ALLOW_ORIGINS'),
    allow_credentials=True,
    allow_methods=CORS_CONFIG.get('ALLOW_METHODS'),
    allow_headers=CORS_CONFIG.get('ALLOW_HEADERS'),
)
#app.add_middleware(LogRequestMiddleware)


if USE_SECWEB:
    SecWeb(app=app, Option={'csp': CSP_FOR_SECWEB})

# register exception handlers
app.add_exception_handler(status.HTTP_404_NOT_FOUND, not_found)
app.add_exception_handler(status.HTTP_405_METHOD_NOT_ALLOWED, not_allowed)
app.add_exception_handler(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, request_entity_to_large)
app.add_exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR, internal_server_error)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exceptions)


@app.get("/")
async def home():
    return Rest.response(
        status_http=status.HTTP_200_OK,
        message='OK',
        data={'info': '🚀 ¡Bienvenid@ al ciberespacio'}
    )

