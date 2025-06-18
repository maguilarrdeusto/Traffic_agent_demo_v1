"""
Rutas para verificar el estado de la aplicación y las APIs externas.
"""
from flask import Blueprint, jsonify
from src.utils.api_client import ApiClient

# Crear el blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint para verificar el estado de la aplicación y las APIs externas.
    
    Returns:
        Estado de la aplicación y las APIs
    """
    # Verificar el estado de las APIs externas
    api_health = ApiClient.check_api_health()
    
    # Verificar el estado general de la aplicación
    app_status = {
        "status": "ok",
        "apis": api_health,
        "all_apis_healthy": all(api_health.values())
    }
    
    return jsonify(app_status)
