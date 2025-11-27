"""
Proactive Care Manager
Tracks emotional states and schedules follow-up check-ins.
"""
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ProactiveCareManager:
    """Manages proactive care and follow-up check-ins."""
    
    def __init__(self, user_id: str, data_path: str = None):
        """Initialize proactive care manager."""
        self.user_id = user_id
        self.data_path = data_path or f"Data/{user_id}_ProactiveCare.json"
        self.care_data = self._load_care_data()
    
    def _load_care_data(self) -> Dict:
        """Load proactive care data from file."""
        default_data = {
            "emotional_states": [],
            "scheduled_check_ins": [],
            "completed_check_ins": [],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    default_data.update(data)
                    return default_data
        except Exception as e:
            logger.error(f"Error loading proactive care data: {e}")
        
        return default_data
    
    def _save_care_data(self):
        """Save proactive care data to file."""
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            self.care_data["updated_at"] = datetime.now().isoformat()
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.care_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving proactive care data: {e}")
    
    def record_emotional_state(self, emotion: str, intensity: str, context: str, query: str = ""):
        """Record an emotional state for tracking."""
        emotional_state = {
            "emotion": emotion,
            "intensity": intensity,
            "context": context,
            "query": query[:200] if query else "",
            "timestamp": datetime.now().isoformat()
        }
        
        self.care_data["emotional_states"].append(emotional_state)
        
        # Keep only last 100 emotional states
        if len(self.care_data["emotional_states"]) > 100:
            self.care_data["emotional_states"] = self.care_data["emotional_states"][-100:]
        
        # Schedule follow-up for significant emotional states
        if emotion in ["sad", "stressed", "anxious", "lonely", "frustrated"] and intensity in ["high", "medium"]:
            self._schedule_follow_up(emotion, intensity, context, query)
        elif emotion in ["happy", "excited", "confident"] and intensity == "high":
            # Celebrate achievements
            self._schedule_celebration(emotion, context)
        
        self._save_care_data()
    
    def _schedule_follow_up(self, emotion: str, intensity: str, context: str, query: str):
        """Schedule a follow-up check-in."""
        # Schedule follow-up based on intensity
        if intensity == "high":
            hours_later = 24  # Check in after 24 hours
        else:
            hours_later = 48  # Check in after 48 hours
        
        scheduled_time = datetime.now() + timedelta(hours=hours_later)
        
        check_in = {
            "type": "emotional_follow_up",
            "emotion": emotion,
            "intensity": intensity,
            "context": context,
            "query": query[:200] if query else "",
            "scheduled_time": scheduled_time.isoformat(),
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        # Check if similar check-in already exists
        existing = [c for c in self.care_data["scheduled_check_ins"] 
                    if c.get("emotion") == emotion and c.get("status") == "pending"]
        if not existing:
            self.care_data["scheduled_check_ins"].append(check_in)
            logger.info(f"Scheduled follow-up for {emotion} at {scheduled_time}")
    
    def _schedule_celebration(self, emotion: str, context: str):
        """Schedule a celebration/acknowledgment."""
        scheduled_time = datetime.now() + timedelta(hours=12)  # Celebrate after 12 hours
        
        check_in = {
            "type": "celebration",
            "emotion": emotion,
            "context": context,
            "scheduled_time": scheduled_time.isoformat(),
            "created_at": datetime.now().isoformat(),
            "status": "pending"
        }
        
        self.care_data["scheduled_check_ins"].append(check_in)
        logger.info(f"Scheduled celebration for {emotion} at {scheduled_time}")
    
    def get_pending_check_ins(self) -> List[Dict]:
        """Get all pending check-ins that are due."""
        now = datetime.now()
        pending = []
        
        for check_in in self.care_data["scheduled_check_ins"]:
            if check_in.get("status") == "pending":
                try:
                    scheduled_time = datetime.fromisoformat(check_in["scheduled_time"])
                    if scheduled_time <= now:
                        pending.append(check_in)
                except:
                    pass
        
        return pending
    
    def complete_check_in(self, check_in_id: str = None, check_in: Dict = None):
        """Mark a check-in as completed."""
        if check_in:
            check_in["status"] = "completed"
            check_in["completed_at"] = datetime.now().isoformat()
            self.care_data["completed_check_ins"].append(check_in)
            
            # Remove from scheduled
            self.care_data["scheduled_check_ins"] = [
                c for c in self.care_data["scheduled_check_ins"]
                if c != check_in or c.get("status") != "pending"
            ]
        elif check_in_id:
            # Find by ID (using timestamp as ID)
            for c in self.care_data["scheduled_check_ins"]:
                if c.get("created_at") == check_in_id and c.get("status") == "pending":
                    self.complete_check_in(check_in=c)
                    break
        
        self._save_care_data()
    
    def generate_proactive_message(self, check_in: Dict) -> Optional[str]:
        """Generate a proactive message for a check-in."""
        check_in_type = check_in.get("type", "")
        emotion = check_in.get("emotion", "")
        context = check_in.get("context", "")
        
        if check_in_type == "emotional_follow_up":
            if emotion in ["sad", "lonely"]:
                return f"Hey, I wanted to check in on you. I remember you were feeling {emotion} earlier. How are you doing now? I'm here for you. 💙"
            elif emotion in ["stressed", "anxious"]:
                return f"Hi! I wanted to see how you're doing. You seemed {emotion} earlier. Are you feeling better? I'm here to support you. 🌸"
            elif emotion == "frustrated":
                return f"Hey, I wanted to check in. You seemed frustrated earlier. How are things going now? I'm here if you need to talk. 💪"
        elif check_in_type == "celebration":
            if emotion in ["happy", "excited"]:
                return f"Hey! I wanted to celebrate with you! You seemed really {emotion} earlier. I'm so happy for you! 🎉💕"
            elif emotion == "confident":
                return f"Hi! I wanted to acknowledge your confidence earlier. You're doing great! Keep it up! ✨💪"
        
        return None
    
    def get_recent_emotional_patterns(self, days: int = 7) -> Dict:
        """Get recent emotional patterns for analysis."""
        cutoff = datetime.now() - timedelta(days=days)
        
        recent_states = [
            state for state in self.care_data["emotional_states"]
            if datetime.fromisoformat(state["timestamp"]) >= cutoff
        ]
        
        patterns = {
            "total_states": len(recent_states),
            "by_emotion": {},
            "by_intensity": {"low": 0, "medium": 0, "high": 0},
            "most_common_emotion": None
        }
        
        for state in recent_states:
            emotion = state.get("emotion", "neutral")
            intensity = state.get("intensity", "low")
            
            patterns["by_emotion"][emotion] = patterns["by_emotion"].get(emotion, 0) + 1
            patterns["by_intensity"][intensity] = patterns["by_intensity"].get(intensity, 0) + 1
        
        if patterns["by_emotion"]:
            patterns["most_common_emotion"] = max(patterns["by_emotion"], key=patterns["by_emotion"].get)
        
        return patterns

