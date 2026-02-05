"""Tipos base da biblioteca Synapsis."""
from typing import Callable, TypedDict, List, Optional

# Função LLM: recebe prompt, retorna resposta
LLMFunc = Callable[[str], str]


class MindMapNode(TypedDict, total=False):
    """Estrutura de um nó do mapa mental."""
    title: str
    icon: str
    color: str
    expanded: bool
    children: List["MindMapNode"]


class ValidationResult(TypedDict):
    """Resultado da validação YAML."""
    valid: bool
    errors: List[str]
    cleaned: Optional[str]
