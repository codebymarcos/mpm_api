# Synapsis

Gerador de mapas mentais com LLM injetável. Zero lock-in de provider.

## Instalação

```bash
pip install -e .
```

## Quickstart

```python
from synapsis import generate

# Qualquer função (prompt) -> response funciona
def my_llm(prompt: str) -> str:
    # Groq, OpenAI, Claude, Ollama, etc
    return "title: Teste\nicon: 🎯\nchildren:\n  - title: Item"

# Gera HTML standalone
path = generate("Python", my_llm, output="mapa.html")
```

## API

### `generate(topic, llm, output=None, style="", validate=True)`

Gera mapa mental completo.

- `topic`: Tema do mapa
- `llm`: Função `(str) -> str`
- `output`: Caminho do HTML (default: mindmap.html)
- `style`: Estilo/personalidade
- `validate`: Validar YAML (default: True)

### `SynapsisBuilder(llm)`

Builder para controle granular:

```python
from synapsis import SynapsisBuilder

builder = SynapsisBuilder(my_llm)
path = builder.expand("Python").validate().render("output.html")
```

## Providers

### Groq

```python
from groq import Groq
client = Groq(api_key="...")

def groq_llm(prompt):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

generate("AI", groq_llm)
```

### OpenAI

```python
from openai import OpenAI
client = OpenAI(api_key="...")

def openai_llm(prompt):
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

generate("AI", openai_llm)
```

## Filosofia

- **LLM Injection**: Qualquer `(prompt) -> response` funciona
- **HTML Standalone**: Abre direto no browser
- **Validação Robusta**: Limpa lixo de LLM automaticamente
- **Zero Lock-in**: Sem dependência de provider específico

## Testes

```bash
pip install -e ".[dev]"
pytest
```

## Licença

MIT
