"""
Configuración de la aplicación Flask para el agente de tráfico.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración base para la aplicación."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-traffic-agent')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # URLs de los servicios de optimización
    STANDARD_OPTIMIZER_URL = os.environ.get(
        'STANDARD_OPTIMIZER_URL', 
        'https://fastapi-traffic-agent-v2.onrender.com/api/optimize'
    )
    DYNAMIC_OPTIMIZER_URL = os.environ.get(
        'DYNAMIC_OPTIMIZER_URL', 
        'https://fastapi2-traffic-agent-v1.onrender.com/api/optimize'
    )
    
    # Configuración de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///traffic_agent.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración del modelo de OpenAI
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
    
    # Configuración de timeouts para las APIs externas
    API_TIMEOUT = int(os.environ.get('API_TIMEOUT', 15))
    
    # Configuración de pesos por defecto
    DEFAULT_WEIGHTS = {
        "weight_PublicTransport": 0.1,
        "weight_Congestion": 0.1,
        "weight_Emissions": 0.1,
        "weight_OperationalCost": 0.1
    }
    
    # Intervalos de prioridad
    PRIORITY_INTERVALS = {
        "very high": (0.9, 1.0),
        "high": (0.7, 0.89),
        "medium": (0.5, 0.69),
        "low": (0.3, 0.49),
        "very low": (0.1, 0.29)
    }

class DevelopmentConfig(Config):
    """Configuración para entorno de desarrollo."""
    DEBUG = True
    TESTING = False

class TestingConfig(Config):
    """Configuración para entorno de pruebas."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Configuración para entorno de producción."""
    DEBUG = False
    TESTING = False
    
    # En producción, asegúrate de que SECRET_KEY esté configurado
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configuraciones adicionales específicas de producción
        if not os.environ.get('SECRET_KEY'):
            raise RuntimeError('SECRET_KEY must be set for production')

# Diccionario de configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
