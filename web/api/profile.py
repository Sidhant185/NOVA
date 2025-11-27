"""
User Profile API
Handles user profile, preferences, and personalization
"""
from flask import Blueprint, request, jsonify
import json
import os
import sys
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from web.session_manager import get_chatbot

bp = Blueprint('profile', __name__)

def get_profile_path(user_id: str) -> str:
    """Get path for user profile file."""
    return f"Data/{user_id}_Profile.json"

def ensure_data_directory():
    """Ensure Data directory exists."""
    os.makedirs("Data", exist_ok=True)

def load_profile(user_id: str) -> dict:
    """Load user profile."""
    ensure_data_directory()
    profile_path = get_profile_path(user_id)
    try:
        if os.path.exists(profile_path):
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading profile: {e}")
    
    # Return default profile
    return {
        "user_id": user_id,
        "preferences": {
            "theme": "dark",
            "chat_style": "friendly",
            "message_theme": "default",
            "avatar_style": "default"
        },
        "interests": [],
        "work_context": "",
        "personal_info": {},
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

def save_profile(user_id: str, profile: dict):
    """Save user profile."""
    ensure_data_directory()
    profile_path = get_profile_path(user_id)
    profile["updated_at"] = datetime.now().isoformat()
    try:
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving profile: {e}")
        return False

@bp.route('/get', methods=['GET'])
def get_profile():
    """Get user profile."""
    try:
        user_id = request.args.get('user_id', 'default')
        profile = load_profile(user_id)
        return jsonify({"success": True, "profile": profile})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/update', methods=['POST'])
def update_profile():
    """Update user profile."""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        updates = data.get('updates', {})
        
        profile = load_profile(user_id)
        
        # Update preferences
        if 'preferences' in updates:
            profile['preferences'].update(updates['preferences'])
        
        # Update other fields
        for key in ['interests', 'work_context', 'personal_info']:
            if key in updates:
                profile[key] = updates[key]
        
        if save_profile(user_id, profile):
            return jsonify({"success": True, "profile": profile})
        else:
            return jsonify({"success": False, "error": "Failed to save profile"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/preferences', methods=['POST'])
def update_preferences():
    """Update user preferences."""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        preferences = data.get('preferences', {})
        
        profile = load_profile(user_id)
        profile['preferences'].update(preferences)
        
        if save_profile(user_id, profile):
            return jsonify({"success": True, "preferences": profile['preferences']})
        else:
            return jsonify({"success": False, "error": "Failed to save preferences"}), 500
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/relationship/status', methods=['GET'])
def get_relationship_status():
    """Get current relationship status."""
    try:
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        status = chatbot.relationship_tracker.get_status()
        return jsonify({"success": True, "status": status})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/relationship/milestones', methods=['GET'])
def get_relationship_milestones():
    """Get relationship milestones."""
    try:
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        milestones = chatbot.relationship_tracker.get_milestones()
        return jsonify({"success": True, "milestones": milestones})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@bp.route('/relationship/progress', methods=['GET'])
def get_relationship_progress():
    """Get relationship progression data."""
    try:
        session_id = request.args.get('session_id', 'default')
        chatbot = get_chatbot(session_id)
        progress = chatbot.relationship_tracker.get_progress()
        return jsonify({"success": True, "progress": progress})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

