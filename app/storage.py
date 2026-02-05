"""Gerenciamento de armazenamento."""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from config import Config


class StorageManager:
    """Gerencia armazenamento de mapas mentais."""
    
    METADATA_FILE = "metadata.json"
    
    def __init__(self):
        self.data_dir = Config.DATA_DIR
        self.metadata_file = self.data_dir / self.METADATA_FILE
        self._load_metadata()
    
    def _load_metadata(self) -> Dict:
        """Carrega metadados existentes."""
        if self.metadata_file.exists():
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    def _save_metadata(self, metadata: Dict) -> None:
        """Salva metadados em arquivo."""
        with open(self.metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def save_map(self, map_id: str, tema: str, filepath: str) -> Dict:
        """Salva informações de um mapa mental.
        
        Args:
            map_id: ID único do mapa
            tema: Tema do mapa
            filepath: Caminho do arquivo HTML
            
        Returns:
            Dict com metadados do mapa salvo
        """
        metadata = self._load_metadata()
        
        map_info = {
            "id": map_id,
            "tema": tema,
            "arquivo": Path(filepath).name,
            "caminho": str(filepath),
            "tamanho": Path(filepath).stat().st_size,
            "criado": datetime.now().isoformat(),
        }
        
        metadata[map_id] = map_info
        self._save_metadata(metadata)
        
        return map_info
    
    def get_map(self, map_id: str) -> Optional[Dict]:
        """Obtém informações de um mapa.
        
        Args:
            map_id: ID do mapa
            
        Returns:
            Dict com metadados ou None se não encontrado
        """
        metadata = self._load_metadata()
        return metadata.get(map_id)
    
    def list_maps(self, limit: int = 100) -> List[Dict]:
        """Lista todos os mapas salvos.
        
        Args:
            limit: Número máximo de mapas a retornar
            
        Returns:
            Lista de mapas ordenados por data (mais recentes primeiro)
        """
        metadata = self._load_metadata()
        maps = sorted(
            metadata.values(),
            key=lambda x: x["criado"],
            reverse=True
        )
        return maps[:limit]
    
    def delete_map(self, map_id: str) -> bool:
        """Deleta um mapa.
        
        Args:
            map_id: ID do mapa
            
        Returns:
            True se deletado com sucesso, False caso contrário
        """
        metadata = self._load_metadata()
        
        if map_id not in metadata:
            return False
        
        map_info = metadata[map_id]
        filepath = Path(map_info["caminho"])
        
        # Delete arquivo
        if filepath.exists():
            filepath.unlink()
        
        # Remove metadata
        del metadata[map_id]
        self._save_metadata(metadata)
        
        return True
    
    def get_stats(self) -> Dict:
        """Obtém estatísticas de armazenamento.
        
        Returns:
            Dict com estatísticas
        """
        metadata = self._load_metadata()
        total_size = sum(
            Path(info["caminho"]).stat().st_size
            for info in metadata.values()
            if Path(info["caminho"]).exists()
        )
        
        return {
            "total_mapas": len(metadata),
            "tamanho_total_mb": round(total_size / (1024 * 1024), 2),
            "limite_mapas": Config.MAX_MAPS,
        }
