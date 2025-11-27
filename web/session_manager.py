"""
Session Manager for NOVA Web Interface
Manages chatbot instances per session
"""
from Chatbot import Chatbot
import logging

logger = logging.getLogger(__name__)

# Shared chatbot instances across all API modules
chatbot_instances = {}

def get_chatbot(session_id='default'):
    """Get or create chatbot instance for session."""
    if session_id not in chatbot_instances:
        chatbot_instances[session_id] = Chatbot()
        logger.info(f"Created new chatbot instance for session: {session_id}")
    return chatbot_instances[session_id]

def clear_session(session_id):
    """Clear a session's chatbot instance."""
    if session_id in chatbot_instances:
        del chatbot_instances[session_id]
        logger.info(f"Cleared chatbot instance for session: {session_id}")

