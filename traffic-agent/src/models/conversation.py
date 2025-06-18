"""
Modelo para almacenar conversaciones del agente de tráfico.
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Conversation(db.Model):
    """Modelo para almacenar conversaciones entre usuarios y el agente."""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), nullable=False, index=True)
    user_message = db.Column(db.Text, nullable=False)
    agent_response = db.Column(db.Text, nullable=False)
    optimizer_type = db.Column(db.String(50), nullable=True)
    weights = db.Column(db.Text, nullable=True)  # Almacenado como JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Conversation {self.id}: {self.session_id}>'
    
    @staticmethod
    def get_conversation_history(session_id, limit=10):
        """Obtiene el historial de conversación para una sesión específica."""
        return Conversation.query.filter_by(session_id=session_id).order_by(
            Conversation.created_at.desc()
        ).limit(limit).all()
