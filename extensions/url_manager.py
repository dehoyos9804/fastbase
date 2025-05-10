# -*- coding: utf-8 -*-
from typing import Any
from typing import Optional
from typing import List
from importlib import import_module
from loguru import logger
from config.settings import ENDPOINT_API
from config.settings import INSTALLED_MODULES
from fastapi import FastAPI


class Url:
    """
    Representa un patrón de URL que se registrará en la aplicación FastAPI.
    Esta clase encapsula el objeto router, su prefijo de endpoint deseado,
    y cualquier argumento adicional para `app.include_router` de FastAPI.
    """
    def __init__(self, obj_handler, endpoint: str, *args: Any, **kwargs: Any):
        self.obj_handler = obj_handler
        self.endpoint = endpoint
        self.args = args
        self.kwargs = kwargs

    def register(self, app: FastAPI):
        if not app:
            logger.warning('La La instancia de la aplicación FastAPI no fue proporcionada. No se registrará la ruta.')
            return

        if not self.obj_handler:
            logger.warning('El manejador de objetos (router) no fue proporcionado. No se registrará la ruta')
            return

        try:
            full_prefix = f'{ENDPOINT_API}{self.endpoint}'
            app.include_router(
                self.obj_handler,
                *self.args,
                **self.kwargs,
                prefix=full_prefix
            )
            logger.info(f'✅ Ruta registrada: {full_prefix}')
            return
        except Exception as e:
            logger.error(f'🚫 Error al registrar la ruta: {e}')
            return


def register_module(app: FastAPI):
    """
    Registra el endpoint en la aplicación

    Args:
        app: La instancia de la aplicación FastAPI a la que se añadirán las rutas.
    """
    logger.info(f'⏳ Cargando Recursos...')

    if not INSTALLED_MODULES:
        logger.info("No hay módulos listados en INSTALLED_MODULES. Omitiendo registro de URLs.")
        return
    for module in INSTALLED_MODULES:
        try:
            # Construir el nombre completo del submódulo 'urls' (ej., 'apps.home.urls')
            full_module_name = f'{module}.urls'

            # Importar el módulo que contiene las URL
            mod = import_module(full_module_name)

            # Obtener los patrones de URL del módulo importado (debe ser una lista de instancia de URL)
            urlpatterns: Optional[List[Url]] = getattr(mod, 'urlpatterns', [])

            if urlpatterns is None:
                logger.warning(f"⚠️ El módulo '{mod}' no tiene un atributo 'urlpatterns'. Omitiendo...")
                continue

            if not isinstance(urlpatterns, list):
                logger.warning(
                    f"⚠️ 'urlpatterns' en '{mod}' no es una lista "
                    f"(tipo: {type(urlpatterns).__name__}). Omitiendo."
                )
                continue

            if not urlpatterns:
                logger.info(f"ℹ️ 'urlpatterns' en '{mod}' está vacía. No hay rutas para registrar desde este módulo.")
                continue

            # Registra cada punto final de Urls con la aplicación
            for url in urlpatterns:
                url.register(app)
        except ModuleNotFoundError as mfe:
            logger.error(f'🚫 Module not found. {mfe}')
        except AttributeError as ate:
            logger.error(f'🚫 urlpatterns not found in urls: {ate}')
        except Exception as e:
            logger.error(f'🚫 Registering Error: {e}')

