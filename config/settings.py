# -*- coding: utf-8 -*-
import os
from typing import Optional

# Define el tipo de logger a utilizar en la aplicación.
# Los valores típicos podrían ser 'default' para un logger con formato estándar (útil en desarrollo local)
# o 'cloud' para un logger con formato específico para entornos de nube.
DEFAULT_LOGGER: str = os.environ.get('DEFAULT_LOGGER', 'default')

# Prefijo global para todos los endpoints de la API. Puede ser,"" si no se necesita prefijo global.
ENDPOINT_API: str = '/api'

# Lists the applications that are installed and active in the project.
INSTALLED_MODULES: list[str] = [
    'apps.home'
]

# Configuración para CORS (Cross-Origin Resource Sharing).
# Define qué orígenes, métodos y cabeceras están permitidos.
CORS_CONFIG = {
    "ALLOW_METHODS": ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
    "ALLOW_ORIGINS": ['*'],
    "ALLOW_HEADERS": ['*']
}

# Proveedor de base de datos por defecto utilizando SQLModel.
# Valores permitidos podrían ser, por ejemplo: 'postgresql', 'mysql', 'sqlite'.
DATABASE_PROVIDER: Optional[str] = os.environ.get('DATABASE_PROVIDER', None)

# Configuración
USE_SECWEB = os.environ.get('USE_SECWEB', 'false').lower() in ('true', '1', 'yes', 'on')

