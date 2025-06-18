"""
Punto de entrada principal de la aplicación Flask.
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from flask import Flask
from flask_cors import CORS
from src.models.conversation import db
from src.routes.chat import chat_bp
from src.routes.health import health_bp
from src.config import config

def create_app(config_name='default'):
    """
    Crea y configura la aplicación Flask.
    
    Args:
        config_name: Nombre de la configuración a utilizar
        
    Returns:
        Aplicación Flask configurada
    """
    app = Flask(__name__)
    
    # Configurar la aplicación
    app_config = config[config_name]
    app.config.from_object(app_config)
    
    # Inicializar extensiones
    CORS(app)  # Permitir solicitudes CORS
    db.init_app(app)
    
    # Registrar blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/api')
    
    # Crear las tablas de la base de datos
    with app.app_context():
        db.create_all()
    
    return app

# Crear la aplicación
app = create_app(os.getenv('FLASK_CONFIG', 'default'))

if __name__ == '__main__':
    # Ejecutar la aplicación
    app.run(host='0.0.0.0', port=8000, debug=True)
