"""Exemplo com Groq como provider LLM."""
import os
from groq import Groq
from synapsis import generate

# Configura cliente Groq
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def groq_llm(prompt: str) -> str:
    """Wrapper Groq compatível com Synapsis."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Gera mapa mental
if __name__ == "__main__":
    topic = input("Tema: ") or "Python"
    path = generate(topic, groq_llm, output=f"{topic.lower().replace(' ', '_')}.html")
    print(f"✅ Mapa gerado: {path}")
