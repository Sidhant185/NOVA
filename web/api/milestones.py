"""
Milestones API endpoints
Handles milestone tracking and celebrations.
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

bp = Blueprint('milestones', __name__)

@bp.route('', methods=['GET'])
def get_milestones():
    """Get all milestones."""
    try:
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        milestones = chatbot.milestone_tracker.get_all_milestones()
        
        return jsonify({
            'success': True,
            'milestones': milestones,
            'count': len(milestones)
        })
    
    except Exception as e:
        logger.error(f"Error in get_milestones: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get milestones: {str(e)}'}), 500

@bp.route('/add', methods=['POST'])
def add_milestone():
    """Add a milestone."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        milestone_type = data.get('type', '').strip()
        date = data.get('date', '').strip()
        description = data.get('description', '').strip()
        importance = int(data.get('importance', 5))
        recurring = bool(data.get('recurring', False))
        
        if not milestone_type or not date or not description:
            return jsonify({'error': 'Type, date, and description are required'}), 400
        
        session_id = data.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        
        success = chatbot.milestone_tracker.add_milestone(
            milestone_type, date, description, importance, recurring
        )
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Milestone added successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to add milestone or milestone already exists'
            }), 400
    
    except Exception as e:
        logger.error(f"Error in add_milestone: {e}", exc_info=True)
        return jsonify({'error': f'Failed to add milestone: {str(e)}'}), 500

@bp.route('/upcoming', methods=['GET'])
def get_upcoming_milestones():
    """Get upcoming milestones."""
    try:
        session_id = request.args.get('session_id', 'default')
        days = int(request.args.get('days', 30))
        
        chatbot = get_chatbot(session_id)
        upcoming = chatbot.milestone_tracker.get_upcoming_milestones(days)
        
        return jsonify({
            'success': True,
            'upcoming': upcoming,
            'count': len(upcoming)
        })
    
    except Exception as e:
        logger.error(f"Error in get_upcoming_milestones: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get upcoming milestones: {str(e)}'}), 500

@bp.route('/today', methods=['GET'])
def get_today_milestones():
    """Get milestones happening today."""
    try:
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        today = chatbot.milestone_tracker.get_today_milestones()
        
        # Generate celebration messages
        celebrations = []
        for milestone in today:
            message = chatbot.milestone_tracker.generate_celebration_message(milestone)
            celebrations.append({
                **milestone,
                "celebration_message": message
            })
        
        return jsonify({
            'success': True,
            'milestones': celebrations,
            'count': len(celebrations)
        })
    
    except Exception as e:
        logger.error(f"Error in get_today_milestones: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get today milestones: {str(e)}'}), 500

