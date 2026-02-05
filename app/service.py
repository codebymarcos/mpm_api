"""Serviço de geração de mapas mentais."""
import uuid
import logging
from pathlib import Path
from typing import Tuple
from llm import gerar_mapa_mental
from storage import StorageManager
from config import Config


logger = logging.getLogger(__name__)


class MapaService:
    """Serviço de geração e gerenciamento de mapas mentais."""
    
    def __init__(self):
        self.storage = StorageManager()
    
    def gerar_mapa(self, tema: str) -> Tuple[str, dict]:
        """Gera um novo mapa mental.
        
        Args:
            tema: Tema para o mapa mental
            
        Returns:
            Tuple com (map_id, info_dict)
            
        Raises:
            ValueError: Se tema for inválido
            RuntimeError: Se houver erro ao gerar mapa
        """
        # Validação
        tema = tema.strip()
        if not tema:
            raise ValueError("Tema não pode estar vazio")
        
        if len(tema) > Config.MAX_REQUEST_SIZE:
            raise ValueError(f"Tema muito longo (máx {Config.MAX_REQUEST_SIZE} caracteres)")
        
        # Verificar limite
        stats = self.storage.get_stats()
        if stats["total_mapas"] >= Config.MAX_MAPS:
            raise RuntimeError(f"Limite de {Config.MAX_MAPS} mapas atingido")
        
        try:
            # Gera ID único
            map_id = str(uuid.uuid4())
            filename = f"{map_id}.html"
            
            # Gera mapa
            logger.info(f"Gerando mapa para tema: {tema}")
            caminho = gerar_mapa_mental(
                tema=tema,
                output_dir=str(Config.DATA_DIR),
                filename=filename
            )
            
            # Salva metadados
            map_info = self.storage.save_map(map_id, tema, str(caminho))
            logger.info(f"Mapa gerado com sucesso: {map_id}")
            
            return map_id, map_info
        
        except Exception as e:
            logger.error(f"Erro ao gerar mapa: {str(e)}")
            raise RuntimeError(f"Erro ao gerar mapa: {str(e)}")
    
    def obter_mapa(self, map_id: str) -> dict:
        """Obtém informações de um mapa.
        
        Args:
            map_id: ID do mapa
            
        Returns:
            Dict com informações do mapa
            
        Raises:
            ValueError: Se mapa não for encontrado
        """
        map_info = self.storage.get_map(map_id)
        if not map_info:
            raise ValueError(f"Mapa {map_id} não encontrado")
        return map_info
    
    def listar_mapas(self, limite: int = 50) -> list:
        """Lista mapas salvos.
        
        Args:
            limite: Número máximo de mapas
            
        Returns:
            Lista de mapas
        """
        return self.storage.list_maps(limit=limite)
    
    def deletar_mapa(self, map_id: str) -> bool:
        """Deleta um mapa.
        
        Args:
            map_id: ID do mapa
            
        Returns:
            True se deletado com sucesso
            
        Raises:
            ValueError: Se mapa não for encontrado
        """
        if not self.storage.delete_map(map_id):
            raise ValueError(f"Mapa {map_id} não encontrado")
        logger.info(f"Mapa deletado: {map_id}")
        return True
    
    def obter_arquivo(self, map_id: str) -> Path:
        """Obtém caminho do arquivo de um mapa.
        
        Args:
            map_id: ID do mapa
            
        Returns:
            Path do arquivo
            
        Raises:
            ValueError: Se mapa não for encontrado
        """
        map_info = self.obter_mapa(map_id)
        filepath = Path(map_info["caminho"])
        
        if not filepath.exists():
            raise ValueError(f"Arquivo do mapa {map_id} não existe")
        
        return filepath
    
    def obter_stats(self) -> dict:
        """Obtém estatísticas.
        
        Returns:
            Dict com estatísticas
        """
        return self.storage.get_stats()
