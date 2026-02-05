# API Mapas Mentais

API profissional para gerar mapas mentais usando IA (Groq).

## 🏗️ Arquitetura

```
app/
├── config.py          # Configurações centralizadas
├── storage.py         # Gerenciamento de armazenamento
├── service.py         # Lógica de negócio
├── app.py             # Aplicação Flask com rotas
├── llm.py             # Interface com LLM (Groq)
├── index.html         # Interface web
└── data/              # Armazenamento de mapas
```

## 📋 Características

✅ **Arquitetura profissional** - Separação clara de responsabilidades  
✅ **Totalmente configurável** - Via variáveis de ambiente  
✅ **Tratamento de erros robusto** - Com logging detalhado  
✅ **API RESTful** - Endpoints bem documentados  
✅ **Interface web** - UI clean e responsiva  
✅ **Metadados** - Rastreamento completo de mapas  
✅ **Escalável** - Fácil de estender e manter  

## 🚀 Como Usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Crie ou edite `.env` na raiz do projeto:

```env
# Flask
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=5000

# LLM
GROQ_API_KEY=seu_api_key_aqui
LLM_TIMEOUT=60

# Armazenamento
MAX_MAPS=1000
RETENTION_DAYS=30
MAX_REQUEST_SIZE=1024
```

### 3. Iniciar a aplicação

```bash
cd app
python app.py
```

Acesse em: **http://localhost:5000**

## 📡 API Endpoints

### GET `/api/saude`
Verifica a saúde da API

**Resposta:**
```json
{
  "status": "ok",
  "versao": "1.0",
  "stats": {
    "total_mapas": 2,
    "tamanho_total_mb": 1.25,
    "limite_mapas": 1000
  }
}
```

### POST `/api/gerar`
Gera um novo mapa mental

**Request:**
```json
{
  "tema": "Inteligência Artificial"
}
```

**Resposta (201):**
```json
{
  "id": "uuid-123...",
  "tema": "Inteligência Artificial",
  "arquivo": "uuid-123....html",
  "tamanho": 45678,
  "criado": "2026-02-04T10:30:00",
  "links": {
    "preview": "/api/preview/uuid-123...",
    "download": "/api/download/uuid-123...",
    "info": "/api/info/uuid-123..."
  }
}
```

### GET `/api/info/<id>`
Obtém informações de um mapa

**Resposta:**
```json
{
  "id": "uuid-123...",
  "tema": "Inteligência Artificial",
  "arquivo": "uuid-123....html",
  "caminho": "/home/.../data/uuid-123....html",
  "tamanho": 45678,
  "criado": "2026-02-04T10:30:00"
}
```

### GET `/api/listar`
Lista todos os mapas

**Query params:**
- `limite` (default: 50) - Número máximo de mapas

**Resposta:**
```json
{
  "total": 2,
  "mapas": [
    {
      "id": "uuid-123...",
      "tema": "Python",
      "arquivo": "uuid-123....html",
      "tamanho": 45678,
      "criado": "2026-02-04T10:30:00"
    }
  ]
}
```

### GET `/api/preview/<id>`
Visualiza um mapa (retorna HTML)

### GET `/api/download/<id>`
Faz download de um mapa

### DELETE `/api/deletar/<id>`
Deleta um mapa

**Resposta (200):**
```json
{
  "id": "uuid-123...",
  "status": "deletado com sucesso"
}
```

### GET `/api/stats`
Obtém estatísticas

**Resposta:**
```json
{
  "total_mapas": 10,
  "tamanho_total_mb": 125.50,
  "limite_mapas": 1000
}
```

### GET `/docs`
Documentação da API em JSON

### GET `/`
Página principal da UI

## 💻 Exemplos de Uso

### Via curl

```bash
# Gerar mapa
curl -X POST http://localhost:5000/api/gerar \
  -H "Content-Type: application/json" \
  -d '{"tema": "Machine Learning"}'

# Listar mapas
curl http://localhost:5000/api/listar

# Obter info
curl http://localhost:5000/api/info/uuid-123

# Deletar mapa
curl -X DELETE http://localhost:5000/api/deletar/uuid-123

# Fazer download
curl -O http://localhost:5000/api/download/uuid-123
```

### Via Python

```python
import requests

# Gerar mapa
response = requests.post(
    "http://localhost:5000/api/gerar",
    json={"tema": "Data Science"}
)
data = response.json()
print(f"Mapa criado: {data['id']}")

# Listar
response = requests.get("http://localhost:5000/api/listar")
mapas = response.json()
print(f"Total de mapas: {mapas['total']}")
```

### Via JavaScript

```javascript
// Gerar mapa
const response = await fetch('/api/gerar', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ tema: 'Blockchain' })
});
const data = await response.json();
console.log(`Mapa: ${data.id}`);
```

## 🗂️ Estrutura de Dados

### Metadados (data/metadata.json)
```json
{
  "uuid-123...": {
    "id": "uuid-123...",
    "tema": "Python",
    "arquivo": "uuid-123....html",
    "caminho": "/app/data/uuid-123....html",
    "tamanho": 45678,
    "criado": "2026-02-04T10:30:00"
  }
}
```

## 🔧 Configurações Avançadas

### Aumentar limite de mapas
```env
MAX_MAPS=5000
```

### Aumentar timeout do LLM
```env
LLM_TIMEOUT=120
```

### Ativar debug mode
```env
FLASK_DEBUG=True
```

## 📝 Logging

A aplicação gera logs detalhados:

```
2026-02-04 10:30:00 - __main__ - INFO - Iniciando API - Host: 0.0.0.0, Port: 5000
2026-02-04 10:30:15 - service - INFO - Gerando mapa para tema: Python
2026-02-04 10:31:00 - service - INFO - Mapa gerado com sucesso: uuid-123...
```

## 🛡️ Tratamento de Erros

Todos os erros retornam JSON estruturado:

```json
{
  "erro": "Descrição do erro"
}
```

**Códigos HTTP:**
- `201` - Recurso criado com sucesso
- `400` - Requisição inválida
- `404` - Recurso não encontrado
- `500` - Erro interno do servidor

## 📦 Dependências

- `flask` - Framework web
- `python-dotenv` - Gerenciamento de variáveis de ambiente
- `groq` - Cliente LLM (do arquivo llm.py)
- `synapsis` - Geração de mapas mentais (do arquivo llm.py)

## 🧹 Manutenção

### Limpar mapas antigos
```bash
# Via API
curl -X DELETE http://localhost:5000/api/deletar/uuid-123
```

### Monitorar uso
```bash
# Verificar saúde
curl http://localhost:5000/api/saude

# Ver estatísticas
curl http://localhost:5000/api/stats
```

## 📊 Performance

- Tempo de geração: Depende do tema (tipicamente 30-60s)
- Tamanho típico: 50-100 KB por mapa
- Limite: Configurável via `MAX_MAPS`

## 🚦 Status da API

Acesse `/api/saude` para verificar o status:

```bash
curl http://localhost:5000/api/saude
```

---

**Versão:** 1.0  
**Última atualização:** 2026-02-04
