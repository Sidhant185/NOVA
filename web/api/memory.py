"""
Memory API endpoints
Handles memory management operations.
"""
from flask import Blueprint, request, jsonify
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

bp = Blueprint('memory', __name__)

def ensure_data_directory():
    """Ensure Data directory exists."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Data')
    try:
        os.makedirs(data_dir, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Error creating Data directory: {e}", exc_info=True)
        return False

@bp.route('', methods=['GET'])
def get_memories():
    """Get all memories."""
    try:
        # Ensure Data directory exists
        if not ensure_data_directory():
            return jsonify({'error': 'Failed to initialize data directory'}), 500
        
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        memories = chatbot.get_memory()
        
        # Handle case where memories might be None, invalid, or wrong type
        if memories is None:
            memories = {}
        elif not isinstance(memories, dict):
            # If memories is a list or other type, convert to empty dict
            logger.warning(f"Memories is not a dict, got {type(memories)}. Resetting to empty dict.")
            memories = {}
        
        # Enhance memories with categories if they don't have them
        enhanced_memories = {}
        for key, data in memories.items():
            if isinstance(data, dict):
                enhanced_memories[key] = {
                    'value': data.get('value', ''),
                    'timestamp': data.get('timestamp', ''),
                    'category': data.get('category', 'general'),
                    'tags': data.get('tags', []),
                    'importance': data.get('importance', 1)
                }
            else:
                enhanced_memories[key] = {
                    'value': data,
                    'timestamp': '',
                    'category': 'general',
                    'tags': [],
                    'importance': 1
                }
        
        return jsonify({
            'success': True,
            'memories': enhanced_memories,
            'count': len(enhanced_memories) if isinstance(enhanced_memories, dict) else 0
        })
    
    except Exception as e:
        logger.error(f"Error in get_memories: {e}", exc_info=True)
        return jsonify({'error': f'Failed to retrieve memories: {str(e)}'}), 500

@bp.route('', methods=['POST'])
def add_memory():
    """Add a new memory."""
    try:
        # Ensure Data directory exists
        if not ensure_data_directory():
            return jsonify({'error': 'Failed to initialize data directory'}), 500
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        key = data.get('key', '').strip()
        value = data.get('value', '').strip()
        category = data.get('category', 'general')
        emotion = data.get('emotion')
        tags = data.get('tags', [])
        importance = data.get('importance', 5)
        
        if not value:
            return jsonify({'error': 'Value is required'}), 400
        
        session_id = data.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        
        # If no key provided and emotional memory, use add_emotional_memory
        if not key and emotion:
            success = chatbot.add_emotional_memory(category, value, emotion, tags, importance)
            if success:
                # Get the generated key from recent memories
                memories = chatbot.get_memory()
                # Find the most recent memory with matching value
                for mem_key, mem_data in memories.items():
                    if isinstance(mem_data, dict) and mem_data.get('value') == value:
                        key = mem_key
                        break
        else:
            if not key:
                return jsonify({'error': 'Key is required when not using emotional memory'}), 400
            success = chatbot.add_memory(key, value, category, emotion, tags, importance)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Memory "{key}" added successfully',
                'key': key,
                'value': value
            })
        else:
            logger.error(f"Failed to add memory: key={key}, value={value[:50]}")
            return jsonify({'error': 'Failed to add memory. Check server logs for details.'}), 500
    
    except Exception as e:
        logger.error(f"Error in add_memory: {e}", exc_info=True)
        return jsonify({'error': f'Failed to add memory: {str(e)}'}), 500

@bp.route('/<key>', methods=['DELETE'])
def delete_memory(key):
    """Delete a memory by key."""
    try:
        # Ensure Data directory exists
        if not ensure_data_directory():
            return jsonify({'error': 'Failed to initialize data directory'}), 500
        
        if not key:
            return jsonify({'error': 'Key is required'}), 400
        
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        success = chatbot.forget_memory(key)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Memory "{key}" deleted successfully'
            })
        else:
            return jsonify({'error': f'Memory "{key}" not found'}), 404
    
    except Exception as e:
        logger.error(f"Error in delete_memory: {e}", exc_info=True)
        return jsonify({'error': f'Failed to delete memory: {str(e)}'}), 500

@bp.route('/category/<category>', methods=['GET'])
def get_memories_by_category(category):
    """Get memories by category."""
    try:
        if not ensure_data_directory():
            return jsonify({'error': 'Failed to initialize data directory'}), 500
        
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        memories = chatbot.get_memories_by_category(category)
        
        return jsonify({
            'success': True,
            'memories': memories,
            'category': category,
            'count': len(memories)
        })
    
    except Exception as e:
        logger.error(f"Error in get_memories_by_category: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get memories by category: {str(e)}'}), 500

@bp.route('/emotion/<emotion>', methods=['GET'])
def get_memories_by_emotion(emotion):
    """Get memories by emotion."""
    try:
        if not ensure_data_directory():
            return jsonify({'error': 'Failed to initialize data directory'}), 500
        
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        memories = chatbot.get_memories_by_emotion(emotion)
        
        return jsonify({
            'success': True,
            'memories': memories,
            'emotion': emotion,
            'count': len(memories)
        })
    
    except Exception as e:
        logger.error(f"Error in get_memories_by_emotion: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get memories by emotion: {str(e)}'}), 500

@bp.route('/tags', methods=['GET'])
def get_memories_by_tags():
    """Get memories by tags."""
    try:
        if not ensure_data_directory():
            return jsonify({'error': 'Failed to initialize data directory'}), 500
        
        tags_str = request.args.get('tags', '')
        if not tags_str:
            return jsonify({'error': 'Tags parameter is required'}), 400
        
        tags = [tag.strip() for tag in tags_str.split(',')]
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        memories = chatbot.get_memories_by_tags(tags)
        
        return jsonify({
            'success': True,
            'memories': memories,
            'tags': tags,
            'count': len(memories)
        })
    
    except Exception as e:
        logger.error(f"Error in get_memories_by_tags: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get memories by tags: {str(e)}'}), 500

@bp.route('/emotional-state', methods=['GET'])
def get_recent_emotional_state():
    """Get recent emotional state patterns."""
    try:
        if not ensure_data_directory():
            return jsonify({'error': 'Failed to initialize data directory'}), 500
        
        days = int(request.args.get('days', 7))
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        emotional_state = chatbot.get_recent_emotional_state(days)
        
        return jsonify({
            'success': True,
            'emotional_state': emotional_state,
            'days': days
        })
    
    except Exception as e:
        logger.error(f"Error in get_recent_emotional_state: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get emotional state: {str(e)}'}), 500

