"""Exemplo rápido: 5 linhas para gerar mapa mental."""
from synapsis import generate

# Mock LLM para teste (substitua por Groq/OpenAI)
mock_llm = lambda p: 'title: "Demo"\nicon: "🎯"\ncolor: "#667eea"\nchildren:\n  - title: "Item"\n    icon: "📚"\n    color: "#4CAF50"'

# Gera HTML
path = generate("Inteligência Artificial", mock_llm, output="demo.html")
print(f"✅ Mapa gerado: {path}")
