"""Core da biblioteca Synapsis: Builder e função generate."""
from pathlib import Path
from typing import Optional

from .types import LLMFunc
from .agents import Planner, Expander
from .validator import clean_and_validate, ValidationError
from .renderer import render_html


class SynapsisBuilder:
    """Builder para criar mapas mentais com LLM injetável."""
    
    def __init__(self, llm: LLMFunc):
        self.llm = llm
        self.planner = Planner(llm)
        self.expander = Expander(llm)
        self._yaml: Optional[str] = None
    
    def plan(self, topic: str) -> "SynapsisBuilder":
        """Cria plano inicial (2-3 níveis)."""
        self._yaml = self.planner.create(topic)
        return self
    
    def expand(self, topic: str, style: str = "") -> "SynapsisBuilder":
        """Expande para mapa detalhado (5-7 níveis)."""
        plan = self._yaml or ""
        self._yaml = self.expander.expand(topic, plan, style)
        return self
    
    def validate(self) -> "SynapsisBuilder":
        """Sanitiza e valida YAML."""
        if self._yaml:
            self._yaml = clean_and_validate(self._yaml)
        return self
    
    def render(self, output: str = None) -> str:
        """Renderiza HTML e retorna caminho do arquivo."""
        if not self._yaml:
            raise ValueError("Nenhum YAML para renderizar")
        return render_html(self._yaml, output)
    
    def get_yaml(self) -> str:
        """Retorna YAML atual."""
        return self._yaml or ""
    
    def plan_and_expand(self, topic: str, style: str = "") -> str:
        """Atalho: planeja e expande em uma chamada."""
        self.expand(topic, style=style)
        self.validate()
        return self._yaml


def generate(
    topic: str,
    llm: LLMFunc,
    output: str = None,
    style: str = "",
    validate: bool = True
) -> str:
    """Gera mapa mental completo e retorna caminho do HTML.
    
    Args:
        topic: Tema do mapa mental
        llm: Função LLM (prompt -> response)
        output: Caminho do HTML de saída (default: mindmap.html)
        style: Estilo/personalidade do mapa
        validate: Se deve validar YAML (default: True)
    
    Returns:
        Caminho absoluto do HTML gerado
    """
    builder = SynapsisBuilder(llm)
    builder.expand(topic, style=style)
    
    if validate:
        builder.validate()
    
    return builder.render(output)
