# Synapsis - Mind Map Generator

Biblioteca para geração de mapas mentais com LLM injetável.

## Setup

```bash
cd synapsis_lib
pip install -e ".[dev]"
```

## Uso Rápido

```python
from synapsis import generate

# Com Groq
import os
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def groq_llm(prompt):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content

generate("Python", groq_llm, output="python.html")
```

## Estrutura

```
synapsis_lib/
├── synapsis/        # Biblioteca principal
├── templates/       # Template HTML pirâmide
├── tests/           # Testes pytest
└── examples/        # Exemplos de uso
```

Veja `synapsis_lib/README.md` para documentação completa.
