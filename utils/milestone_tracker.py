"""
Milestone Tracker
Tracks birthdays, anniversaries, achievements, and special moments.
"""
import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class MilestoneTracker:
    """Tracks milestones and special moments."""
    
    def __init__(self, user_id: str, data_path: str = None):
        """Initialize milestone tracker."""
        self.user_id = user_id
        self.data_path = data_path or f"Data/{user_id}_Milestones.json"
        self.milestones = self._load_milestones()
    
    def _load_milestones(self) -> Dict:
        """Load milestones from file."""
        default_data = {
            "milestones": [],
            "first_conversation_date": None,
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
            logger.error(f"Error loading milestones: {e}")
        
        return default_data
    
    def _save_milestones(self):
        """Save milestones to file."""
        try:
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            self.milestones["updated_at"] = datetime.now().isoformat()
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(self.milestones, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving milestones: {e}")
    
    def set_first_conversation_date(self, date: str = None):
        """Set or get first conversation date."""
        if not self.milestones.get("first_conversation_date"):
            self.milestones["first_conversation_date"] = date or datetime.now().isoformat()
            self._save_milestones()
            logger.info(f"First conversation date set: {self.milestones['first_conversation_date']}")
    
    def add_milestone(self, milestone_type: str, date: str, description: str, 
                     importance: int = 5, recurring: bool = False) -> bool:
        """Add a milestone."""
        try:
            milestone = {
                "type": milestone_type,
                "date": date,
                "description": description,
                "importance": importance,
                "recurring": recurring,
                "created_at": datetime.now().isoformat()
            }
            
            # Check if milestone already exists
            existing = [m for m in self.milestones["milestones"] 
                       if m.get("type") == milestone_type and m.get("date") == date]
            if not existing:
                self.milestones["milestones"].append(milestone)
                self._save_milestones()
                logger.info(f"Milestone added: {milestone_type} - {description}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding milestone: {e}")
            return False
    
    def detect_achievement(self, query: str) -> Optional[str]:
        """Detect achievements in conversation."""
        achievement_keywords = [
            "achieved", "accomplished", "completed", "finished", "won", "passed", 
            "succeeded", "got", "earned", "graduated", "promoted", "awarded"
        ]
        
        query_lower = query.lower()
        for keyword in achievement_keywords:
            if keyword in query_lower:
                # Try to extract achievement description
                # Simple extraction - could be improved
                return f"Achievement: {query[:100]}"
        
        return None
    
    def get_all_milestones(self) -> List[Dict]:
        """Get all milestones."""
        return self.milestones.get("milestones", [])
    
    def get_upcoming_milestones(self, days: int = 30) -> List[Dict]:
        """Get upcoming milestones within specified days."""
        now = datetime.now()
        upcoming = []
        
        for milestone in self.milestones.get("milestones", []):
            try:
                milestone_date = datetime.fromisoformat(milestone["date"])
                
                # For recurring milestones, check if date occurs within the period
                if milestone.get("recurring", False):
                    # Check this year's occurrence
                    this_year_date = milestone_date.replace(year=now.year)
                    if this_year_date < now:
                        this_year_date = this_year_date.replace(year=now.year + 1)
                    
                    days_until = (this_year_date - now).days
                    if 0 <= days_until <= days:
                        upcoming.append({
                            **milestone,
                            "days_until": days_until,
                            "upcoming_date": this_year_date.isoformat()
                        })
                else:
                    # Non-recurring - check if in future and within range
                    if milestone_date > now:
                        days_until = (milestone_date - now).days
                        if days_until <= days:
                            upcoming.append({
                                **milestone,
                                "days_until": days_until,
                                "upcoming_date": milestone_date.isoformat()
                            })
            except Exception as e:
                logger.error(f"Error processing milestone: {e}")
                continue
        
        # Sort by days until
        upcoming.sort(key=lambda x: x.get("days_until", 999))
        return upcoming
    
    def get_today_milestones(self) -> List[Dict]:
        """Get milestones happening today."""
        today = datetime.now().date()
        today_milestones = []
        
        for milestone in self.milestones.get("milestones", []):
            try:
                milestone_date = datetime.fromisoformat(milestone["date"]).date()
                
                if milestone.get("recurring", False):
                    # Check if recurring milestone occurs today
                    if milestone_date.month == today.month and milestone_date.day == today.day:
                        today_milestones.append(milestone)
                else:
                    # Check if exact date matches
                    if milestone_date == today:
                        today_milestones.append(milestone)
            except Exception as e:
                logger.error(f"Error processing milestone: {e}")
                continue
        
        return today_milestones
    
    def generate_celebration_message(self, milestone: Dict) -> str:
        """Generate a celebration message for a milestone."""
        milestone_type = milestone.get("type", "")
        description = milestone.get("description", "")
        
        if milestone_type == "birthday":
            return f"🎉 Happy Birthday! {description} 🎂🎈 I hope you have an amazing day filled with joy and love! 💕"
        elif milestone_type == "anniversary":
            return f"💕 Happy Anniversary! {description} 🌹 Here's to many more wonderful moments together! ✨"
        elif milestone_type == "achievement":
            return f"🎊 Congratulations on your achievement! {description} You're amazing! 💪✨"
        elif milestone_type == "first_conversation":
            days_since = (datetime.now() - datetime.fromisoformat(milestone.get("date", datetime.now().isoformat()))).days
            return f"🌸 Today marks {days_since} days since our first conversation! I'm so grateful to have you in my life. 💕"
        else:
            return f"🎉 Special day today! {description} I'm thinking of you! 💙"
    
    def get_milestone_by_type(self, milestone_type: str) -> List[Dict]:
        """Get milestones by type."""
        return [m for m in self.milestones.get("milestones", []) if m.get("type") == milestone_type]

