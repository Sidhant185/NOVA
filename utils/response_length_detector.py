"""
Intelligent Response Length Detector
Automatically determines when detailed vs short responses are needed.
"""
import re
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ResponseLengthDetector:
    """Intelligently detects optimal response length based on query analysis."""
    
    # Keywords that indicate need for detailed response (improved with whole word matching)
    DETAILED_KEYWORDS = [
        "explain", "describe", "how does", "why does", "what is", "tell me about",
        "analyze", "compare", "discuss", "elaborate", "break down", "walk through",
        "guide me", "help me understand", "teach me", "show me how", "research",
        "find information", "investigate", "study", "deep dive", "comprehensive",
        "detailed", "full", "complete", "extensive", "thorough", "in-depth",
        "what are", "what were", "how can", "how do", "how did", "why is",
        "why are", "when did", "where did", "who is", "who are", "which",
        "difference", "similarities", "pros and cons", "advantages", "disadvantages",
        "benefits", "drawbacks", "examples", "instance", "case study"
    ]
    
    # Keywords that indicate need for short response
    SHORT_KEYWORDS = [
        "quick", "brief", "short", "simple", "just", "only", "yes or no",
        "one word", "tldr", "summary", "in a nutshell", "quickly", "fast",
        "yes", "no", "ok", "okay", "sure", "maybe", "probably", "possibly"
    ]
    
    # Code-related keywords (usually need detailed but structured)
    CODE_KEYWORDS = [
        "code", "function", "class", "program", "script", "debug", "error",
        "syntax", "algorithm", "implement", "create", "build", "develop",
        "programming", "coding", "software", "application", "api", "library",
        "framework", "module", "package", "variable", "method", "procedure"
    ]
    
    # Research-related keywords (always detailed)
    RESEARCH_KEYWORDS = [
        "research", "find information", "tell me about", "what is known about",
        "investigate", "study", "analyze", "explore", "discover", "information about",
        "learn about", "understand", "background", "history", "overview", "summary of"
    ]
    
    # Casual/social keywords (usually short)
    CASUAL_KEYWORDS = [
        "hey", "hi", "hello", "how are you", "what's up", "sup", "howdy",
        "morning", "afternoon", "evening", "night", "thanks", "thank you",
        "bye", "see you", "later", "goodbye"
    ]
    
    # Question complexity indicators
    COMPLEX_QUESTION_PATTERNS = [
        r"how\s+(does|do|did|can|will|should|would|might|could)",
        r"why\s+(does|do|did|is|are|was|were)",
        r"what\s+(are|is|were|was)\s+(the|all|some)",
        r"explain\s+(how|why|what|when|where)",
        r"compare\s+(and|or)",
        r"difference\s+between",
        r"relationship\s+between"
    ]
    
    def __init__(self):
        """Initialize response length detector."""
        pass
    
    def detect(self, query: str, recent_messages: Optional[List[Dict]] = None, 
               query_type: Optional[str] = None) -> Dict[str, any]:
        """
        Detect optimal response length and style.
        
        Args:
            query: User query
            recent_messages: Recent conversation history
            query_type: Pre-detected query type (research, code, casual, etc.)
            
        Returns:
            Dict with 'style' (short/detailed), 'reason', 'confidence', 'max_tokens'
        """
        if not query or not query.strip():
            return {
                "style": "short",
                "reason": "Empty query",
                "confidence": 1.0,
                "max_tokens": 150
            }
        
        query_lower = query.lower().strip()
        
        # Check for casual/social queries (usually short)
        casual_matches = sum(1 for kw in self.CASUAL_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        if casual_matches > 0 and len(query.split()) <= 5:
            return {
                "style": "short",
                "reason": "Casual/social query detected",
                "confidence": 0.9,
                "max_tokens": 100
            }
        
        # Check for explicit user preferences (whole word matching)
        short_keyword_matches = sum(1 for kw in self.SHORT_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        if short_keyword_matches > 0:
            return {
                "style": "short",
                "reason": "User explicitly requested short response",
                "confidence": 0.95,
                "max_tokens": 150
            }
        
        # Research queries always need detailed responses (will go to research canvas)
        research_matches = sum(1 for kw in self.RESEARCH_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        if research_matches > 0:
            return {
                "style": "detailed",
                "reason": "Research query detected - needs comprehensive response",
                "confidence": 0.9,
                "max_tokens": 2000,  # No limit for research
                "use_research_canvas": True
            }
        
        # Code queries need detailed but structured responses
        code_matches = sum(1 for kw in self.CODE_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        if code_matches > 0:
            return {
                "style": "detailed",
                "reason": "Code-related query - needs explanation and guidance",
                "confidence": 0.85,
                "max_tokens": 800,
                "use_code_panel": True
            }
        
        # Check for complex question patterns (improved matching)
        is_complex = any(re.search(pattern, query_lower) for pattern in self.COMPLEX_QUESTION_PATTERNS)
        
        # Check for detailed keywords (whole word matching)
        detailed_matches = sum(1 for kw in self.DETAILED_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        has_detailed_keywords = detailed_matches > 0
        
        # Analyze query length and structure
        word_count = len(query.split())
        has_question_mark = "?" in query
        has_multiple_sentences = len(re.split(r'[.!?]+', query)) > 2
        has_multiple_questions = query.count("?") > 1
        
        # Check for follow-up indicators
        follow_up_indicators = ["also", "and", "additionally", "furthermore", "moreover", "plus", "what about", "how about"]
        has_follow_ups = any(indicator in query_lower for indicator in follow_up_indicators)
        
        # Calculate complexity score (improved algorithm)
        complexity_score = 0.0
        
        # Base complexity from question patterns
        if is_complex:
            complexity_score += 0.35
        if has_detailed_keywords:
            # Weight by number of matches
            complexity_score += min(0.3 + (detailed_matches * 0.05), 0.5)
        if word_count > 20:
            complexity_score += 0.15
        elif word_count > 10:
            complexity_score += 0.08
        if has_multiple_sentences:
            complexity_score += 0.12
        if has_multiple_questions:
            complexity_score += 0.15
        if has_question_mark and word_count > 10:
            complexity_score += 0.1
        if has_follow_ups:
            complexity_score += 0.1
        
        # Check recent conversation context (improved)
        if recent_messages:
            # If last few messages were detailed, user might want continuation
            recent_style = self._analyze_recent_style(recent_messages)
            if recent_style == "detailed":
                complexity_score += 0.2
            
            # Check if user is asking for more details on previous topic
            if self._is_follow_up_query(query, recent_messages):
                complexity_score += 0.15
        
        # Determine style based on complexity score
        if complexity_score >= 0.5:
            style = "detailed"
            max_tokens = min(600 + int(complexity_score * 400), 1200)
            reason = f"Complex query detected (score: {complexity_score:.2f})"
        else:
            style = "short"
            max_tokens = 200
            reason = f"Simple query detected (score: {complexity_score:.2f})"
        
        confidence = min(0.5 + complexity_score, 0.95) if style == "detailed" else min(0.5 + (1 - complexity_score), 0.95)
        
        return {
            "style": style,
            "reason": reason,
            "confidence": confidence,
            "max_tokens": max_tokens,
            "complexity_score": complexity_score
        }
    
    def _analyze_recent_style(self, recent_messages: List[Dict]) -> str:
        """Analyze recent conversation style (improved)."""
        if not recent_messages:
            return "short"
        
        # Check last 3 assistant messages
        assistant_messages = [msg for msg in recent_messages[-5:] if msg.get("role") == "assistant"]
        
        if not assistant_messages:
            return "short"
        
        # Calculate average message length
        total_length = sum(len(msg.get("content", "").split()) for msg in assistant_messages)
        avg_length = total_length / len(assistant_messages)
        
        # Also check for detailed keywords in recent messages
        detailed_count = 0
        for msg in assistant_messages:
            content = msg.get("content", "").lower()
            if any(kw in content for kw in self.DETAILED_KEYWORDS[:10]):  # Check first 10 keywords
                detailed_count += 1
        
        # If most messages are detailed or average length is high, return detailed
        if avg_length > 50 or (detailed_count / len(assistant_messages)) > 0.5:
            return "detailed"
        return "short"
    
    def _is_follow_up_query(self, query: str, recent_messages: List[Dict]) -> bool:
        """Check if query is a follow-up to previous conversation."""
        if not recent_messages:
            return False
        
        query_lower = query.lower()
        follow_up_patterns = [
            r"what (about|is|are|was|were)",
            r"how (about|is|are|was|were)",
            r"tell me more",
            r"explain (more|further|in detail)",
            r"can you (elaborate|expand|clarify)",
            r"also",
            r"and (what|how|why|when|where)"
        ]
        
        # Check if query matches follow-up patterns
        if any(re.search(pattern, query_lower) for pattern in follow_up_patterns):
            return True
        
        # Check if query references previous topic
        if len(recent_messages) > 0:
            last_assistant_msg = None
            for msg in reversed(recent_messages):
                if msg.get("role") == "assistant":
                    last_assistant_msg = msg.get("content", "").lower()
                    break
            
            if last_assistant_msg:
                # Extract key terms from last message
                last_words = set(re.findall(r'\b\w{4,}\b', last_assistant_msg))
                query_words = set(re.findall(r'\b\w{4,}\b', query_lower))
                # If there's significant overlap, it's likely a follow-up
                if len(last_words & query_words) >= 2:
                    return True
        
        return False
    
    def is_research_query(self, query: str) -> bool:
        """Check if query is a research query (improved with whole word matching)."""
        query_lower = query.lower()
        return any(re.search(r'\b' + re.escape(kw) + r'\b', query_lower) for kw in self.RESEARCH_KEYWORDS)
    
    def is_code_query(self, query: str) -> bool:
        """Check if query is a code-related query (improved with whole word matching)."""
        query_lower = query.lower()
        return any(re.search(r'\b' + re.escape(kw) + r'\b', query_lower) for kw in self.CODE_KEYWORDS)

