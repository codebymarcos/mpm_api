"""Validador e sanitizador de YAML."""
import re
from typing import Tuple
import yaml


class ValidationError(Exception):
    """Erro de validação do YAML."""
    pass


def sanitize(raw: str) -> str:
    """Remove lixo de LLM: code blocks, comentários, whitespace."""
    text = raw.strip()
    
    # Remove ```yaml ou ``` no início
    text = re.sub(r'^```(?:yaml|yml)?\s*\n?', '', text)
    # Remove ``` no final
    text = re.sub(r'\n?```\s*$', '', text)
    
    # Remove linhas de comentário puro (mas preserva inline para YAML válido)
    lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        lines.append(line)
    
    return '\n'.join(lines).strip()


def validate_schema(yaml_str: str) -> Tuple[bool, list]:
    """Valida estrutura YAML do mapa mental. Retorna (válido, erros)."""
    errors = []
    
    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        return False, [f"YAML inválido: {e}"]
    
    if not isinstance(data, dict):
        return False, ["Raiz deve ser um dicionário"]
    
    def check_node(node: dict, path: str = "root") -> None:
        if "title" not in node:
            errors.append(f"{path}: campo 'title' obrigatório")
        
        if "children" in node:
            if not isinstance(node["children"], list):
                errors.append(f"{path}: 'children' deve ser lista")
            else:
                for i, child in enumerate(node["children"]):
                    if isinstance(child, dict):
                        check_node(child, f"{path}.children[{i}]")
                    else:
                        errors.append(f"{path}.children[{i}]: deve ser dicionário")
    
    check_node(data)
    return len(errors) == 0, errors


def clean_and_validate(raw: str) -> str:
    """Sanitiza e valida YAML. Levanta ValidationError se inválido."""
    cleaned = sanitize(raw)
    valid, errors = validate_schema(cleaned)
    
    if not valid:
        raise ValidationError(f"YAML inválido: {'; '.join(errors)}")
    
    return cleaned
