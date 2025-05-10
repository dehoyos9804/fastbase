# -*- coding: utf-8 -*-
import time
import uuid
from datetime import datetime

from loguru import logger
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class LogRequestMiddleware:
    """
    Middleware ASGI para FastAPI/Starlette que registra información detallada
    sobre cada solicitud HTTP entrante y la respuesta correspondiente.
    Utiliza Loguru para una gestión de logs flexible y potente.
    """

    def __init__(self, app: ASGIApp):
        """
        Inicializa el middleware.

        Args:
            app: La aplicación ASGI a la que se adjunta este middleware (puede ser
                 la aplicación principal de FastAPI/Starlette u otro middleware).
        """
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """
        Procesa cada solicitud/respuesta que pasa a través del middleware.
        Este es el método principal llamado por el servidor ASGI.

        Args:
            scope: Un diccionario que contiene información sobre la conexión.
                   Para HTTP, incluye detalles como el método, la ruta, las cabeceras, etc.
            receive: Un canal awaitable para recibir mensajes del cuerpo de la solicitud.
            send: Un canal awaitable para enviar mensajes de respuesta al cliente.
        """
        if scope["type"] != "http":
            # Si el scope no es HTTP (por ejemplo, websocket), pasa la llamada
            # al siguiente componente de la aplicación sin procesarla aquí.
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        request = Request(scope)

        # Inyectar X-Request-ID en las cabeceras de la solicitud para que esté disponible
        # en los endpoints o middlewares posteriores.
        # scope["headers"] es una lista de tuplas (bytes, bytes).
        original_headers = list(scope.get("headers", []))
        original_headers.append((b"x-request-id", request_id.encode('utf-8')))
        scope["headers"] = original_headers

        # Contextualizar el logger con el request_id. Si el formato del logger
        # incluye {extra[request_id]}, este valor se imprimirá automáticamente.
        with logger.contextualize(request_id=request_id):
            ts_request_start_iso = datetime.now().isoformat()
            time_request_start_perf = time.perf_counter()

            client_host = request.client.host if request.client else "N/A"
            client_port = request.client.port if request.client else "N/A"

            # Log de la solicitud entrante
            logger.info(
                f"REQUEST START | Method: {request.method} | Path: {request.url.path} | "
                f"Client: {client_host}:{client_port} | "
                f"Timestamp: {ts_request_start_iso} | "
                f"User-Agent: {request.headers.get('user-agent', 'N/A')} | "
                f"Content-Type: {request.headers.get('content-type', 'N/A')} | "
                f"Authorization: {'Present' if request.headers.get('Authorization') else 'N/A'}"
            )

            # Variable para almacenar el código de estado de la respuesta.
            # Se inicializa a 500 en caso de que un error catastrófico impida
            # que se envíe una respuesta normal.
            response_status_code_capture = {"status": 500}

            async def send_wrapper(message: Message) -> None:
                """
                Wrapper alrededor del canal `send` original para interceptar
                el mensaje 'http.response.start', que contiene el código de estado
                y las cabeceras de la respuesta antes de que se envíen al cliente.
                """
                if message["type"] == "http.response.start":
                    response_status_code_capture["status"] = message.get("status", 500)

                    # Inyectar X-Request-ID en las cabeceras de la respuesta.
                    response_headers = MutableHeaders(scope=message)
                    response_headers["X-Request-ID"] = request_id
                    message["headers"] = response_headers.raw  # Actualizar las cabeceras en el mensaje

                await send(message)  # Enviar el mensaje original (o modificado)

            try:
                # Pasar la solicitud al siguiente componente de la aplicación (otro middleware o el endpoint).
                # Se usa el send_wrapper para poder interceptar los detalles de la respuesta.
                await self.app(scope, receive, send_wrapper)
            except Exception as e:
                # Si ocurre una excepción no controlada durante el procesamiento de la solicitud
                # en la aplicación (después de este middleware), se registra aquí.
                time_request_end_perf = time.perf_counter()
                duration_ms = (time_request_end_perf - time_request_start_perf) * 1000

                # El response_status_code_capture["status"] podría seguir siendo 500
                # o podría haber sido establecido por un manejador de excepciones de FastAPI
                # antes de que la excepción llegara aquí.
                logger.error(
                    f"REQUEST FAILED (UNHANDLED EXCEPTION) | Method: {request.method} | Path: {request.url.path} | "
                    f"Status: {response_status_code_capture['status']} | Duration: {duration_ms:.2f}ms | Error: {type(e).__name__}(\"{e}\")"
                )
                raise  # Re-lanzar la excepción para que el framework la maneje adecuadamente.
            else:
                # Este bloque se ejecuta si self.app() completó sin lanzar una excepción no controlada.
                time_request_end_perf = time.perf_counter()
                duration_ms = (time_request_end_perf - time_request_start_perf) * 1000
                status_code = response_status_code_capture["status"]

                log_message = (
                    f"REQUEST END | Method: {request.method} | Path: {request.url.path} | "
                    f"Status: {status_code} | Duration: {duration_ms:.2f}ms"
                )

                if status_code >= 500:
                    logger.error(log_message)
                # Para errores del cliente (4xx), podrías usar logger.warning().
                # Siguiendo el requisito de usar solo info o error:
                # elif status_code >= 400:
                #     logger.warning(log_message) # Opcional: logger.info(log_message)
                else:  # Para 1xx, 2xx, 3xx, y 4xx (según la decisión anterior)
                    logger.info(log_message)
