"""Teste de uso: gera mapa mental com Groq."""
import os
import sys
from pathlib import Path

# Adiciona synapsis ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from groq import Groq
from synapsis import generate

# Carrega .env da raiz
load_dotenv(Path(__file__).parent.parent.parent / ".env")

# Cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def groq_llm(prompt: str) -> str:
    """Wrapper Groq compatível com Synapsis."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    tema = sys.argv[1] if len(sys.argv) > 1 else "Python"
    output = f"{tema.lower().replace(' ', '_')}_map.html"
    
    print(f"🧠 Gerando mapa mental: {tema}")
    path = generate(tema, groq_llm, output=output)
    print(f"✅ Mapa salvo: {path}")
