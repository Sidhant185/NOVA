"""
Schedule Tracker
Tracks classes, assignments, and reminders for the user.
"""
import json
import os
import datetime
import logging
import re
from typing import Dict, List, Optional
from config import Config

logger = logging.getLogger(__name__)

class ScheduleTracker:
    """Tracks classes, assignments, and reminders."""
    
    def __init__(self, user_id: str):
        """Initialize schedule tracker."""
        self.user_id = user_id
        self.schedule_path = Config.get_data_path(f"{user_id}_Schedule.json")
        self.schedule = self._load_schedule()
    
    def _load_schedule(self) -> Dict:
        """Load schedule from file."""
        if os.path.exists(self.schedule_path):
            try:
                with open(self.schedule_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading schedule: {e}")
                return self._default_schedule()
        return self._default_schedule()
    
    def _default_schedule(self) -> Dict:
        """Return default schedule structure."""
        return {
            "classes": [],
            "assignments": [],
            "reminders": []
        }
    
    def _save_schedule(self):
        """Save schedule to file."""
        try:
            # Ensure directory exists
            dir_path = os.path.dirname(self.schedule_path)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(self.schedule_path, 'w', encoding='utf-8') as f:
                json.dump(self.schedule, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving schedule: {e}")
    
    def add_class(self, name: str, days: List[str], time: str, location: Optional[str] = None) -> bool:
        """
        Add a class to the schedule.
        
        Args:
            name: Class name
            days: List of days (e.g., ["Monday", "Wednesday", "Friday"])
            time: Time (e.g., "10:00 AM")
            location: Optional location
            
        Returns:
            True if added successfully
        """
        try:
            class_entry = {
                "id": f"class_{len(self.schedule['classes']) + 1}",
                "name": name,
                "days": days,
                "time": time,
                "location": location,
                "created_at": datetime.datetime.now().isoformat()
            }
            self.schedule["classes"].append(class_entry)
            self._save_schedule()
            logger.info(f"Added class: {name}")
            return True
        except Exception as e:
            logger.error(f"Error adding class: {e}")
            return False
    
    def add_assignment(self, title: str, due_date: str, class_name: Optional[str] = None, 
                      description: Optional[str] = None) -> bool:
        """
        Add an assignment.
        
        Args:
            title: Assignment title
            due_date: Due date (ISO format or readable date)
            class_name: Optional class name
            description: Optional description
            
        Returns:
            True if added successfully
        """
        try:
            # Parse due date
            try:
                due_datetime = datetime.datetime.fromisoformat(due_date.replace('Z', '+00:00'))
            except:
                # Try parsing common date formats
                try:
                    due_datetime = datetime.datetime.strptime(due_date, "%Y-%m-%d")
                except:
                    due_datetime = datetime.datetime.now() + datetime.timedelta(days=7)  # Default: 7 days
            
            assignment_entry = {
                "id": f"assignment_{len(self.schedule['assignments']) + 1}",
                "title": title,
                "due_date": due_datetime.isoformat(),
                "class_name": class_name,
                "description": description,
                "completed": False,
                "created_at": datetime.datetime.now().isoformat()
            }
            self.schedule["assignments"].append(assignment_entry)
            self._save_schedule()
            logger.info(f"Added assignment: {title}")
            return True
        except Exception as e:
            logger.error(f"Error adding assignment: {e}")
            return False
    
    def get_upcoming_classes(self, days_ahead: int = 7) -> List[Dict]:
        """Get upcoming classes in the next N days (improved calculation)."""
        today = datetime.datetime.now()
        upcoming = []
        
        # Day name to number mapping
        day_map = {
            "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
            "friday": 4, "saturday": 5, "sunday": 6,
            "mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6
        }
        
        for class_entry in self.schedule["classes"]:
            days = class_entry.get("days", [])
            time_str = class_entry.get("time", "")
            
            for day_name in days:
                day_num = day_map.get(day_name.lower(), None)
                if day_num is None:
                    continue
                
                # Calculate next occurrence of this day
                current_weekday = today.weekday()
                days_until = (day_num - current_weekday) % 7
                if days_until == 0:
                    # If today is the day, check if time hasn't passed
                    if time_str:
                        try:
                            # Try to parse time
                            time_parts = re.search(r"(\d{1,2}):?(\d{2})?\s*(am|pm)", time_str.lower())
                            if time_parts:
                                hour = int(time_parts.group(1))
                                minute = int(time_parts.group(2) or "0")
                                is_pm = time_parts.group(3) == "pm"
                                if is_pm and hour != 12:
                                    hour += 12
                                elif not is_pm and hour == 12:
                                    hour = 0
                                
                                class_time = today.replace(hour=hour, minute=minute, second=0, microsecond=0)
                                if class_time < today:
                                    days_until = 7  # Next week
                        except:
                            pass
                    else:
                        days_until = 7  # If no time specified and today, assume next week
                
                if days_until <= days_ahead:
                    upcoming.append({
                        "class": class_entry["name"],
                        "day": day_name,
                        "time": time_str,
                        "location": class_entry.get("location", ""),
                        "days_until": days_until,
                        "date": (today + datetime.timedelta(days=days_until)).strftime("%Y-%m-%d")
                    })
        
        # Sort by days_until
        upcoming.sort(key=lambda x: x.get("days_until", 999))
        return upcoming[:10]  # Return first 10
    
    def get_upcoming_assignments(self, days_ahead: int = 7) -> List[Dict]:
        """Get upcoming assignments due in the next N days."""
        today = datetime.datetime.now()
        end_date = today + datetime.timedelta(days=days_ahead)
        upcoming = []
        
        for assignment in self.schedule["assignments"]:
            if assignment.get("completed", False):
                continue
            
            try:
                due_date = datetime.datetime.fromisoformat(assignment["due_date"].replace('Z', '+00:00'))
                if today <= due_date <= end_date:
                    days_until = (due_date - today).days
                    upcoming.append({
                        **assignment,
                        "days_until": days_until
                    })
            except:
                continue
        
        # Sort by due date
        upcoming.sort(key=lambda x: x.get("due_date", ""))
        return upcoming
    
    def detect_schedule_mentions(self, text: str) -> Dict:
        """
        Detect mentions of classes or assignments in text (improved detection).
        
        Returns:
            Dict with detected items and extracted information
        """
        import re
        text_lower = text.lower()
        detected = {
            "classes": [],
            "assignments": [],
            "has_schedule_info": False
        }
        
        # Class keywords (improved with whole word matching)
        class_keywords = ["class", "lecture", "course", "subject", "i have a class", "my class",
                         "i take", "enrolled in", "attending", "going to class"]
        class_patterns = [
            r"i (have|take|attend|go to) (a )?class",
            r"my class",
            r"class (on|at|is)",
            r"lecture (on|at|is)"
        ]
        
        class_mentioned = any(re.search(r'\b' + re.escape(kw) + r'\b', text_lower) for kw in class_keywords) or \
                         any(re.search(pattern, text_lower) for pattern in class_patterns)
        
        if class_mentioned:
            # Try to extract class name, day, time
            class_name_match = re.search(r"(?:class|course|lecture|subject)[\s:]+([A-Za-z0-9\s]+?)(?:on|at|$)", text_lower)
            day_match = re.search(r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|wed|thu|fri|sat|sun)", text_lower)
            time_match = re.search(r"(\d{1,2}):?(\d{2})?\s*(am|pm|morning|afternoon|evening)", text_lower)
            
            class_info = {"mentioned": True}
            if class_name_match:
                class_info["name"] = class_name_match.group(1).strip()
            if day_match:
                class_info["day"] = day_match.group(1)
            if time_match:
                class_info["time"] = time_match.group(0)
            
            detected["classes"].append(class_info)
            detected["has_schedule_info"] = True
        
        # Assignment keywords (improved)
        assignment_keywords = ["assignment", "homework", "project", "due", "deadline", "submit", 
                             "i have an assignment", "my assignment", "due date", "homework due",
                             "project due", "assignment due", "need to submit", "need to turn in"]
        assignment_patterns = [
            r"assignment (due|is due|on)",
            r"homework (due|is due|on)",
            r"project (due|is due|on)",
            r"due (date|on|by)",
            r"deadline (is|on|for)"
        ]
        
        assignment_mentioned = any(re.search(r'\b' + re.escape(kw) + r'\b', text_lower) for kw in assignment_keywords) or \
                               any(re.search(pattern, text_lower) for pattern in assignment_patterns)
        
        if assignment_mentioned:
            # Try to extract assignment title, due date
            title_match = re.search(r"(?:assignment|homework|project)[\s:]+([A-Za-z0-9\s]+?)(?:due|$)", text_lower)
            date_match = re.search(r"(?:due|deadline)[\s:]+([A-Za-z0-9\s,]+)", text_lower)
            
            assignment_info = {"mentioned": True}
            if title_match:
                assignment_info["title"] = title_match.group(1).strip()
            if date_match:
                assignment_info["due_date_text"] = date_match.group(1).strip()
            
            detected["assignments"].append(assignment_info)
            detected["has_schedule_info"] = True
        
        return detected
    
    def get_reminder_context(self) -> str:
        """Get context about upcoming classes and assignments for LLM (improved)."""
        upcoming_assignments = self.get_upcoming_assignments(7)
        upcoming_classes = self.get_upcoming_classes(7)
        
        context_parts = []
        
        # Urgent assignments (due in 1-2 days)
        urgent_assignments = [a for a in upcoming_assignments if a.get("days_until", 999) <= 2]
        if urgent_assignments:
            context_parts.append("⚠️ URGENT - Assignments Due Soon:")
            for assignment in urgent_assignments[:3]:
                days = assignment.get("days_until", 0)
                title = assignment.get("title", "Untitled")
                class_name = assignment.get("class_name", "")
                urgency = "TODAY" if days == 0 else f"in {days} day{'s' if days > 1 else ''}"
                context_parts.append(f"- {title}{' (' + class_name + ')' if class_name else ''} - Due {urgency}")
        
        # Regular upcoming assignments
        regular_assignments = [a for a in upcoming_assignments if a.get("days_until", 999) > 2]
        if regular_assignments:
            context_parts.append("\n📚 Upcoming Assignments (next 7 days):")
            for assignment in regular_assignments[:5]:
                days = assignment.get("days_until", 0)
                title = assignment.get("title", "Untitled")
                class_name = assignment.get("class_name", "")
                context_parts.append(f"- {title}{' (' + class_name + ')' if class_name else ''} - Due in {days} days")
        
        # Today's classes
        today_classes = [c for c in upcoming_classes if c.get("days_until", 999) == 0]
        if today_classes:
            context_parts.append("\n📖 Classes Today:")
            for class_info in today_classes:
                context_parts.append(f"- {class_info['class']} at {class_info['time']}{' (' + class_info['location'] + ')' if class_info.get('location') else ''}")
        
        # Upcoming classes
        future_classes = [c for c in upcoming_classes if c.get("days_until", 999) > 0]
        if future_classes:
            context_parts.append("\n📖 Upcoming Classes:")
            for class_info in future_classes[:5]:
                days = class_info.get("days_until", 0)
                day_name = class_info.get("day", "")
                context_parts.append(f"- {class_info['class']} on {day_name} at {class_info['time']} (in {days} days)")
        
        if context_parts:
            return "\n".join(context_parts)
        
        return ""
    
    def check_reminders(self) -> List[str]:
        """
        Check for reminders and return list of reminder messages.
        Improved reminder system with better timing.
        """
        reminders = []
        today = datetime.datetime.now()
        
        # Check assignments due soon
        upcoming_assignments = self.get_upcoming_assignments(3)  # Next 3 days
        for assignment in upcoming_assignments:
            days = assignment.get("days_until", 0)
            title = assignment.get("title", "Untitled")
            class_name = assignment.get("class_name", "")
            
            if days == 0:
                reminders.append(f"⚠️ REMINDER: {title}{' (' + class_name + ')' if class_name else ''} is due TODAY!")
            elif days == 1:
                reminders.append(f"📝 Reminder: {title}{' (' + class_name + ')' if class_name else ''} is due tomorrow.")
            elif days == 2:
                reminders.append(f"📝 Reminder: {title}{' (' + class_name + ')' if class_name else ''} is due in 2 days.")
        
        # Check classes today
        today_classes = self.get_upcoming_classes(1)
        today_classes = [c for c in today_classes if c.get("days_until", 0) == 0]
        if today_classes:
            class_list = ", ".join([c["class"] for c in today_classes])
            reminders.append(f"📖 You have classes today: {class_list}")
        
        return reminders

