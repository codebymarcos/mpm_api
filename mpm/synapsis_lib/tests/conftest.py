"""Fixtures e configuração de testes."""
import pytest
from pathlib import Path


FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def mock_llm():
    """LLM mock que retorna YAML válido."""
    def _llm(prompt: str) -> str:
        return '''title: "Teste"
icon: "🎯"
color: "#667eea"
children:
  - title: "Conceito 1"
    icon: "📚"
    color: "#4CAF50"
    children:
      - title: "Detalhe 1.1"
        icon: "📝"
        color: "#8BC34A"
  - title: "Conceito 2"
    icon: "⚡"
    color: "#2196F3"'''
    return _llm


@pytest.fixture
def mock_llm_with_fences():
    """LLM mock que retorna YAML com code fences."""
    def _llm(prompt: str) -> str:
        return '''```yaml
title: "Teste"
icon: "🎯"
color: "#667eea"
children:
  - title: "Item"
    icon: "📚"
```'''
    return _llm


@pytest.fixture
def valid_simple_yaml():
    """YAML válido simples."""
    return (FIXTURES_DIR / "valid_simple.yaml").read_text()


@pytest.fixture
def valid_complex_yaml():
    """YAML válido complexo."""
    return (FIXTURES_DIR / "valid_complex.yaml").read_text()


@pytest.fixture
def invalid_no_title_yaml():
    """YAML inválido sem title."""
    return (FIXTURES_DIR / "invalid_no_title.yaml").read_text()


@pytest.fixture
def invalid_children_type_yaml():
    """YAML inválido com children errado."""
    return (FIXTURES_DIR / "invalid_children_type.yaml").read_text()
