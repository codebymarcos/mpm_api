"""API Flask para geração de mapas mentais."""
import logging
from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.exceptions import HTTPException
from service import MapaService
from cleaner import CleanupService
from config import Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializar aplicação
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Serviço
service = MapaService()
cleaner = CleanupService()


# ============================================================================
# Tratamento de erros
# ============================================================================

@app.errorhandler(400)
def bad_request(error):
    """Erro 400: Requisição inválida."""
    return jsonify({"erro": "Requisição inválida"}), 400


@app.errorhandler(404)
def not_found(error):
    """Erro 404: Recurso não encontrado."""
    return jsonify({"erro": "Recurso não encontrado"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Erro 500: Erro interno do servidor."""
    logger.error(f"Erro interno: {str(error)}")
    return jsonify({"erro": "Erro interno do servidor"}), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handler genérico para exceções."""
    if isinstance(error, HTTPException):
        return error
    
    logger.error(f"Exceção não tratada: {str(error)}")
    return jsonify({"erro": "Erro ao processar requisição"}), 500


# ============================================================================
# Rotas da API
# ============================================================================

@app.route("/api/saude", methods=["GET"])
def saude():
    """Verifica saúde da API.
    
    Returns:
        Status da aplicação
    """
    stats = service.obter_stats()
    return jsonify({
        "status": "ok",
        "versao": "1.0",
        "stats": stats
    }), 200


@app.route("/api/gerar", methods=["POST"])
def gerar():
    """Gera um novo mapa mental.
    
    Recebe:
        {
            "tema": "seu tema aqui"
        }
    
    Retorna:
        {
            "id": "uuid",
            "tema": "...",
            "arquivo": "...",
            "criado": "2026-02-04T...",
            "links": {
                "preview": "/api/preview/id",
                "download": "/api/download/id",
                "info": "/api/info/id"
            }
        }
    """
    try:
        dados = request.get_json()
        
        if not dados or "tema" not in dados:
            return jsonify({"erro": "Campo 'tema' obrigatório"}), 400
        
        tema = dados["tema"]
        map_id, map_info = service.gerar_mapa(tema)
        
        return jsonify({
            "id": map_id,
            "tema": map_info["tema"],
            "arquivo": map_info["arquivo"],
            "tamanho": map_info["tamanho"],
            "criado": map_info["criado"],
            "links": {
                "preview": f"/api/preview/{map_id}",
                "download": f"/api/download/{map_id}",
                "info": f"/api/info/{map_id}"
            }
        }), 201
    
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/info/<map_id>", methods=["GET"])
def obter_info(map_id):
    """Obtém informações de um mapa.
    
    Retorna:
        Metadados do mapa
    """
    try:
        map_info = service.obter_mapa(map_id)
        return jsonify(map_info), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@app.route("/api/listar", methods=["GET"])
def listar():
    """Lista mapas salvos.
    
    Query params:
        limite: número máximo de mapas (default: 50)
    
    Retorna:
        Lista de mapas com metadados
    """
    try:
        limite = request.args.get("limite", 50, type=int)
        mapas = service.listar_mapas(limite=limite)
        
        return jsonify({
            "total": len(mapas),
            "mapas": mapas
        }), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


@app.route("/api/preview/<map_id>", methods=["GET"])
def preview(map_id):
    """Visualiza um mapa (serve o HTML).
    
    Retorna:
        Arquivo HTML do mapa
    """
    try:
        filepath = service.obter_arquivo(map_id)
        return send_file(filepath, mimetype="text/html")
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@app.route("/api/download/<map_id>", methods=["GET"])
def download(map_id):
    """Faz download de um mapa.
    
    Retorna:
        Arquivo HTML para download
    """
    try:
        filepath = service.obter_arquivo(map_id)
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"mapa_mental_{map_id}.html",
            mimetype="text/html"
        )
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@app.route("/api/deletar/<map_id>", methods=["DELETE"])
def deletar(map_id):
    """Deleta um mapa.
    
    Retorna:
        Confirmação de exclusão
    """
    try:
        service.deletar_mapa(map_id)
        return jsonify({
            "id": map_id,
            "status": "deletado com sucesso"
        }), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 404


@app.route("/api/stats", methods=["GET"])
def stats():
    """Obtém estatísticas da aplicação.
    
    Retorna:
        Estatísticas gerais
    """
    try:
        stats_data = service.obter_stats()
        return jsonify(stats_data), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500


# ============================================================================
# Rotas da UI
# ============================================================================

@app.route("/", methods=["GET"])
def index():
    """Retorna página principal."""
    return send_from_directory(".", "index.html")


# ============================================================================
# Documentação da API
# ============================================================================

@app.route("/docs", methods=["GET"])
def docs():
    """Retorna documentação da API."""
    return jsonify({
        "nome": "API Mapas Mentais",
        "versao": "1.0",
        "descricao": "API para gerar mapas mentais usando IA",
        "base_url": request.host_url.rstrip("/"),
        "endpoints": {
            "GET /api/saude": "Verifica saúde da API",
            "POST /api/gerar": "Gera novo mapa mental",
            "GET /api/info/<id>": "Obtém info de um mapa",
            "GET /api/listar": "Lista todos os mapas",
            "GET /api/preview/<id>": "Visualiza um mapa",
            "GET /api/download/<id>": "Faz download de um mapa",
            "DELETE /api/deletar/<id>": "Deleta um mapa",
            "GET /api/stats": "Obtém estatísticas",
            "GET /docs": "Documentação da API"
        },
        "exemplo_gerar": {
            "metodo": "POST",
            "url": "/api/gerar",
            "headers": {"Content-Type": "application/json"},
            "body": {"tema": "Inteligência Artificial"}
        }
    }), 200


if __name__ == "__main__":
    logger.info(f"Iniciando API - Host: {Config.HOST}, Port: {Config.PORT}")
    
    # Iniciar serviço de limpeza
    cleaner.iniciar(intervalo_minutos=5)
    logger.info("Serviço de limpeza automática ativado (a cada 5 minutos)")
    
    try:
        app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
    finally:
        cleaner.parar()
