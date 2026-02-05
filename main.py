"""Teste de uso: gera mapa mental com Groq."""
import os
import sys
from pathlib import Path


from dotenv import load_dotenv
from groq import Groq
from synapsis import generate

# Carrega .env da raiz
load_dotenv()

# Cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def groq_llm(prompt: str) -> str:
    """Wrapper Groq compatível com Synapsis."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def gerar_mapa_mental(tema: str, output_dir: str = None, filename: str = None) -> Path:
    """Gera mapa mental com Groq e Synapsis."""
    if filename is None:
        filename = f"{tema.lower().replace(' ', '_')}_map.html"
    
    if output_dir is not None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        output = str(output_path / filename)
    else:
        output = filename
    
    print(f"🧠 Gerando mapa mental: {tema}")
    path = generate(tema, groq_llm, output=output)
    print(f"✅ Mapa salvo: {path}")
    return path


if __name__ == "__main__":
    tema = sys.argv[1] if len(sys.argv) > 1 else "como criar um banco de dados em Python do zero"
    gerar_mapa_mental(tema)
