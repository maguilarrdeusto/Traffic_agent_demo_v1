import json
import logging
from typing import Dict, Any, Optional
from .agent_logic import traffic_agent, extract_differences, interpret_user_input

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Almacenamiento de conversaciones por ID de sesión
conversation_store: Dict[str, Any] = {}

def chat_with_agent(user_input: str, session_id: Optional[str] = None) -> str:
    """
    Procesa la entrada del usuario y devuelve la respuesta del agente.
    
    Args:
        user_input: El mensaje del usuario
        session_id: Identificador opcional de sesión para mantener conversaciones separadas
    
    Returns:
        La respuesta del agente como texto
    """
    if not session_id:
        session_id = "default"
    
    logger.info(f"Procesando mensaje para sesión {session_id}: {user_input[:50]}...")
    
    try:
        # Detectar si es una solicitud de optimización
        optimization_triggers = [
            "optimize", "priority", "weight", "optimizar", "prioridad", "peso",
            "public transport", "congestion", "emissions", "operational cost",
            "transporte público", "congestión", "emisiones", "costo operacional"
        ]
        is_optimization = any(trigger in user_input.lower() for trigger in optimization_triggers)

        # Preparar el mensaje para el agente
        if is_optimization:
            try:
                logger.info("Detectada solicitud de optimización, interpretando parámetros...")
                weights = interpret_user_input(user_input)
                message = json.dumps(weights)
                logger.info(f"Parámetros interpretados: {message}")
            except Exception as e:
                logger.error(f"Error al interpretar la entrada: {str(e)}")
                return f"❌ Error al interpretar la entrada: {str(e)}"
        else:
            message = user_input

        # Preparar la entrada para el agente (incluyendo historial de conversación)
        agent_input = {
            "input": message
            # No es necesario pasar chat_history explícitamente, el agente mantiene su propia memoria
        }

        # Invocar al agente
        logger.info("Invocando al agente...")
        agent_response = traffic_agent.invoke(agent_input)
        
        # Procesar la respuesta
        try:
            # Intentar interpretar la respuesta como JSON (para resultados de optimización)
            response_data = json.loads(agent_response.get("output", ""))
            friendly_summary = extract_differences(response_data)
            logger.info("Respuesta de optimización procesada correctamente")
        except (json.JSONDecodeError, TypeError):
            # Si no es JSON, usar la respuesta directa del agente
            friendly_summary = agent_response.get("output", "")
            logger.info("Respuesta de texto procesada correctamente")
        except Exception as e:
            logger.error(f"Error al procesar la respuesta: {str(e)}")
            friendly_summary = f"Error al procesar la respuesta: {str(e)}"

        return friendly_summary

    except Exception as e:
        logger.error(f"Error general del agente: {str(e)}")
        return f"⚠️ Error del agente: {str(e)}"
