import os
from typing import Optional
from loguru import logger


def mysql_get_connect() -> Optional[str]:
    """
    Obtiene la URI de conexión para MYSQL
    :return:
    """
    mysql_driver = 'mysql+aiomysql'
    mysql_db = os.environ.get("MYSQL_DB", None)
    mysql_username = os.environ.get("MYSQL_USERNAME", None)
    mysql_password = os.environ.get("MYSQL_PASSWORD", None)
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    mysql_host = os.environ.get('MYSQL_HOST', '127.0.0.1')

    conn = f'{mysql_driver}://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'
    return conn
