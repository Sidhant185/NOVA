"""
Chat API endpoints
Handles chat messages and responses.
"""
from flask import Blueprint, request, jsonify
import logging
import sys
import os
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import Config

# Add web directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.session_manager import get_chatbot

logger = logging.getLogger(__name__)

bp = Blueprint('chat', __name__)

@bp.route('/send', methods=['POST'])
def send_message():
    """Send a message and get response."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data['message'].strip()
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        session_id = data.get('session_id') or request.headers.get('X-Session-ID', 'default')
        chatbot = get_chatbot(session_id)
        
        # Detect emotion before chat (to include in response)
        detected_emotion = chatbot.emotion_detector.detect(message, chatbot.messages[-5:] if len(chatbot.messages) > 0 else None)
        
        # Get relationship status
        relationship_status = chatbot.relationship_tracker.get_status()
        
        # Determine mode
        query_lower = message.lower()
        detected_modes = chatbot.personality_engine.determine_mode(
            detected_emotion['emotion'],
            detected_emotion['intensity'],
            relationship_status["relationship_stage"],
            message,
            query_lower
        )
        
        response = chatbot.chat(message)
        
        return jsonify({
            'success': True,
            'response': response,
            'message': message,
            'emotion': {
                'emotion': detected_emotion['emotion'],
                'intensity': detected_emotion['intensity'],
                'confidence': detected_emotion.get('confidence', 0.0)
            },
            'relationship': {
                'stage': relationship_status['relationship_stage'],
                'trust_level': relationship_status['trust_level'],
                'intimacy_level': relationship_status['intimacy_level']
            },
            'mode': detected_modes[0] if detected_modes else 'casual_friend',
            'modes': detected_modes
        })
    
    except Exception as e:
        logger.error(f"Error in send_message: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@bp.route('/history', methods=['GET'])
def get_history():
    """Get chat history."""
    try:
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        return jsonify({
            'success': True,
            'messages': chatbot.messages,
            'count': len(chatbot.messages)
        })
    
    except Exception as e:
        logger.error(f"Error in get_history: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@bp.route('/clear', methods=['POST'])
def clear_history():
    """Clear chat history."""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        chatbot.messages = []
        chatbot.save_chat_log()
        
        return jsonify({
            'success': True,
            'message': 'Chat history cleared'
        })
    
    except Exception as e:
        logger.error(f"Error in clear_history: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@bp.route('/export', methods=['GET'])
def export_history():
    """Export chat history."""
    try:
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        return jsonify({
            'success': True,
            'messages': chatbot.messages,
            'exported_at': str(chatbot.messages[-1].get('timestamp', '') if chatbot.messages else '')
        })
    
    except Exception as e:
        logger.error(f"Error in export_history: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

