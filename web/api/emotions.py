"""
Emotions API endpoints
Handles emotion detection and analysis.
"""
from flask import Blueprint, request, jsonify
import logging
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.emotion_detector import EmotionDetector

logger = logging.getLogger(__name__)

bp = Blueprint('emotions', __name__)

# Store emotion detectors per session
emotion_detectors = {}

def get_emotion_detector(session_id: str = 'default') -> EmotionDetector:
    """Get or create emotion detector for session."""
    if session_id not in emotion_detectors:
        emotion_detectors[session_id] = EmotionDetector()
        logger.info(f"Created new emotion detector for session: {session_id}")
    return emotion_detectors[session_id]

@bp.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion from a message."""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        context = data.get('context', [])  # Optional conversation context
        
        if not message:
            return jsonify({
                'success': True,
                'emotion': 'neutral',
                'intensity': 'low',
                'context': '',
                'keywords': [],
                'confidence': 0.0
            })
        
        detector = get_emotion_detector(session_id)
        result = detector.detect(message, context)
        
        return jsonify({
            'success': True,
            **result
        })
    
    except Exception as e:
        logger.error(f"Error in analyze_emotion: {e}", exc_info=True)
        return jsonify({'error': f'Failed to analyze emotion: {str(e)}'}), 500

@bp.route('/history', methods=['GET'])
def get_emotion_history():
    """Get emotion history for a session."""
    try:
        session_id = request.args.get('session_id', 'default')
        limit = int(request.args.get('limit', 20))
        
        detector = get_emotion_detector(session_id)
        history = detector.get_emotion_history(limit)
        
        return jsonify({
            'success': True,
            'history': history,
            'count': len(history)
        })
    
    except Exception as e:
        logger.error(f"Error in get_emotion_history: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get emotion history: {str(e)}'}), 500

@bp.route('/stats', methods=['GET'])
def get_emotion_stats():
    """Get emotion statistics for a session."""
    try:
        session_id = request.args.get('session_id', 'default')
        
        detector = get_emotion_detector(session_id)
        stats = detector.get_emotion_stats()
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        logger.error(f"Error in get_emotion_stats: {e}", exc_info=True)
        return jsonify({'error': f'Failed to get emotion stats: {str(e)}'}), 500

