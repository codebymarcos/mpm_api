"""Exemplo de geração em lote."""
from pathlib import Path
from synapsis import generate, SynapsisBuilder

# Mock LLM para teste
def mock_llm(prompt: str) -> str:
    topic = "Tema" 
    for word in ["Python", "JavaScript", "Rust", "Go"]:
        if word.lower() in prompt.lower():
            topic = word
            break
    
    return f'''title: "{topic}"
icon: "🎯"
color: "#667eea"
children:
  - title: "Fundamentos"
    icon: "📚"
    color: "#4CAF50"
    children:
      - title: "Sintaxe"
        icon: "📝"
        color: "#8BC34A"
      - title: "Tipos"
        icon: "🔢"
        color: "#8BC34A"
  - title: "Avançado"
    icon: "⚡"
    color: "#2196F3"'''


def batch_generate(topics: list, output_dir: str = "output"):
    """Gera múltiplos mapas em lote."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    results = []
    for topic in topics:
        filename = f"{topic.lower().replace(' ', '_')}.html"
        path = generate(topic, mock_llm, output=str(output_path / filename))
        results.append(path)
        print(f"✅ {topic}: {path}")
    
    return results


if __name__ == "__main__":
    topics = ["Python", "JavaScript", "Rust", "Go"]
    paths = batch_generate(topics)
    print(f"\n🎉 {len(paths)} mapas gerados!")
