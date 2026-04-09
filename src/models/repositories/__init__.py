"""
Módulo de repositórios compartilhados.

Contém as abstrações base do padrão Repository que podem ser
reutilizadas por repositórios específicos de cada feature.
"""

from src.models.repositories.base import BaseRepository, JsonFileRepository

__all__ = [
    "BaseRepository",
    "JsonFileRepository",
]
