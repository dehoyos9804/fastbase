from contextlib import asynccontextmanager
from loguru import logger
from config.settings import DATABASE_PROVIDER
from config.logger import start_logger
from config.database.connect.connection_uri import get_connection_uri
from config.database.manager import db_manager
from fastapi import FastAPI
from extensions.url_manager import register_module


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Iniciar Configuración de logs
    start_logger()
    logger.info('startup Backend')
    logger.info(DATABASE_PROVIDER)

    if DATABASE_PROVIDER is not None:
        # obtenemos la conexión de base de datos
        db_connection = get_connection_uri(DATABASE_PROVIDER)
        # Inicializa la conexión a la base de datos al iniciar la app
        await db_manager.init_database(db_connection)

    # Registrar todos los modulos registrados
    register_module(app)

    yield
    logger.info('shutdown backend')

    if DATABASE_PROVIDER is not None:
        # Cierra la conexión a la base de datos al detener la app
        await db_manager.stop_database()
