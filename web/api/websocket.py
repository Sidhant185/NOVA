"""
WebSocket handlers for real-time communication
"""
from flask import request
from flask_socketio import emit, join_room, leave_room
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config import Config

# Add web directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.session_manager import get_chatbot

logger = logging.getLogger(__name__)

# Store streaming states
streaming_states = {}

def register_events(socketio):
    """Register WebSocket events."""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection."""
        logger.info(f"Client connected: {request.sid}")
        emit('connected', {
            'message': f'Connected to {Config.ASSISTANT_NAME}',
            'assistant_name': Config.ASSISTANT_NAME
        })
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        logger.info(f"Client disconnected: {request.sid}")
        # Clean up streaming state if exists
        if request.sid in streaming_states:
            del streaming_states[request.sid]
    
    @socketio.on('chat_message')
    def handle_chat_message(data):
        """Handle chat message with optional streaming."""
        try:
            message = data.get('message', '').strip()
            stream = data.get('stream', False)
            session_id = data.get('session_id', 'default')
            
            if not message:
                emit('error', {'message': 'Message cannot be empty'})
                return
            
            chatbot = get_chatbot(session_id)
            
            # Emit typing indicator
            emit('typing', {'status': True})
            
            if stream:
                # Stream response word by word (for detailed responses)
                response = chatbot.chat(message)
                words = response.split()
                
                for i, word in enumerate(words):
                    emit('stream_token', {
                        'token': word + (' ' if i < len(words) - 1 else ''),
                        'is_complete': i == len(words) - 1
                    })
                    socketio.sleep(0.05)  # Small delay for streaming effect
            else:
                # Send complete response
                response = chatbot.chat(message)
                
                # Handle response format (string or dict)
                if isinstance(response, dict):
                    # Response has metadata for routing
                    emit('chat_response', {
                        'message': message,
                        'response': response.get('content', ''),
                        'metadata': response.get('metadata', {}),
                        'research_data': response.get('research_data'),
                        'complete': True
                    })
                else:
                    # Simple string response (backward compatibility)
                    emit('chat_response', {
                        'message': message,
                        'response': response,
                        'complete': True
                    })
            
            # Emit typing indicator off
            emit('typing', {'status': False})
            
        except Exception as e:
            logger.error(f"Error in handle_chat_message: {e}", exc_info=True)
            emit('error', {'message': str(e)})
            emit('typing', {'status': False})
    
    @socketio.on('cancel_stream')
    def handle_cancel_stream():
        """Cancel ongoing stream."""
        if request.sid in streaming_states:
            streaming_states[request.sid]['cancelled'] = True
            emit('stream_cancelled', {'message': 'Stream cancelled'})
    
    @socketio.on('get_history')
    def handle_get_history(data):
        """Send chat history to client."""
        try:
            session_id = data.get('session_id', 'default')
            chatbot = get_chatbot(session_id)
            
            emit('history', {
                'messages': chatbot.messages,
                'count': len(chatbot.messages)
            })
        except Exception as e:
            logger.error(f"Error in handle_get_history: {e}", exc_info=True)
            emit('error', {'message': str(e)})

