"""
Rutas para la API de chat del agente de tráfico.
"""
from flask import Blueprint, request, jsonify, current_app
import json
import uuid
from src.services.agent_service import AgentService
from src.models.conversation import Conversation, db

# Create blueprint
chat_bp = Blueprint('chat', __name__)

# Instantiate agent service
agent_service = AgentService()

@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint to process user messages and get agent responses.
    
    Expects a JSON with:
    - message: User message
    - session_id: (Optional) Session ID to maintain context
    
    Returns:
    - response: Agent response
    - session_id: Session ID (new or existing)
    """
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({
            'error': 'A message is required in the request body'
        }), 400
    
    user_message = data.get('message')
    session_id = data.get('session_id', str(uuid.uuid4()))
    
    # Process message with agent
    result = agent_service.process_message(user_message, session_id)
    
    # Save conversation to database
    try:
        conversation = Conversation(
            session_id=session_id,
            user_message=user_message,
            agent_response=result.get('response', ''),
            optimizer_type=result.get('optimizer_type'),
            weights=json.dumps(result.get('weights', {}))
        )
        db.session.add(conversation)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error saving conversation: {str(e)}")
        db.session.rollback()
    
    return jsonify({
        'response': result.get('response', ''),
        'session_id': session_id
    })

@chat_bp.route('/history/<session_id>', methods=['GET'])
def get_history(session_id):
    """
    Get conversation history for a specific session.
    
    Args:
        session_id: Session ID
        
    Returns:
        List of conversation messages
    """
    try:
        conversations = Conversation.get_conversation_history(session_id)
        history = []
        
        for conv in conversations:
            history.append({
                'id': conv.id,
                'user_message': conv.user_message,
                'agent_response': conv.agent_response,
                'optimizer_type': conv.optimizer_type,
                'weights': json.loads(conv.weights) if conv.weights else {},
                'created_at': conv.created_at.isoformat()
            })
        
        return jsonify({
            'session_id': session_id,
            'history': history
        })
    
    except Exception as e:
        current_app.logger.error(f"Error getting conversation history: {str(e)}")
        return jsonify({
            'error': f'Error retrieving conversation history: {str(e)}'
        }), 500
