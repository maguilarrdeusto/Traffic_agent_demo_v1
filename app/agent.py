import json
import logging
from typing import Dict, Any, Optional
# The new agent_logic.py now exports the agent instance directly
from .agent_logic import traffic_agent, InterfaceModule

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def chat_with_agent(user_input: str, session_id: Optional[str] = None) -> str:
    """
    Process user input and return the agent's response.
    The agent itself now handles tool selection and result formatting.
    
    Args:
        user_input: The user's message
        session_id: Optional session identifier (currently managed by the agent's memory)
    
    Returns:
        The agent's response as text
    """
    if not session_id:
        # Session ID is primarily managed by the agent's memory, 
        # but can be logged or used for other external tracking if needed.
        session_id = "default_session" 
    
    logger.info(f"Processing message for session {session_id}: {user_input[:100]}...")
    
    try:
        # The new agent expects the raw user input.
        # It will internally decide the tool and parameters.
        agent_input = {"input": user_input}
        
        logger.info(f"Invoking the main traffic agent with input: {agent_input}")
        # The agent_executor.invoke will return a dictionary, typically with an 'output' key for the final response.
        agent_response_dict = traffic_agent.invoke(agent_input)
        
        # The agent's prompt is designed to return the final, user-facing formatted string.
        final_response = agent_response_dict.get("output", "Sorry, I encountered an issue processing your request.")
        
        logger.info(f"Agent final response: {final_response[:100]}...")
        return final_response

    except Exception as e:
        logger.error(f"Error in chat_with_agent: {str(e)}", exc_info=True)
        return f"⚠️ Agent error: An unexpected issue occurred. Details: {str(e)}"

