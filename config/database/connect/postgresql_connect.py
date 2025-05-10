import os
from typing import Optional
from loguru import logger


def pg_get_connect() -> Optional[str]:
    """
    Obtiene la URI de conexión para Postgresql
    :return:
    """
    pg_driver = 'postgresql+asyncpg'
    pg_db = os.environ.get("POSTGRESQL_DB", None)
    pg_username = os.environ.get("POSTGRESQL_USERNAME", None)
    pg_password = os.environ.get("POSTGRESQL_PASSWORD", None)
    pg_port = os.environ.get('POSTGRESQL_PORT', '5432')
    pg_host = os.environ.get('POSTGRESQL_HOST', '127.0.0.1')

    conn = f'{pg_driver}://{pg_username}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'
    return conn
