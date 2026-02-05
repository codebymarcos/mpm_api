"""Agentes de planejamento e expansão de mapas mentais."""
from .types import LLMFunc


class Planner:
    """Agente mestre: cria plano conciso em 2-3 níveis."""
    
    PROMPT = """
Você é um AGENTE MESTRE de Mapas Mentais.

Tarefa: Extrair conceitos PRINCIPAIS e estruturar mapa mental CONCISO.

FORMATO (YAML puro):
title: "Tema"
icon: "🎯"
children:
  - title: "Conceito 1"
    children:
      - title: "Detalhe"

REGRAS:
- APENAS YAML puro (sem ```, sem explicações)
- Máximo 3 palavras por título
- 2-3 níveis de profundidade
- Conceitos essenciais apenas
- Comece com "title:"

TEMA: {topic}

YAML:"""

    def __init__(self, llm: LLMFunc):
        self.llm = llm
    
    def create(self, topic: str) -> str:
        """Gera plano inicial do mapa mental."""
        prompt = self.PROMPT.format(topic=topic)
        return self.llm(prompt)


class Expander:
    """Agente expansor: transforma plano em mapa detalhado 5-7 níveis."""
    
    PROMPT = """
Você é um gerador AVANÇADO de mapas mentais em YAML PURO.
O output será parseado por js-yaml e renderizado em HTML.

CRÍTICO - RESPONDA APENAS YAML VÁLIDO:
- SEM blocos de código (```)
- SEM explicações
- SEM comentários
- Comece DIRETO com "title:"

ESTRUTURA (cada nó):
title: "Texto"        # máx 5 palavras
icon: "🎯"            # emoji relevante
color: "#HEX"         # cor hexadecimal
expanded: true        # opcional
children:             # sub-nós

PALETA DE CORES:
Nível 0: #667eea (roxo)
Nível 1: #4CAF50, #2196F3, #FF9800, #E91E63
Nível 2: #8BC34A, #64B5F6, #FFB74D, #F06292
Nível 3+: #AED581, #90CAF9, #FFCC80, #F48FB1

LAYOUT:
- 5-8 filhos por nó
- 4-5 níveis de profundidade
- Títulos descritivos
- Cores progressivas por nível

TEMA: {topic}
{plan_section}
{style_section}

GERE YAML EXPANSIVO E DETALHADO (começando com "title:"):"""

    def __init__(self, llm: LLMFunc):
        self.llm = llm
    
    def expand(self, topic: str, plan: str = "", style: str = "") -> str:
        """Expande tema/plano em mapa mental detalhado."""
        plan_section = f"PLANO BASE:\n{plan}" if plan else ""
        style_section = f"ESTILO: {style}" if style else ""
        
        prompt = self.PROMPT.format(
            topic=topic,
            plan_section=plan_section,
            style_section=style_section
        )
        return self.llm(prompt)
