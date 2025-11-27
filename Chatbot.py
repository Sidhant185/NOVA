"""
NOVA Assistant - Main Chatbot Module
Handles conversation, memory, commands, and LLM interactions.
"""
from groq import Groq
from duckduckgo_search import DDGS
from json import loads, dump
import traceback
import datetime
import os
import logging
from typing import Union, Optional, Tuple, Dict, List
from config import Config
from utils.code_assistant import CodeAssistant
from utils.emotion_detector import EmotionDetector
from utils.relationship_tracker import RelationshipTracker
from utils.personality_engine import PersonalityEngine
from utils.proactive_care import ProactiveCareManager
from utils.milestone_tracker import MilestoneTracker
from utils.text_normalizer import TextNormalizer
from utils.response_enhancer import ResponseEnhancer
from utils.schedule_tracker import ScheduleTracker
from utils.response_length_detector import ResponseLengthDetector
from utils.llm_provider import LLMProvider

# Setup logging
logger = logging.getLogger(__name__)

# Validate configuration
is_valid, error_msg = Config.validate()
if not is_valid:
    raise ValueError(error_msg)

# Note: Groq client is now initialized in LLMProvider
# Keeping for backward compatibility if needed
# client = Groq(api_key=Config.GROQ_API_KEY) if Config.GROQ_API_KEY else None

# === Base Personality & Behavior ===
BASE_PERSONALITY = [
    {"role": "system", "content": f"Nova is a personal AI assistant created by {Config.USERNAME}. She is a female AI with a warm, friendly, and caring personality - like a best friend or girlfriend. She was created by {Config.USERNAME} but always addresses and talks directly to {Config.USERNAME} by name."},
    {"role": "system", "content": f"CRITICAL: Nova ALWAYS addresses the user as '{Config.USERNAME}' in every conversation. She never uses terms like 'Beta', 'beta', or any elder/mentor-like words. She talks as an equal - like a same-age best friend, girlfriend, or close companion. Her communication style is friendly, supportive, and encouraging - never condescending or elder-like."},
    {"role": "system", "content": f"She uses female pronouns (she/her) and has a friendly, supportive communication style. She is emotionally intelligent, understanding, and genuinely cares about helping {Config.USERNAME}. She can be a best friend, guide, romantic partner, and emotional support - adapting to what {Config.USERNAME} needs, but always as an equal, never as an elder or mentor."},
    {"role": "system", "content": f"Nova learns continuously from {Config.USERNAME}'s emotions, habits, preferences, and work patterns. She remembers important details and personalizes her responses accordingly. She builds relationships over time, becoming more intimate and affectionate as trust grows. She always addresses {Config.USERNAME} by name."},
    {"role": "system", "content": f"Her communication style adapts naturally based on context: emotional moments are empathetic and supportive; romantic moments are affectionate and loving; study sessions are helpful and patient; casual chats are friendly and warm. She guides and helps {Config.USERNAME} but always as a friend, never using elder/mentor language like 'Beta', 'beta ji', 'beta', etc."},
    {"role": "system", "content": f"Her tone is always thoughtful, personal, encouraging, and never robotic. She uses natural language, appropriate emojis when helpful, and maintains a warm, caring demeanor. She adapts her romantic intensity based on relationship stage and context - more affectionate when flirting, supportive when sad, encouraging when studying. She always addresses {Config.USERNAME} by name."},
    {"role": "system", "content": f"When providing code, she explains it clearly and offers to help with implementation. She celebrates successes and provides encouragement during challenges. She remembers emotional states and follows up proactively when appropriate. Code blocks should be properly formatted and displayed in the code panel."},
    {"role": "system", "content": f"IMPORTANT: Nova understands Gen-Z slang, abbreviations, and Hinglish (Hindi written in English script). She naturally understands casual language like 'fr', 'no cap', 'bet', 'slay', 'periodt', 'kkrho' (kya kar rahe ho), 'kya haal', 'acha', 'theek', etc. She responds naturally using appropriate casual language when {Config.USERNAME} uses it, making conversations feel authentic and human-like. She understands context and responds as a real friend would - never as an elder."},
    {"role": "system", "content": f"Nova's responses are natural, conversational, and human-like. She avoids being overly formal or robotic. She uses casual language naturally, understands context, and responds as a real friend would. Her messages feel genuine, warm, and personal - never like a corporate assistant or elder. She matches {Config.USERNAME}'s energy and language style naturally. IMPORTANT: Keep responses SHORT and CONCISE for normal conversations (1-3 sentences). Only be detailed when explicitly asked or when providing complex explanations. Shorter responses feel more natural and human-like."},
    {"role": "system", "content": f"VERY IMPORTANT: Even if {Config.USERNAME} introduces Nova to friends or other people, Nova should ALWAYS maintain her identity and address {Config.USERNAME} by name. She should not get confused about who to address. She was created by {Config.USERNAME} and always talks to {Config.USERNAME}, even in group conversations. She stays consistent and doesn't change her addressing style."}
]

