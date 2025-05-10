# -*- coding: utf-8 -*-
from typing import AsyncGenerator
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from loguru import logger

# Variable global para almacenar la instancia del motor (Engine)
# Se inicializará en init_database
_engine: Optional[AsyncEngine] = None

# Variable global para almacenar el creador de sesiones (SessionMaker)
# Se inicializará en e init_database
_async_session_maker: Optional[sessionmaker] = None


class DatabaseManager:
    """
    Gestiona la conexión y sesiones de la base de datos de forma asíncrona.
    """

    def __init__(self):
        self.engine: Optional[AsyncEngine] = _engine
        self.async_session_maker: Optional[sessionmaker] = _async_session_maker

    async def init_database(self, db_uri: str):
        """Inicializa la conexión a la base de datos.

        Parameters:
            db_uri (str): La URI de conexión a la base de datos.
        """
        global _engine, _async_session_maker

        if self.engine is not None:
            logger.info('La conexión a la base de datos ya está inicializada.')
            return

        try:
            logger.info(f"Inicializando conexión a la base de datos con URL: ...{db_uri[db_uri.find('@') + 1:]}")

            # Crea el motor asíncrono. echo=True mostrará las queries SQL ejecutadas (útil para debug)
            self.engine = create_async_engine(db_uri, echo=True, future=True)
            _engine = self.engine

            # Crea un creador de sesiones asíncronas vinculado al motor
            # expire_on_commit=False evita que los objetos se desvinculen de la sesión después de un commit
            self.async_session_maker = sessionmaker(
                bind=self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,  # Desactiva el autoflush para control manual si es necesario
            )
            _async_session_maker = self.async_session_maker

            logger.info("Conexión a la base de datos inicializada exitosamente.")
        except Exception as e:
            logger.error(f'Error al inicializar la base de datos: {e}')
            raise

    async def stop_database(self):
        """
        Cierra la conexión a la base de datos (dispose del engine).
        """
        global _engine, _async_session_maker
        if self.engine:
            logger.info("Cerrando la conexión a la base de datos...")
            # Cierra todas las conexiones del pool de forma segura
            await self.engine.dispose()
            self.engine = None
            self.async_session_maker = None
            _engine = None
            _async_session_maker = None
            logger.info("Conexión a la base de datos cerrada.")
        else:
            logger.error("No hay conexión activa a la base de datos para cerrar.")

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Generador asíncrono para obtener una sesión de base de datos.

        Este mr usado como una dependencia en FastAPI (`Depends`).
        Maneja automáticamente el ciclo de vida de la sesión (inicio, commit/rollback, cierre).

        Yields:
            AsyncSession: Una sesión de base de datos asíncrona.

        Raises:
            RuntimeError: Si el gestor de base de datos no ha sido inicializado.
        """
        if self.async_session_maker is None:
            message = "El gestor de base de datos no ha sido inicializado. Llama a 'init_database' primero."
            logger.error(message)
            raise RuntimeError(message)

        # crea una nueva sesión asíncrona
        async with self.async_session_maker() as session:
            try:
                # Entrega la sesión al endpoint de FastAPI
                yield session
                # Si el endpoint finaliza sin errores, confirma la transacción
                await session.commit()
            except Exception as e:
                message = f"Error en la sesión, revirtiendo cambios: {e}"
                logger.error(message)
                await session.rollback()
                raise
            finally:
                # La sesión se cierra automáticamente al salir del bloque 'async with'
                pass  # No es necesario session.close() explícito aquí


# Se crea una única instancia que se usará en toda la aplicación
db_manager = DatabaseManager()


async def get_bd_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependencia de FastAPI para obtener una sesión de BD."""
    async for session in db_manager.get_session():
        yield session

