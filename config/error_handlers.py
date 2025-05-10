# -*- coding: utf-8 -*-
"""Módulo con funciones para manejar excepciones en las solicitudes a FastAPI.
Para más información, te recomendamos leer la documentación del Proyecto.

- https://fastapi.tiangolo.com/tutorial/handling-errors/
- https://fastapi.tiangolo.com/how-to/custom-request-and-route/
- https://www.starlette.io/requests/

FIX:
Mejoras en la presentación de mensajes de error y logging. Inspirados en patrones de repositorios como:
- https://gitlab.com/HomeInside/callisto.git.
"""

from typing import Any
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import RequestValidationError
from loguru import logger
from extensions.rest.rest import Rest
from fastapi import status


async def not_found(request: Request, exc: Exception) -> Any:
    """
    Manejador de excepciones para errores 404 (No Encontrado).

    Esta función se activa cuando FastAPI no puede encontrar una ruta que coincida
    con la solicitud del cliente. Devuelve una respuesta JSON estandarizada indicando que el recurso solicitado no existe.

    Parameters:
        request (Request): El objeto de la solicitud FastAPI que causó el error. Contiene información sobre la petición (método, URL, etc.).

        exc (Exception): La excepción específica que se levantó (generalmente una HTTPException
                         con estado 404, aunque aquí se captura de forma más genérica
                         si se registra para `Exception` en lugar de `HTTPException` específica).

    """
    logger.warning(f"¡OMG! 😱 ¡Alerta de Recurso Perdido en el Ciberespacio! "
                   f"No pudimos encontrar lo que buscabas en: {request.method} {request.url.path}, "
                   f"Detalles del fantasma: {exc}")

    return Rest.response(
        status_http=status.HTTP_404_NOT_FOUND,
        message="¡OMG! 😱 ¡Alerta de Recurso Perdido en el Ciberespacio!",
        errors={'code': 'RESOURCE_NOT_FOUND', 'message': 'El recurso solicitado no existe'}
    )


async def request_entity_to_large(request: Request, exc: Exception) -> Any:
    """Para GAE/Cloud Run, cuando la solicitud es más grande de lo
    que el servidor quiere o puede servir.

     Args:
        request (Request): una instancia de `Request`
            para las conexiones HTTP entrantes
        exc (Exception): la exception generada

    Returns:
        un objeto de tipo ORJSONResponse
    """
    logger.warning(
        f"¡OMG! 😱 ¡Carga Pesada Detectada en el Ciberespacio! "
        f"solicitud para {request.method} {request.url.path} "
        f"es demasiado grande para manejar. Detalles del exceso de equipaje: {exc}"
    )
    return Rest.response(
        status_http=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        message="¡OMG! 😱 ¡Carga Pesada Detectada en el Ciberespacio!",
        errors={'code': 'PAYLOAD_TOO_LARGE', 'message': 'La solicitud es demasiado grande.'}
    )


async def internal_server_error(request: Request, exc: Exception) -> Any:
    """Se encarga de devolver las respuestas en JSON por defecto,
    cuando se lanza una HTTPException, para prevenir que el
    BackEnd genere un error 500x.

    Args:
        request (Request): una instancia de `Request`
            para las conexiones HTTP entrantes
        exc (Exception): la exception generada

    Returns:
        un objeto de tipo ORJSONResponse
    """
    logger.warning(
        f"¡Alerta Roja! 🔥 ¡Fallo Catastrófico en el Núcleo del Ciberespacio! "
        f"Algo ha explotado internamente durante la solicitud {request.method} {request.url.path}. "
        f"Detalles de la implosión: {exc}"
    )
    return Rest.response(
        status_http=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="¡Houston, tenemos un problema GRAVE en el Ciberespacio! Algo salió terriblemente mal en nuestro lado.",
        errors={
            'code': 'INTERNAL_SERVER_ERROR',
            'message': 'Ocurrió un error inesperado en el servidor. Por favor, '
                       'intentalo de nuevo más tarde o contacta a soporte si el problema persiste'
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> Any:
    """Sobreescribe algunos errores de fastapi (Ej. 422) por mensajes acordes
    a la estructura de respuestas del BackEnd.

    Args:
        request (Request): una instancia de `Request`
            para las conexiones HTTP entrantes
        exc (RequestValidationError): la exception generada cuando
            una solicitud contiene datos no válidos

    Returns:
        un objeto de tipo ORJSONResponse
    """
    try:
        errors_detail = jsonable_encoder(exc.errors())
        logger.warning(f"🚨 ¡Falla Crítica en la Puerta del Ciberespacio! detalle: {errors_detail}")
    except Exception as e:
        logger.warning(f"🚨 ¡Falla Crítica en la Puerta del Ciberespacio! detalle: {e}")
        errors_detail = str(e)

    return Rest.response(
        status_http=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="unprocessable entity",
        errors={
            'code': 'UNPROCESSABLE',
            'message': errors_detail
        }
    )


async def not_allowed(request: Request, exc: Exception) -> Any:
    """Se encarga de devolver una respuesta JSON
        por defecto, cuando el recurso solicitado no
        está permitido, normalmente generado por APIRouter.

        Args:
            request (Request): una instancia de `Request`
                para las conexiones HTTP entrantes
            exc (Exception): la excepcion generada

        Returns:
            un objeto de tipo ORJSONResponse
    """
    logger.warning(
        f"🚫 ¡Método Bloqueado en el Ciberespacio! "
        f"El intento de usar el método {request.method} en la ruta {request.url.path} ha sido denegado. "
        f"Detalles de la restricción: {exc}"
    )

    return Rest.response(
        status_http=status.HTTP_405_METHOD_NOT_ALLOWED,
        message="🚫 Método no permitido en esta zona del ciberespacio.",
        errors={
            'code': 'METHOD_NOT_ALLOWED',
            'message': f"El método {request.method} no está permitido para la ruta solicitada. "
                       f"Por favor, verifica los métodos HTTP permitidos."
        }
    )


async def custom_http_exceptions(request: Request, exc: Exception) -> Any:
    """Sobreescribe algunos errores de fastapi generados por
    excepciones personalizadas y por `HTTPException`, con
    mensajes acordes a la estructura de respuestas del BackEnd.

    Args:
        request (Request): una instancia de `Request`
            para las conexiones HTTP entrantes
        exc (Exception|HTTPException): la excepcion generada cuando
            se genera una excepción

    Returns:
        un objeto de tipo ORJSONResponse

    Examples:
        ```
        ...
        fastapp.add_exception_handler(HTTPException, custom_http_exceptions)
        ```
    """

    logger.warning("OMFG! custom_http_exceptions!: {} {}", request.method, request.url.path)

    status_code = 401
    errors_detail = {"status": 401, "message": "unauthorized"}

    try:
        status_code = exc.status_code
        logger.warning("OMFG! custom_http_exceptions errors status_code!: {}", status_code)
        errors_detail = exc.detail
        # logger.warning("OMFG! custom_http_exceptions errors details: {}", errors_detail)
    except Exception as e:
        logger.warning("OMFG! custom_http_exceptions Exception: {}", e)

    return Rest.response(
        status_http=status_code,
        message="unprocessable entity",
        errors=errors_detail
    )