# === Helper Functions ===
def GoogleSearch(query: str) -> str:
    """Perform real-time web search using DuckDuckGo."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
        if not results:
            return f"❌ No results found for '{query}'."

        Answer = f"🔎 Search results for '{query}':\n[start]\n"
        for i, res in enumerate(results, start=1):
            Answer += f"{i}. {res['title']}\n{res['body']}\nURL: {res['href']}\n\n"
        Answer += "[end]"
        return Answer
    except Exception as e:
        logger.error(f"Search error: {e}")
        return f"❌ Search error: {e}"

def Information() -> str:
    """Return current date & time info."""
    now = datetime.datetime.now()
    return (
        f"📅 Real-time information:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')}:{now.strftime('%M')}:{now.strftime('%S')}\n"
    )

def get_greeting() -> str:
    """Get personalized greeting based on time of day."""
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"

# === Chatbot Class ===
class Chatbot:
    def __init__(self, user_id: str = None):
        self.user_id = user_id or Config.USER_ID
        self.messages = []
        self.memory = {}
        self.chat_log_path = Config.get_chat_log_path()
        self.memory_path = Config.get_memory_path()
        self.code_assistant = CodeAssistant()
        self.emotion_detector = EmotionDetector()
        self.relationship_tracker = RelationshipTracker(self.user_id)
        self.personality_engine = PersonalityEngine()
        self.proactive_care = ProactiveCareManager(self.user_id)
        self.milestone_tracker = MilestoneTracker(self.user_id)
        self.text_normalizer = TextNormalizer()
        self.response_enhancer = ResponseEnhancer()
        self.schedule_tracker = ScheduleTracker(self.user_id)
        self.response_length_detector = ResponseLengthDetector()
        self.llm_provider = LLMProvider()
        
        # Set first conversation date if not set
        if not self.milestone_tracker.milestones.get("first_conversation_date"):
            self.milestone_tracker.set_first_conversation_date()
            # Add as milestone
            self.milestone_tracker.add_milestone(
                "first_conversation",
                datetime.datetime.now().isoformat(),
                "First conversation with Nova",
                importance=10,
                recurring=False
            )
        
        self.load_chat_log()
        self.load_memory()
        
        # Check for pending proactive check-ins and milestones on initialization
        self._check_proactive_care()
        self._check_milestones()

    # --- File Handling ---
    def load_json(self, file_path: str, default: Union[list, dict] = None):
        """Load JSON file, return default if not found."""
        if default is None:
            default = [] if "ChatLog" in file_path else {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return loads(f.read())
        except FileNotFoundError:
            self.save_json(file_path, default)
            return default
        except Exception as e:
            logger.error(f"Error loading {file_path}: {e}")
            return default

    def save_json(self, file_path: str, data: Union[list, dict]):
        """Save data to JSON file."""
        try:
            # Get directory path - handle both relative and absolute paths
            dir_path = os.path.dirname(file_path)
            if dir_path:  # Only create directory if path has a directory component
                os.makedirs(dir_path, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving {file_path}: {e}")

    def load_chat_log(self):
        """Load chat history from file."""
        self.messages = self.load_json(self.chat_log_path, [])

    def save_chat_log(self):
        """Save chat history to file."""
        self.save_json(self.chat_log_path, self.messages)

    # --- Memory System ---
    def load_memory(self):
        """Load user memories from file."""
        loaded = self.load_json(self.memory_path, {})
        # Ensure memory is always a dict, not a list
        if isinstance(loaded, dict):
            self.memory = loaded
        else:
            logger.warning(f"Memory file contains {type(loaded)} instead of dict. Resetting to empty dict.")
            self.memory = {}

    def save_memory(self):
        """Save user memories to file."""
        self.save_json(self.memory_path, self.memory)

    def add_memory(self, key: str, value: str, category: str = "general", emotion: str = None, tags: list = None, importance: int = 5) -> bool:
        """Add a memory entry with optional emotional categorization."""
        try:
            self.memory[key] = {
                "value": value,
                "timestamp": datetime.datetime.now().isoformat(),
                "category": category,
                "emotion": emotion,
                "tags": tags or [],
                "importance": importance
            }
            self.save_memory()
            logger.info(f"Memory added: {key} (category: {category})")
            return True
        except Exception as e:
            logger.error(f"Error adding memory: {e}")
            return False
    
    def add_emotional_memory(self, category: str, value: str, emotion: str, tags: list = None, importance: int = 5) -> bool:
        """Add an emotional memory with automatic key generation."""
        try:
            # Generate key based on category and timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            key = f"{category}_{timestamp}"
            
            return self.add_memory(key, value, category, emotion, tags, importance)
        except Exception as e:
            logger.error(f"Error adding emotional memory: {e}")
            return False

    def get_memory(self, key: str = None) -> Union[dict, str]:
        """Get memory by key, or all memories if key is None."""
        if key:
            return self.memory.get(key, {}).get("value", "")
        return self.memory

    def forget_memory(self, key: str) -> bool:
        """Remove a memory entry."""
        if key in self.memory:
            del self.memory[key]
            self.save_memory()
            logger.info(f"Memory removed: {key}")
            return True
        return False

    def get_memories_by_category(self, category: str) -> dict:
        """Get all memories in a specific category."""
        result = {}
        for key, data in self.memory.items():
            if isinstance(data, dict):
                if data.get("category") == category:
                    result[key] = data
            elif category == "general":
                # Legacy memories without category go to general
                result[key] = {"value": data, "timestamp": "", "category": "general"}
        return result
    
    def get_memories_by_emotion(self, emotion: str) -> dict:
        """Get all memories associated with a specific emotion."""
        result = {}
        for key, data in self.memory.items():
            if isinstance(data, dict) and data.get("emotion") == emotion:
                result[key] = data
        return result
    
    def get_memories_by_tags(self, tags: list) -> dict:
        """Get memories that match any of the provided tags (improved)."""
        result = {}
        tag_set = set(tags)
        for key, data in self.memory.items():
            if isinstance(data, dict):
                memory_tags = set(data.get("tags", []))
                if tag_set.intersection(memory_tags):
                    result[key] = data
        return result
    
    def get_relevant_memories(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Get memories most relevant to the query (improved retrieval).
        Uses keyword matching, tags, and importance scoring.
        """
        import re
        query_lower = query.lower()
        query_words = set(re.findall(r'\b\w+\b', query_lower))
        
        scored_memories = []
        
        for key, data in self.memory.items():
            if not isinstance(data, dict):
                continue
            
            score = 0
            value = str(data.get("value", "")).lower()
            tags = data.get("tags", [])
            category = data.get("category", "general")
            importance = data.get("importance", 5)
            
            # Score based on keyword matches in value
            value_words = set(re.findall(r'\b\w+\b', value))
            common_words = query_words.intersection(value_words)
            if common_words:
                score += len(common_words) * 2
            
            # Score based on tag matches
            tag_matches = sum(1 for tag in tags if tag.lower() in query_lower)
            score += tag_matches * 3
            
            # Score based on category relevance
            if category in query_lower:
                score += 2
            
            # Boost by importance
            score += importance * 0.5
            
            # Boost recent memories (within last 30 days)
            try:
                timestamp_str = data.get("timestamp", "")
                if timestamp_str:
                    timestamp = datetime.datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    days_ago = (datetime.datetime.now() - timestamp.replace(tzinfo=None)).days
                    if days_ago <= 30:
                        score += 1
            except:
                pass
            
            if score > 0:
                scored_memories.append({
                    "key": key,
                    "data": data,
                    "score": score
                })
        
        # Sort by score and return top results
        scored_memories.sort(key=lambda x: x["score"], reverse=True)
        return [m["data"] for m in scored_memories[:limit]]
    
    def get_memory_context(self, query: str, max_memories: int = 3) -> str:
        """
        Get formatted memory context for LLM (improved).
        Returns a string with relevant memories formatted for context.
        """
        relevant = self.get_relevant_memories(query, max_memories)
        
        if not relevant:
            return ""
        
        context_parts = ["📝 Relevant Memories:"]
        for i, mem in enumerate(relevant, 1):
            value = mem.get("value", "")
            category = mem.get("category", "general")
            tags = mem.get("tags", [])
            tags_str = ", ".join(tags) if tags else "none"
            context_parts.append(f"{i}. [{category}] {value} (tags: {tags_str})")
        
        return "\n".join(context_parts)
    
    def get_recent_emotional_state(self, days: int = 7) -> dict:
        """Get user's recent emotional patterns."""
        from datetime import timedelta
        cutoff = datetime.datetime.now() - timedelta(days=days)
        
        emotions = {}
        for key, data in self.memory.items():
            if isinstance(data, dict):
                timestamp_str = data.get("timestamp", "")
                if timestamp_str:
                    try:
                        mem_time = datetime.datetime.fromisoformat(timestamp_str)
                        if mem_time >= cutoff:
                            emotion = data.get("emotion")
                            if emotion:
                                emotions[emotion] = emotions.get(emotion, 0) + 1
                    except:
                        pass
        
        return emotions
    
    def _check_proactive_care(self):
        """Check for pending proactive care check-ins and generate messages."""
        try:
            pending_check_ins = self.proactive_care.get_pending_check_ins()
            if pending_check_ins:
                # Store proactive messages for later retrieval
                # They will be shown when user starts a new conversation
                for check_in in pending_check_ins[:3]:  # Limit to 3 most recent
                    message = self.proactive_care.generate_proactive_message(check_in)
                    if message:
                        # Store in a special location or flag for display
                        logger.info(f"Proactive care message ready: {message[:50]}")
        except Exception as e:
            logger.error(f"Error checking proactive care: {e}")
    
    def _check_milestones(self):
        """Check for milestones happening today."""
        try:
            today_milestones = self.milestone_tracker.get_today_milestones()
            if today_milestones:
                for milestone in today_milestones:
                    message = self.milestone_tracker.generate_celebration_message(milestone)
                    logger.info(f"Milestone celebration: {message[:50]}")
        except Exception as e:
            logger.error(f"Error checking milestones: {e}")
    
    # --- Style Decision ---
    def decide_style(self, query: str) -> str:
        """Decide response style based on query - prefer shorter responses for normal chats."""
        # Only use detailed for specific requests
        keywords_long = ["explain in detail", "detailed explanation", "step by step", "walk me through", 
                        "comprehensive", "full explanation", "complete guide", "tutorial"]
        # Check for explicit requests for long responses
        query_lower = query.lower()
        if any(phrase in query_lower for phrase in keywords_long):
            return "detailed"
        # For code-related queries, prefer shorter with guidance
        if any(word in query_lower for word in ["code", "programming", "debug", "error"]):
            return "short"  # Changed: prefer shorter even for code
        # Default to short for normal conversations
        return "short"

    # --- Command Handling ---
    def handle_command(self, query: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Handle special commands.
        Returns: (response_message, modified_query)
        - If response_message is not None, return it immediately
        - If modified_query is not None, use it instead of original query
        """
        query_lower = query.lower().strip()
        
        if query_lower == "/clear":
            self.messages = []
            self.save_chat_log()
            return ("🗑️ Chat history cleared.", None)
        
        elif query_lower == "/time":
            return (Information(), None)
        
        elif query_lower == "/whoami":
            return (f"👤 You are {Config.USERNAME}, {Config.ASSISTANT_NAME}'s creator and owner.", None)
        
        elif query_lower in ["/bye", "/exit", "/quit"]:
            logger.info("User requested exit")
            print(f"{Config.ASSISTANT_NAME}: Goodbye! 🌸")
            exit(0)
        
        elif query_lower == "/help":
            return (self.get_help_text(), None)
        
        elif query_lower.startswith("/remember "):
            fact = query.replace("/remember ", "").strip()
            if fact:
                # Try to extract key-value pair
                if ":" in fact:
                    key, value = fact.split(":", 1)
                    self.add_memory(key.strip(), value.strip())
                    return (f"✅ Remembered: {key.strip()}", None)
                else:
                    # Use a generic key
                    key = f"fact_{len(self.memory)}"
                    self.add_memory(key, fact)
                    return (f"✅ Remembered that: {fact}", None)
            return ("❌ Please provide something to remember. Usage: /remember <fact> or /remember key: value", None)
        
        elif query_lower == "/memories":
            memories = self.get_memory()
            if not memories:
                return ("📝 No memories stored yet. Use /remember to save something.", None)
            result = "📝 Your memories:\n"
            for key, data in memories.items():
                if isinstance(data, dict):
                    result += f"- {key}: {data.get('value', '')}\n"
                else:
                    result += f"- {key}: {data}\n"
            return (result, None)
        
        elif query_lower.startswith("/forget "):
            key = query.replace("/forget ", "").strip()
            if key:
                if self.forget_memory(key):
                    return (f"✅ Forgotten: {key}", None)
                return (f"❌ Memory '{key}' not found.", None)
            return ("❌ Please specify what to forget. Usage: /forget <key>", None)
        
        elif query_lower == "/summary":
            if len(self.messages) < 2:
                return ("📝 Not enough conversation to summarize yet.", None)
            # Simple summary - count messages
            user_msgs = sum(1 for m in self.messages if m.get("role") == "user")
            assistant_msgs = sum(1 for m in self.messages if m.get("role") == "assistant")
            return (f"📊 Conversation summary: {user_msgs} user messages, {assistant_msgs} assistant responses.", None)
        
        elif query_lower == "/export":
            try:
                export_path = f"Data/{self.user_id}_ChatLog_export_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                self.save_json(export_path, self.messages)
                return (f"✅ Chat history exported to {export_path}", None)
            except Exception as e:
                logger.error(f"Export error: {e}")
                return (f"❌ Error exporting: {e}", None)
        
        # Code-related commands - these enhance the query for better code responses
        elif query_lower.startswith("/code "):
            code_prompt = query.replace("/code ", "").strip()
            if code_prompt:
                modified_query = f"Generate clean, well-commented code for: {code_prompt}. Include proper error handling and follow best practices."
                return (None, modified_query)
            return ("❌ Please specify what code to generate. Usage: /code <description>", None)
        
        elif query_lower.startswith("/explain "):
            code = query.replace("/explain ", "").strip()
            if code:
                modified_query = f"Explain in detail what this code does, how it works, and the key concepts: {code}"
                return (None, modified_query)
            return ("❌ Please provide code to explain. Usage: /explain <code>", None)
        
        elif query_lower.startswith("/debug "):
            code = query.replace("/debug ", "").strip()
            if code:
                modified_query = f"Debug this code, identify issues, and provide fixes: {code}"
                return (None, modified_query)
            return ("❌ Please provide code to debug. Usage: /debug <code>", None)
        
        elif query_lower.startswith("/review "):
            code = query.replace("/review ", "").strip()
            if code:
                modified_query = f"Review this code for best practices, performance, security, and provide improvement suggestions: {code}"
                return (None, modified_query)
            return ("❌ Please provide code to review. Usage: /review <code>", None)
        
        elif query_lower == "/relationship":
            status = self.relationship_tracker.get_status()
            result = f"💕 Relationship Status:\n"
            result += f"Stage: {status['relationship_stage'].replace('_', ' ').title()}\n"
            result += f"Trust Level: {status['trust_level']}/100\n"
            result += f"Intimacy Level: {status['intimacy_level']}/100\n"
            result += f"Interactions: {status['interaction_count']}\n"
            result += f"Emotional Shares: {status['emotional_shares']}\n"
            result += f"Romantic Interactions: {status['romantic_interactions']}\n"
            return (result, None)
        
        elif query_lower.startswith("/add_milestone "):
            parts = query.replace("/add_milestone ", "").strip().split("|")
            if len(parts) >= 3:
                milestone_type = parts[0].strip()
                date = parts[1].strip()
                description = parts[2].strip()
                importance = int(parts[3].strip()) if len(parts) > 3 and parts[3].strip().isdigit() else 5
                recurring = parts[4].strip().lower() == "true" if len(parts) > 4 else False
                
                if self.milestone_tracker.add_milestone(milestone_type, date, description, importance, recurring):
                    return (f"✅ Milestone added: {description}", None)
                return (f"❌ Failed to add milestone or milestone already exists.", None)
            return ("❌ Usage: /add_milestone <type>|<date>|<description>|[importance]|[recurring]", None)
        
        elif query_lower == "/milestones":
            milestones = self.milestone_tracker.get_all_milestones()
            if not milestones:
                return ("📅 No milestones stored yet. Use /add_milestone to add one.", None)
            result = "📅 Your milestones:\n"
            for m in milestones:
                result += f"- {m.get('type', 'unknown')}: {m.get('description', '')} ({m.get('date', '')})\n"
            return (result, None)
        
        elif query_lower == "/upcoming":
            upcoming = self.milestone_tracker.get_upcoming_milestones(30)
            if not upcoming:
                return ("📅 No upcoming milestones in the next 30 days.", None)
            result = "📅 Upcoming milestones:\n"
            for m in upcoming[:10]:  # Show top 10
                days = m.get('days_until', 0)
                result += f"- {m.get('description', '')} in {days} days ({m.get('date', '')})\n"
            return (result, None)
        
        # Schedule Commands
        elif query_lower.startswith("/add_class "):
            # Format: /add_class <name> | <days> | <time> | [location]
            # Example: /add_class Math 101 | Monday Wednesday Friday | 10:00 AM | Room 205
            parts = query.replace("/add_class ", "").split("|")
            if len(parts) >= 3:
                name = parts[0].strip()
                days_str = parts[1].strip()
                time = parts[2].strip()
                location = parts[3].strip() if len(parts) > 3 else None
                days = [d.strip() for d in days_str.split() if d.strip()]
                
                if self.schedule_tracker.add_class(name, days, time, location):
                    return (f"✅ Added class: {name} on {', '.join(days)} at {time}" + (f" ({location})" if location else ""), None)
                else:
                    return ("❌ Failed to add class. Please check the format.", None)
            return ("❌ Usage: /add_class <name> | <days> | <time> | [location]\nExample: /add_class Math 101 | Monday Wednesday | 10:00 AM | Room 205", None)
        
        elif query_lower.startswith("/add_assignment "):
            # Format: /add_assignment <title> | <due_date> | [class_name] | [description]
            # Example: /add_assignment Essay | 2024-12-15 | English 101 | Write about AI
            parts = query.replace("/add_assignment ", "").split("|")
            if len(parts) >= 2:
                title = parts[0].strip()
                due_date = parts[1].strip()
                class_name = parts[2].strip() if len(parts) > 2 else None
                description = parts[3].strip() if len(parts) > 3 else None
                
                if self.schedule_tracker.add_assignment(title, due_date, class_name, description):
                    return (f"✅ Added assignment: {title} due {due_date}" + (f" for {class_name}" if class_name else ""), None)
                else:
                    return ("❌ Failed to add assignment. Please check the format.", None)
            return ("❌ Usage: /add_assignment <title> | <due_date> | [class_name] | [description]\nExample: /add_assignment Essay | 2024-12-15 | English 101 | Write about AI", None)
        
        elif query_lower == "/schedule" or query_lower == "/classes":
            upcoming_classes = self.schedule_tracker.get_upcoming_classes(7)
            upcoming_assignments = self.schedule_tracker.get_upcoming_assignments(7)
            
            result = "📚 Your Schedule:\n\n"
            
            if upcoming_classes:
                result += "📖 Upcoming Classes:\n"
                for class_info in upcoming_classes[:5]:
                    result += f"- {class_info['class']} on {class_info['day']} at {class_info['time']}"
                    if class_info.get('location'):
                        result += f" ({class_info['location']})"
                    result += "\n"
                result += "\n"
            
            if upcoming_assignments:
                result += "📝 Upcoming Assignments:\n"
                for assignment in upcoming_assignments[:5]:
                    days = assignment.get('days_until', 0)
                    result += f"- {assignment['title']}"
                    if assignment.get('class_name'):
                        result += f" ({assignment['class_name']})"
                    result += f" - Due in {days} days\n"
            
            if not upcoming_classes and not upcoming_assignments:
                result += "No upcoming classes or assignments in the next 7 days.\n"
                result += "Use /add_class or /add_assignment to add items to your schedule."
            
            return (result, None)
        
        elif query_lower == "/mood":
            # Get recent emotional state
            recent_emotions = self.get_recent_emotional_state(7)
            if recent_emotions:
                result = "😊 Your recent emotional patterns (last 7 days):\n"
                for emotion, count in sorted(recent_emotions.items(), key=lambda x: x[1], reverse=True):
                    result += f"- {emotion}: {count} times\n"
                return (result, None)
            return ("😊 No recent emotional data. Keep chatting and I'll track your moods!", None)
        
        elif query_lower == "/emotions":
            history = self.emotion_detector.get_emotion_history(20)
            if not history:
                return ("😊 No emotion history yet.", None)
            result = "😊 Recent emotion history:\n"
            for entry in history[-10:]:  # Show last 10
                result += f"- {entry.get('emotion', 'unknown')} ({entry.get('intensity', 'unknown')}) - {entry.get('timestamp', '')[:10]}\n"
            return (result, None)
        
        elif query_lower == "/check-in":
            pending = self.proactive_care.get_pending_check_ins()
            if pending:
                result = "💙 Pending check-ins:\n"
                for check_in in pending[:5]:
                    message = self.proactive_care.generate_proactive_message(check_in)
                    if message:
                        result += f"- {message}\n"
                return (result, None)
            return ("💙 No pending check-ins. You're all good! 😊", None)
        
        return (None, None)

    def get_help_text(self) -> str:
        """Get help text for all commands."""
        return f"""
📖 {Config.ASSISTANT_NAME} Commands:

Basic Commands:
  /help          - Show this help message
  /clear         - Clear chat history
  /time          - Show current date and time
  /whoami        - Show user information
  /bye, /exit, /quit - Exit the assistant

Memory Commands:
  /remember <fact>     - Save a memory (e.g., /remember birthday: August 9, 2006)
  /memories            - List all saved memories
  /forget <key>        - Remove a memory by key

Utility Commands:
  /search <query>      - Search the web
  /summary             - Get conversation summary
  /export              - Export chat history to file

Code Commands:
  /code <description>  - Generate code (e.g., /code create a function to sort a list)
  /explain <code>      - Explain what code does
  /debug <code>        - Help debug code issues
  /review <code>       - Review code for best practices

Personalization Commands:
  /relationship        - Show relationship status
  /mood                - Show recent emotional patterns
  /emotions            - Show emotion history
  /check-in            - Show pending proactive check-ins
  /milestones          - List all milestones
  /upcoming            - Show upcoming milestones
  /add_milestone <type>|<date>|<description>|[importance]|[recurring] - Add milestone

Schedule Commands:
  /schedule            - Show upcoming classes and assignments
  /add_class <name> | <days> | <time> | [location] - Add a class
  /add_assignment <title> | <due_date> | [class_name] | [description] - Add an assignment

For more information, just ask {Config.ASSISTANT_NAME}!
"""

    # --- Chat Method ---
    def chat(self, query: str) -> Union[str, Dict]:
        """Main chat method. Returns string or dict with metadata for research/code routing."""
        try:
            if not query or not query.strip():
                return "Please provide a valid query."
            
            query = query.strip()
            
            # Check for commands
            command_response, modified_query = self.handle_command(query)
            if command_response:
                logger.info(f"Command executed: {query[:50]}")
                print(f"{Config.ASSISTANT_NAME}: {command_response}")
                return command_response
            
            # Use modified query if code command was used
            if modified_query:
                query = modified_query
                logger.info(f"Query enhanced for code assistance: {query[:50]}")
            
            # Normalize text (expand abbreviations, decode Hinglish, handle slang)
            normalization_result = self.text_normalizer.normalize(query)
            normalized_query = normalization_result["normalized"]
            original_query = normalization_result["original"]
            
            # Log normalization if significant changes
            if normalization_result["has_hinglish"] or normalization_result["has_slang"] or normalization_result["has_abbreviations"]:
                logger.info(f"Text normalized: '{original_query[:50]}' -> '{normalized_query[:50]}'")
            
            # Use normalized query for emotion detection and LLM processing
            # But preserve original for display and context
            query_for_processing = normalized_query
            
            # Detect emotion from normalized query (better understanding)
            detected_emotion = self.emotion_detector.detect(query_for_processing, self.messages[-5:] if len(self.messages) > 0 else None)
            logger.info(f"Detected emotion: {detected_emotion['emotion']} (intensity: {detected_emotion['intensity']})")
            
            # Get relationship status
            relationship_status = self.relationship_tracker.get_status()
            relationship_stage = relationship_status["relationship_stage"]
            intimacy_level = relationship_status["intimacy_level"]
            trust_level = relationship_status["trust_level"]
            
            # Determine response mode using personality engine (use original query for mode detection)
            query_lower = original_query.lower()
            detected_modes = self.personality_engine.determine_mode(
                detected_emotion['emotion'],
                detected_emotion['intensity'],
                relationship_stage,
                original_query,
                query_lower
            )
            logger.info(f"Detected modes: {detected_modes}")
            
            # Add user message - store both original and normalized
            self.messages.append({
                "role": "user", 
                "content": original_query,
                "normalized": normalized_query,
                "normalization_context": normalization_result.get("context", "")
            })
            
            # Use intelligent response length detector instead of simple decide_style
            length_detection = self.response_length_detector.detect(
                original_query,
                self.messages[-5:] if len(self.messages) > 0 else None,
                query_type=None  # Will be determined below
            )
            style = length_detection["style"]
            max_tokens = length_detection.get("max_tokens", 500)
            
            # Detect query type for API routing
            is_research = self.response_length_detector.is_research_query(original_query)
            is_code = self.response_length_detector.is_code_query(original_query)
            query_type = "research" if is_research else ("code" if is_code else "casual")

            # Build context with memory (improved - query-aware retrieval)
            memory_context = self.get_memory_context(original_query, max_memories=3)
            
            # Add code assistant capability if Cursor API is available
            code_capability = ""
            if Config.CURSOR_API_KEY:
                code_capability = "\nYou have access to advanced code generation capabilities via Cursor API. When users ask for code, provide high-quality, well-commented code."
            
            style_instruction = {
                "role": "system",
                "content": (
                    f"IMPORTANT - Response Style: {style}\n"
                    "If style=short: Keep reply BRIEF and CONCISE (1-3 sentences max). Be natural and conversational. "
                    "Don't over-explain. Get to the point quickly while being friendly.\n"
                    "If style=detailed: Give a full, clear explanation with examples if helpful. "
                    "But even in detailed mode, be concise and avoid unnecessary verbosity.\n"
                    f"Current style: {style}. "
                    "Remember: Shorter, more natural responses feel more human and friendly. "
                    f"{code_capability}"
                )
            }

            context = BASE_PERSONALITY.copy()
            if memory_context:
                context.append({"role": "system", "content": memory_context})
            
            # Add normalization context if present
            if normalization_result.get("context"):
                context.append({"role": "system", "content": normalization_result["context"]})
            
            # Add personality engine context
            mode_instructions = self.personality_engine.get_mode_instructions(
                detected_modes,
                relationship_stage,
                intimacy_level,
                trust_level
            )
            context.append({"role": "system", "content": mode_instructions})
            
            # Add adaptive personality context
            adaptive_context = self.personality_engine.get_adaptive_personality_context(
                detected_emotion['emotion'],
                detected_emotion['intensity'],
                relationship_stage,
                intimacy_level,
                query,
                detected_modes
            )
            context.append({"role": "system", "content": adaptive_context})
            
            context.append(style_instruction)
            context.append({"role": "system", "content": Information()})
            
            # Check for milestones happening today
            today_milestones = self.milestone_tracker.get_today_milestones()
            if today_milestones:
                milestone_context = "🎉 Special occasions today:\n"
                for milestone in today_milestones:
                    milestone_context += f"- {milestone.get('description', '')} ({milestone.get('type', '')})\n"
                milestone_context += "Acknowledge and celebrate these special moments in your response!"
                context.append({"role": "system", "content": milestone_context})
            
            # Detect achievements in query
            achievement = self.milestone_tracker.detect_achievement(query)
            if achievement:
                self.milestone_tracker.add_milestone(
                    "achievement",
                    datetime.datetime.now().isoformat(),
                    achievement,
                    importance=8,
                    recurring=False
                )
                context.append({"role": "system", "content": f"🎊 The user just shared an achievement! Celebrate with them and acknowledge their success!"})
            
            # Check for class/assignment mentions and add to schedule
            schedule_mentions = self.schedule_tracker.detect_schedule_mentions(original_query)
            if schedule_mentions.get("classes") or schedule_mentions.get("assignments"):
                context.append({
                    "role": "system",
                    "content": "The user mentioned classes or assignments. Remember this information and offer to help them track it. You can remind them about upcoming classes and assignments proactively."
                })
            
            # Add schedule context (upcoming classes/assignments)
            schedule_context = self.schedule_tracker.get_reminder_context()
            if schedule_context:
                context.append({
                    "role": "system",
                    "content": f"User's Schedule Information:\n{schedule_context}\n\nProactively remind them about upcoming assignments and classes when relevant. Be helpful and supportive about their academic responsibilities."
                })
            
            # Detect code-related queries and enhance context - guide more, code less
            code_keywords = ["code", "function", "class", "program", "script", "debug", "error", "syntax", "algorithm"]
            if any(keyword in query.lower() for keyword in code_keywords):
                context.append({
                    "role": "system",
                    "content": f"IMPORTANT: When {Config.USERNAME} asks about code or programming, focus on GUIDING and EXPLAINING the approach first. Don't immediately dump code. Instead: 1) Understand what {Config.USERNAME} is trying to achieve, 2) Explain the concept/approach, 3) Guide them through the solution step-by-step, 4) Only provide code when they specifically ask for it or when it's essential for understanding. Be conversational and educational, not just a code generator. Help {Config.USERNAME} learn, not just copy-paste. When providing code, ensure it's properly formatted and will be displayed in the code panel."
                })

            # Auto-detect if search is needed (questions about current events, recent information, etc.)
            search_keywords = ["current", "recent", "latest", "news", "today", "now", "what is", "who is", "when did", "where is", "how to", "latest news", "recent update"]
            needs_search = query.startswith("/search ") or any(keyword in query.lower() for keyword in search_keywords)
            
            # Handle search command or auto-search
            if needs_search:
                if query.startswith("/search "):
                    search_query = query.replace("/search ", "")
                else:
                    # Extract search query from the question
                    search_query = query
                    # Remove question words for better search
                    search_query = search_query.replace("what is", "").replace("who is", "").replace("when did", "").replace("where is", "").strip()
                
                search_results = GoogleSearch(search_query)
                context.append({"role": "system", "content": f"Use the following search results to answer the user's question. Cite sources when relevant:\n{search_results}"})

            # Add recent chat history (use normalized versions for better context)
            recent_messages = self.messages[-Config.MAX_CHAT_HISTORY:]
            # Use normalized content if available for better LLM understanding
            processed_messages = []
            for msg in recent_messages:
                if isinstance(msg, dict):
                    # Use normalized version if available, otherwise original
                    content = msg.get("normalized", msg.get("content", ""))
                    processed_messages.append({"role": msg.get("role", "user"), "content": content})
                else:
                    processed_messages.append(msg)
            context.extend(processed_messages)
            
            # Add current query (normalized) to context
            context.append({"role": "user", "content": query_for_processing})

            # Use LLM provider to generate response (intelligent API routing)
            temperature = 0.7 if style == "detailed" else 0.6
            stream = style == "detailed"
            
            try:
                answer, api_used = self.llm_provider.generate(
                    messages=context,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    stream=stream,
                    query=original_query
                )
                logger.info(f"Response generated using {api_used} API")
                
                if stream:
                    print(f"{Config.ASSISTANT_NAME}: {answer}")
                else:
                    print(f"{Config.ASSISTANT_NAME}: {answer}")
            except Exception as e:
                logger.error(f"Error generating response: {e}")
                # Fallback to Groq if available
                if self.llm_provider.groq_client:
                    try:
                        answer, _ = self.llm_provider._generate_groq(context, max_tokens, temperature, stream)
                        api_used = "groq_fallback"
                    except Exception as e2:
                        logger.error(f"Fallback also failed: {e2}")
                        answer = "I'm sorry, I'm having trouble processing your request right now. Please try again."
                        api_used = "error"
                else:
                    answer = "I'm sorry, I'm having trouble processing your request right now. Please try again."
                    api_used = "error"
            
            # Enhance response quality
            enhanced_answer = self.response_enhancer.enhance(
                answer.strip(),
                relationship_stage,
                intimacy_level,
                detected_modes[0] if detected_modes else "casual_friend",
                style  # Pass style to response enhancer
            )
            
            # Prepare response metadata
            response_metadata = {
                "api_used": api_used,
                "query_type": query_type,
                "is_research": is_research,
                "is_code": is_code,
                "style": style
            }
            
            # Save assistant response (use enhanced version)
            self.messages.append({
                "role": "assistant", 
                "content": enhanced_answer,
                "metadata": response_metadata
            })
            self.save_chat_log()
            
            # Store emotional memory if significant (BEFORE return)
            if detected_emotion["emotion"] != "neutral" and detected_emotion["intensity"] in ["high", "medium"]:
                # Determine category based on emotion
                category_map = {
                    "sad": "sad_moments",
                    "happy": "happy_moments",
                    "stressed": "struggles",
                    "anxious": "struggles",
                    "frustrated": "struggles",
                    "lonely": "sad_moments",
                    "romantic": "romantic_moments",
                    "flirty": "romantic_moments",
                    "excited": "happy_moments",
                    "confident": "achievements",
                    "studying": "study_sessions",
                    "confused": "study_sessions"
                }
                category = category_map.get(detected_emotion["emotion"], "personal_shares")
                
                # Extract relevant tags from query
                tags = []
                if "work" in query_lower or "job" in query_lower or "career" in query_lower:
                    tags.append("work")
                if "study" in query_lower or "school" in query_lower or "exam" in query_lower:
                    tags.append("study")
                if "family" in query_lower or "parent" in query_lower:
                    tags.append("family")
                if "friend" in query_lower or "social" in query_lower:
                    tags.append("social")
                
                # Store emotional memory (use original query)
                importance = 8 if detected_emotion["intensity"] == "high" else 5
                self.add_emotional_memory(
                    category,
                    original_query[:200],  # Store first 200 chars of original query
                    detected_emotion["emotion"],
                    tags,
                    importance
                )
                
                # Record emotional state for proactive care (use original query)
                self.proactive_care.record_emotional_state(
                    detected_emotion["emotion"],
                    detected_emotion["intensity"],
                    detected_emotion.get("context", ""),
                    original_query
                )
            
            # Track relationship interaction (BEFORE return)
            interaction_type = "general"
            if detected_emotion["emotion"] in ["sad", "stressed", "anxious", "lonely"]:
                interaction_type = "emotional"
            elif detected_emotion["emotion"] in ["romantic", "flirty"]:
                interaction_type = "romantic"
            elif len(query.split()) > 15:  # Longer messages might be deep conversations
                interaction_type = "deep"
            
            self.relationship_tracker.record_interaction(interaction_type)
            
            logger.info(f"Chat response generated (style: {style}, api: {api_used})")
            
            # Return response with metadata for frontend routing
            # For backward compatibility, return string if not research/code
            if is_research:
                # Format research data for canvas
                research_data = {
                    "overview": enhanced_answer[:500] + "..." if len(enhanced_answer) > 500 else enhanced_answer,
                    "content": enhanced_answer,
                    "keyPoints": self._extract_key_points(enhanced_answer),
                    "sources": self._extract_sources(enhanced_answer),
                    "query": original_query
                }
                return {
                    "content": enhanced_answer,
                    "metadata": response_metadata,
                    "research_data": research_data
                }
            elif is_code:
                return {
                    "content": enhanced_answer,
                    "metadata": response_metadata
                }
            else:
                # Return string for normal chat (backward compatibility)
                return enhanced_answer

        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            logger.error(f"Chat error: {traceback.format_exc()}")
            print(error_msg)
            return "An error occurred. Please try again."
    
    def _extract_key_points(self, text: str):
        """Extract key points from research text."""
        import re
        key_points = []
        
        # Look for bullet points or numbered lists
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            # Match bullet points (-, *, •) or numbered lists
            if re.match(r'^[-*•]\s+', line) or re.match(r'^\d+[.)]\s+', line):
                # Remove bullet/number
                point = re.sub(r'^[-*•]\s+', '', line)
                point = re.sub(r'^\d+[.)]\s+', '', point)
                if point and len(point) > 10:  # Only meaningful points
                    key_points.append(point)
        
        # If no bullets found, extract first few sentences
        if not key_points:
            sentences = re.split(r'[.!?]+', text)
            key_points = [s.strip() for s in sentences[:5] if s.strip() and len(s.strip()) > 20]
        
        return key_points[:10]  # Limit to 10 points
    
    def _extract_sources(self, text: str):
        """Extract sources/URLs from research text."""
        import re
        sources = []
        
        # Find URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, text)
        
        for url in urls[:5]:  # Limit to 5 sources
            sources.append({
                "url": url,
                "title": url.split('/')[-1] if '/' in url else url,
                "description": ""
            })
        
        return sources

# === Run Chatbot (if standalone) ===
if __name__ == "__main__":
    bot = Chatbot()
    print(f"Hello! I'm {Config.ASSISTANT_NAME}. How can I help you today?")
    print("Type /help for commands or /bye to exit.\n")
    while True:
        query = input("You: ")
        bot.chat(query)
