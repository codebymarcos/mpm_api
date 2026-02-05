"""Synapsis - Biblioteca para geração de mapas mentais com LLM."""

__version__ = "1.0.0"

from .types import LLMFunc, MindMapNode, ValidationResult
from .core import generate, SynapsisBuilder
from .validator import sanitize, validate_schema, clean_and_validate, ValidationError
from .agents import Planner, Expander
from .renderer import render_html

__all__ = [
    "generate",
    "SynapsisBuilder",
    "LLMFunc",
    "MindMapNode",
    "ValidationResult",
    "sanitize",
    "validate_schema",
    "clean_and_validate",
    "ValidationError",
    "Planner",
    "Expander",
    "render_html",
]
