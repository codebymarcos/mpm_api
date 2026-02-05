"""Exemplo com OpenAI como provider LLM."""
import os
from openai import OpenAI
from synapsis import generate

# Configura cliente OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def openai_llm(prompt: str) -> str:
    """Wrapper OpenAI compatível com Synapsis."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Gera mapa mental
if __name__ == "__main__":
    topic = input("Tema: ") or "Machine Learning"
    path = generate(topic, openai_llm, output=f"{topic.lower().replace(' ', '_')}.html")
    print(f"✅ Mapa gerado: {path}")
