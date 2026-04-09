"""
Módulo de modelos compartilhados.

Contém a classe base `BaseModel` e as abstrações de repositório
reutilizáveis por todas as features. Modelos específicos de cada
feature devem ficar dentro de `src/features/<feature>/models/`.
"""

from src.models.base import BaseModel

__all__ = [
    "BaseModel",
]
