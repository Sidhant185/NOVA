"""
Proactive Care API endpoints
Handles proactive care and follow-up check-ins.
"""
from flask import Blueprint, request, jsonify
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Add web directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web.session_manager import get_chatbot

logger = logging.getLogger(__name__)

bp = Blueprint('care', __name__)

@bp.route('/check-ins', methods=['GET'])
def get_check_ins():
    """Get pending check-ins."""
    try:
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        check_ins = chatbot.proactive_care.get_pending_check_ins()
        
        # Generate messages for each check-in
        check_ins_with_messages = []
        for check_in in check_ins:
            message = chatbot.proactive_care.generate_proactive_message(check_in)
            check_ins_with_messages.append({
                **check_in,
                "message": message
            })
        
        return jsonify({
            'success': True,
            'check_ins': check_ins_with_messages,
            'count': len(check_ins_with_messages)
        })
    
    except Exception as e:
        logger.error(f"Error in get_check_ins: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get check-ins: {str(e)}'}), 500

@bp.route('/schedule', methods=['POST'])
def schedule_check_in():
    """Schedule a follow-up check-in."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        session_id = data.get('session_id', 'default')
        emotion = data.get('emotion', '')
        intensity = data.get('intensity', 'medium')
        context = data.get('context', '')
        query = data.get('query', '')
        
        chatbot = get_chatbot(session_id)
        chatbot.proactive_care.record_emotional_state(emotion, intensity, context, query)
        
        return jsonify({
            'success': True,
            'message': 'Check-in scheduled successfully'
        })
    
    except Exception as e:
        logger.error(f"Error in schedule_check_in: {e}", exc_info=True)
        return jsonify({'error': f'Failed to schedule check-in: {str(e)}'}), 500

@bp.route('/complete', methods=['POST'])
def complete_check_in():
    """Mark a check-in as completed."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        session_id = data.get('session_id', 'default')
        check_in_id = data.get('check_in_id')
        check_in = data.get('check_in')
        
        chatbot = get_chatbot(session_id)
        chatbot.proactive_care.complete_check_in(check_in_id, check_in)
        
        return jsonify({
            'success': True,
            'message': 'Check-in completed successfully'
        })
    
    except Exception as e:
        logger.error(f"Error in complete_check_in: {e}", exc_info=True)
        return jsonify({'error': f'Failed to complete check-in: {str(e)}'}), 500

@bp.route('/patterns', methods=['GET'])
def get_emotional_patterns():
    """Get recent emotional patterns."""
    try:
        session_id = request.args.get('session_id', 'default')
        days = int(request.args.get('days', 7))
        
        chatbot = get_chatbot(session_id)
        patterns = chatbot.proactive_care.get_recent_emotional_patterns(days)
        
        return jsonify({
            'success': True,
            'patterns': patterns
        })
    
    except Exception as e:
        logger.error(f"Error in get_emotional_patterns: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get emotional patterns: {str(e)}'}), 500

