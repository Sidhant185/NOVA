"""
Relationship Tracker
Tracks relationship progression, trust, intimacy, and milestones.
"""
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class RelationshipTracker:
    """Tracks relationship progression with user."""
    
    RELATIONSHIP_STAGES = [
        "stranger",
        "acquaintance", 
        "friend",
        "close_friend",
        "best_friend",
        "romantic_partner"
    ]
    
    def __init__(self, user_id: str, data_path: str = None):
        """Initialize relationship tracker."""
        self.user_id = user_id
        self.data_path = data_path or f"Data/{user_id}_Relationship.json"
        self.relationship_data = self._load_relationship_data()
    
    def _load_relationship_data(self) -> Dict:
        """Load relationship data from file."""
        default_data = {
            "trust_level": 30,  # Start at 30 (friend level)
            "intimacy_level": 20,  # Start at 20 (low intimacy)
            "relationship_stage": "friend",
            "first_conversation": None,
            "milestones": [],
            "interaction_count": 0,
            "emotional_shares": 0,
            "romantic_interactions": 0,
            "deep_conversations": 0,
            "trust_building_moments": 0,
            "last_interaction": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        try:
            if os.path.exists(self.data_path):
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    default_data.update(data)
                    return default_data
        except Exception as e:
            logger.error(f"Error loading relationship data: {e}")
        
        return default_data
    
    def _save_relationship_data(self):
        """Save relationship data to file."""
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            self.relationship_data["updated_at"] = datetime.now().isoformat()
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.relationship_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving relationship data: {e}")
    
    def record_interaction(self, interaction_type: str = "general"):
        """Record an interaction."""
        self.relationship_data["interaction_count"] += 1
        self.relationship_data["last_interaction"] = datetime.now().isoformat()
        
        # Set first conversation if not set
        if not self.relationship_data.get("first_conversation"):
            self.relationship_data["first_conversation"] = datetime.now().isoformat()
            self.add_milestone("first_conversation", "First conversation with Nova")
        
        # Track specific interaction types
        if interaction_type == "emotional":
            self.relationship_data["emotional_shares"] += 1
            self._increase_intimacy(2)
            self._increase_trust(1)
        elif interaction_type == "romantic":
            self.relationship_data["romantic_interactions"] += 1
            self._increase_intimacy(3)
            self._increase_trust(1)
        elif interaction_type == "deep":
            self.relationship_data["deep_conversations"] += 1
            self._increase_intimacy(1)
            self._increase_trust(2)
        elif interaction_type == "trust_building":
            self.relationship_data["trust_building_moments"] += 1
            self._increase_trust(3)
            self._increase_intimacy(1)
        else:
            # General interaction - small increases
            self._increase_intimacy(0.1)
            self._increase_trust(0.1)
        
        self._update_relationship_stage()
        self._save_relationship_data()
    
    def _increase_trust(self, amount: float):
        """Increase trust level (0-100)."""
        self.relationship_data["trust_level"] = min(100, self.relationship_data["trust_level"] + amount)
    
    def _increase_intimacy(self, amount: float):
        """Increase intimacy level (0-100)."""
        self.relationship_data["intimacy_level"] = min(100, self.relationship_data["intimacy_level"] + amount)
    
    def _update_relationship_stage(self):
        """Update relationship stage based on trust and intimacy."""
        trust = self.relationship_data["trust_level"]
        intimacy = self.relationship_data["intimacy_level"]
        avg = (trust + intimacy) / 2
        
        current_stage = self.relationship_data["relationship_stage"]
        current_index = self.RELATIONSHIP_STAGES.index(current_stage) if current_stage in self.RELATIONSHIP_STAGES else 0
        
        # Determine new stage based on average
        if avg >= 80:
            new_stage = "romantic_partner"
        elif avg >= 65:
            new_stage = "best_friend"
        elif avg >= 50:
            new_stage = "close_friend"
        elif avg >= 35:
            new_stage = "friend"
        elif avg >= 20:
            new_stage = "acquaintance"
        else:
            new_stage = "stranger"
        
        # Only upgrade, never downgrade (unless explicitly reset)
        new_index = self.RELATIONSHIP_STAGES.index(new_stage)
        if new_index > current_index:
            old_stage = current_stage
            self.relationship_data["relationship_stage"] = new_stage
            self.add_milestone(f"relationship_upgrade_{new_stage}", f"Relationship upgraded to {new_stage}")
            logger.info(f"Relationship stage upgraded: {old_stage} -> {new_stage}")
    
    def add_milestone(self, milestone_type: str, description: str):
        """Add a relationship milestone."""
        milestone = {
            "type": milestone_type,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        
        # Check if milestone already exists
        existing = [m for m in self.relationship_data["milestones"] if m.get("type") == milestone_type]
        if not existing:
            self.relationship_data["milestones"].append(milestone)
            self._save_relationship_data()
            logger.info(f"Milestone added: {milestone_type}")
    
    def get_status(self) -> Dict:
        """Get current relationship status."""
        return {
            "trust_level": round(self.relationship_data["trust_level"], 1),
            "intimacy_level": round(self.relationship_data["intimacy_level"], 1),
            "relationship_stage": self.relationship_data["relationship_stage"],
            "interaction_count": self.relationship_data["interaction_count"],
            "emotional_shares": self.relationship_data["emotional_shares"],
            "romantic_interactions": self.relationship_data["romantic_interactions"],
            "deep_conversations": self.relationship_data["deep_conversations"],
            "trust_building_moments": self.relationship_data["trust_building_moments"],
            "first_conversation": self.relationship_data.get("first_conversation"),
            "last_interaction": self.relationship_data.get("last_interaction")
        }
    
    def get_milestones(self) -> List[Dict]:
        """Get all relationship milestones."""
        return self.relationship_data.get("milestones", [])
    
    def get_progress(self) -> Dict:
        """Get relationship progression data."""
        first_conv = self.relationship_data.get("first_conversation")
        days_since_first = 0
        
        if first_conv:
            try:
                first_date = datetime.fromisoformat(first_conv)
                days_since_first = (datetime.now() - first_date).days
            except:
                pass
        
        return {
            "status": self.get_status(),
            "milestones": self.get_milestones(),
            "days_since_first_conversation": days_since_first,
            "interaction_frequency": self.relationship_data["interaction_count"] / max(days_since_first, 1) if days_since_first > 0 else 0
        }

