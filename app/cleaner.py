"""Serviço de limpeza de dados antigos."""
import logging
import threading
from datetime import datetime, timedelta
from pathlib import Path
from storage import StorageManager
from config import Config

logger = logging.getLogger(__name__)


class CleanupService:
    """Serviço de limpeza periódica de dados."""
    
    def __init__(self):
        self.storage = StorageManager()
        self.running = False
        self.thread = None
    
    def iniciar(self, intervalo_minutos: int = 5):
        """Inicia o serviço de limpeza em background.
        
        Args:
            intervalo_minutos: Intervalo entre limpezas em minutos
        """
        if self.running:
            logger.warning("Serviço de limpeza já está em execução")
            return
        
        self.running = True
        intervalo_segundos = intervalo_minutos * 60
        
        self.thread = threading.Thread(
            target=self._loop_limpeza,
            args=(intervalo_segundos,),
            daemon=True
        )
        self.thread.start()
        logger.info(f"Serviço de limpeza iniciado (intervalo: {intervalo_minutos}m)")
    
    def parar(self):
        """Para o serviço de limpeza."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Serviço de limpeza parado")
    
    def _loop_limpeza(self, intervalo_segundos: int):
        """Loop de limpeza periódica.
        
        Args:
            intervalo_segundos: Intervalo em segundos
        """
        while self.running:
            try:
                self.limpar_antigos()
                self.limpar_orfaos()
            except Exception as e:
                logger.error(f"Erro durante limpeza: {str(e)}")
            
            # Aguarda próxima limpeza
            for _ in range(intervalo_segundos):
                if not self.running:
                    break
                threading.Event().wait(1)
    
    def limpar_antigos(self) -> dict:
        """Limpa mapas mais antigos que RETENTION_DAYS.
        
        Returns:
            Dict com estatísticas de limpeza
        """
        metadata = self.storage._load_metadata()
        limite_dias = Config.RETENTION_DAYS
        data_limite = datetime.now() - timedelta(days=limite_dias)
        
        deletados = []
        
        for map_id, map_info in list(metadata.items()):
            try:
                data_criacao = datetime.fromisoformat(map_info["criado"])
                
                if data_criacao < data_limite:
                    filepath = Path(map_info["caminho"])
                    
                    # Deleta arquivo
                    if filepath.exists():
                        filepath.unlink()
                    
                    # Remove metadata
                    del metadata[map_id]
                    deletados.append(map_id)
                    logger.debug(f"Mapa antigo deletado: {map_id}")
            
            except Exception as e:
                logger.error(f"Erro ao processar mapa {map_id}: {str(e)}")
        
        if deletados:
            self.storage._save_metadata(metadata)
            logger.info(f"Limpeza concluída: {len(deletados)} mapas antigos removidos")
        
        return {
            "tipo": "antigos",
            "total_deletados": len(deletados),
            "dias_retencao": limite_dias,
            "ids_deletados": deletados
        }
    
    def limpar_orfaos(self) -> dict:
        """Limpa metadados de arquivos que não existem.
        
        Returns:
            Dict com estatísticas de limpeza
        """
        metadata = self.storage._load_metadata()
        deletados = []
        
        for map_id, map_info in list(metadata.items()):
            filepath = Path(map_info["caminho"])
            
            # Se arquivo não existe mas metadata está registrada
            if not filepath.exists():
                del metadata[map_id]
                deletados.append(map_id)
                logger.debug(f"Metadata órfã deletada: {map_id}")
        
        if deletados:
            self.storage._save_metadata(metadata)
            logger.info(f"Metadados órfãos removidos: {len(deletados)}")
        
        return {
            "tipo": "orfaos",
            "total_deletados": len(deletados),
            "ids_deletados": deletados
        }
    
    def obter_status(self) -> dict:
        """Obtém status do serviço de limpeza.
        
        Returns:
            Dict com status
        """
        return {
            "ativo": self.running,
            "retention_days": Config.RETENTION_DAYS,
            "data_dir": str(Config.DATA_DIR)
        }
