import os
import sys
from loguru import logger
from config.settings import DEFAULT_LOGGER


def start_logger():
    is_default = DEFAULT_LOGGER == 'default'
    # Formato de log
    format_log_default = '🚀[{time:HH:mm:ss}]<level>{level} »</level> <level>{message}</level> {name}@{function} at {line}'
    format_log_cloud = '<level>{level}:</level> {message}'

    # Configuración de logger
    logger_configuration = {
        'handlers': [
            {
                'colorize': is_default,
                'sink': sys.stdout,
                'format': format_log_default if is_default else format_log_cloud
            }
        ]
    }

    logger.configure(**logger_configuration)

    logger.configure(**logger_configuration)

    # Agregar niveles de log personalizados (sin redefinir los existentes)
    custom_levels = [
        ("SUCCESS", 25, "<green>", "✅"),
        ("WARNING", 30, "<yellow>", "⚠️"),
        ("ERROR", 40, "<red>", "🔥"),
        ("CRITICAL", 50, "<bold red>", "💀"),
    ]

    for name, level_no, color, icon in custom_levels:
        if not logger.level(name):  # Evita redefinir niveles
            logger.level(name, no=level_no, color=color, icon=icon)

    logger.info("🛠️ Logger inicializado correctamente.")
