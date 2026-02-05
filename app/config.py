"""Configurações da aplicação."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv(Path(__file__).parent.parent / ".env")


class Config:
    """Configurações da aplicação."""
    
    # Diretório base
    BASE_DIR = Path(__file__).parent
    DATA_DIR = BASE_DIR / "data"
    
    # Flask
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    PORT = int(os.getenv("FLASK_PORT", 5000))
    
    # LLM
    LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", 60))
    
    # Armazenamento
    MAX_MAPS = int(os.getenv("MAX_MAPS", 1000))
    RETENTION_DAYS = int(os.getenv("RETENTION_DAYS", 30))
    
    # API
    MAX_REQUEST_SIZE = int(os.getenv("MAX_REQUEST_SIZE", 1024))  # caracteres
    
    @classmethod
    def init(cls):
        """Inicializa configurações."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)


# Inicializa ao importar
Config.init()
