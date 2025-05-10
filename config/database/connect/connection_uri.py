from typing import Optional
from config.database.connect.mysql_connect import mysql_get_connect
from config.database.connect.postgresql_connect import pg_get_connect


def get_connection_uri(provider) -> Optional[str]:
    """
    Obtener URI de conexión para cualquier proveedor de base de datos que se soporta
    :param provider: mysql, postgresql
    :return:
    """
    match provider:
        case 'mysql':
            return mysql_get_connect()
        case 'postgresql':
            return pg_get_connect()
        case _:
            return None
