"""
utils/logs.py
Configuração centralizada de logging para a aplicação.
"""
import logging
import sys
from typing import Optional


def get_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """
    Retorna um logger configurado com o nome fornecido.

    Args:
        name: Nome do logger (geralmente __name__ do módulo chamador).
        level: Nível de log opcional; usa INFO por padrão.

    Returns:
        Instância de logging.Logger configurada.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(level if level is not None else logging.INFO)
    return logger
