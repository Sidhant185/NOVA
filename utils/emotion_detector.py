"""
Emotion Detection Utility
Detects emotions from text using keywords, context, and conversation patterns.
"""
import re
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EmotionDetector:
    """Detects emotions from user messages."""
    
    # Emotion keywords with intensity indicators
    EMOTION_KEYWORDS = {
        "happy": {
            "keywords": ["happy", "joy", "excited", "great", "wonderful", "amazing", "fantastic", "love", "awesome", "yay", "celebrate", "success", "win", "achieved", "proud", "glad", "delighted", "thrilled", "ecstatic", "blissful", "cheerful", "jubilant", "elated", "euphoric", "radiant", "smiling", "grinning", "laughing", "grateful", "blessed"],
            "intensifiers": ["very", "extremely", "so", "really", "super", "incredibly", "absolutely", "completely", "totally", "utterly"]
        },
        "sad": {
            "keywords": ["sad", "depressed", "down", "upset", "unhappy", "crying", "tears", "hurt", "broken", "lonely", "empty", "hopeless", "miserable", "gloomy", "melancholy", "disappointed", "let down", "heartbroken", "devastated", "sorrowful", "dejected", "despondent", "dismal", "blue", "feeling low", "downhearted"],
            "intensifiers": ["very", "extremely", "so", "really", "deeply", "terribly", "absolutely", "completely", "utterly", "incredibly"]
        },
        "stressed": {
            "keywords": ["stressed", "stress", "pressure", "overwhelmed", "anxious", "worried", "panic", "deadline", "busy", "rushed", "tension", "nervous", "frazzled", "burnt out", "exhausted", "strained", "pressured", "swamped", "drowning", "can't cope", "too much", "breaking point"],
            "intensifiers": ["very", "extremely", "so", "really", "incredibly", "super", "absolutely", "completely", "totally"]
        },
        "anxious": {
            "keywords": ["anxious", "anxiety", "worried", "nervous", "fear", "afraid", "scared", "panic", "uneasy", "restless", "apprehensive", "tense", "jittery", "fretful", "on edge", "worried sick", "butterflies", "dread", "fearful", "terrified"],
            "intensifiers": ["very", "extremely", "so", "really", "incredibly", "absolutely", "completely", "terribly"]
        },
        "excited": {
            "keywords": ["excited", "thrilled", "pumped", "energized", "eager", "enthusiastic", "stoked", "hyped", "can't wait", "looking forward", "pumped up", "fired up", "jazzed", "amped", "buzzing", "ecstatic"],
            "intensifiers": ["very", "extremely", "so", "really", "super", "incredibly", "absolutely", "totally"]
        },
        "frustrated": {
            "keywords": ["frustrated", "annoyed", "irritated", "angry", "mad", "upset", "fed up", "sick of", "tired of", "can't stand", "hate", "disgusted", "aggravated", "exasperated", "irked", "bothered", "pissed", "fuming", "livid", "enraged"],
            "intensifiers": ["very", "extremely", "so", "really", "incredibly", "absolutely", "completely", "totally"]
        },
        "lonely": {
            "keywords": ["lonely", "alone", "isolated", "empty", "missing", "longing", "yearning", "homesick", "abandoned", "neglected", "disconnected", "detached", "solitary", "lonesome", "feeling alone", "no one", "by myself"],
            "intensifiers": ["very", "extremely", "so", "really", "deeply", "absolutely", "completely"]
        },
        "confident": {
            "keywords": ["confident", "sure", "certain", "positive", "optimistic", "ready", "prepared", "capable", "able", "strong", "powerful", "self-assured", "bold", "fearless", "determined", "motivated", "focused", "driven"],
            "intensifiers": ["very", "extremely", "so", "really", "absolutely", "completely"]
        },
        "romantic": {
            "keywords": ["love", "romantic", "romance", "sweetheart", "darling", "honey", "babe", "beautiful", "gorgeous", "attractive", "crush", "dating", "relationship", "together", "forever", "adore", "cherish", "devoted", "passionate", "intimate", "affectionate", "caring", "tender"],
            "intensifiers": ["very", "extremely", "so", "really", "deeply", "truly", "absolutely", "completely", "madly"]
        },
        "flirty": {
            "keywords": ["flirt", "flirty", "cute", "sexy", "hot", "attractive", "charming", "seductive", "teasing", "playful", "wink", "kiss", "hug", "cuddle", "smooth", "sweet", "adorable", "handsome", "pretty", "stunning"],
            "intensifiers": ["very", "extremely", "so", "really", "absolutely", "incredibly"]
        },
        "studying": {
            "keywords": ["study", "studying", "learn", "learning", "homework", "assignment", "exam", "test", "quiz", "practice", "review", "understand", "explain", "teach", "tutor", "lesson", "coursework", "academic", "education", "school", "college", "university"],
            "intensifiers": []
        },
        "confused": {
            "keywords": ["confused", "don't understand", "unclear", "lost", "puzzled", "bewildered", "perplexed", "baffled", "don't get it", "not sure", "uncertain", "mixed up", "disoriented", "muddled", "clueless", "stuck", "don't know"],
            "intensifiers": ["very", "extremely", "so", "really", "completely", "totally", "absolutely"]
        },
        "grateful": {
            "keywords": ["grateful", "thankful", "appreciate", "thanks", "thank you", "blessed", "fortunate", "lucky", "appreciation", "gratitude"],
            "intensifiers": ["very", "extremely", "so", "really", "deeply", "truly"]
        },
        "tired": {
            "keywords": ["tired", "exhausted", "sleepy", "drained", "worn out", "fatigued", "weary", "spent", "beat", "zoned out", "can't keep my eyes open"],
            "intensifiers": ["very", "extremely", "so", "really", "completely", "absolutely"]
        },
        "motivated": {
            "keywords": ["motivated", "inspired", "determined", "focused", "driven", "ambitious", "goal-oriented", "ready to", "want to", "going to", "planning to"],
            "intensifiers": ["very", "extremely", "so", "really", "absolutely"]
        }
    }
    
    # Context patterns for better detection (improved regex)
    CONTEXT_PATTERNS = {
        "feeling": r"\b(i|i'm|i am|im)\s+(feel|am feeling|'m feeling|feel like|feeling)\b",
        "emotion_statement": r"\b(i'm|i am|im)\s+([a-z\s]+?)(?:\.|!|\?|$)",
        "question_emotion": r"\b(how|why)\s+(.*?)(?:feeling|feel|emotion|doing)\b",
        "romantic_context": r"\b(you|your|together|us|we|relationship|dating|ours|ourselves)\b",
        "study_context": r"\b(help|explain|teach|learn|study|homework|assignment|exam|class|course)\b",
        "negative_context": r"\b(not|don't|doesn't|didn't|won't|can't|cannot|never|no|nothing|nobody|nowhere)\b",
        "positive_context": r"\b(yes|yeah|yep|sure|definitely|absolutely|of course|certainly|always)\b",
        "intensity_markers": r"\b(very|extremely|so|really|super|incredibly|absolutely|completely|totally|utterly)\b"
    }
    
    def __init__(self):
        """Initialize the emotion detector."""
        self.emotion_history = []  # Store emotion history for pattern analysis
    
    def detect(self, text: str, context: Optional[List[Dict]] = None) -> Dict:
        """
        Detect emotion from text.
        
        Args:
            text: The text to analyze
            context: Optional conversation context for better detection
            
        Returns:
            Dict with keys: emotion, intensity, context, keywords, confidence
        """
        if not text or not text.strip():
            return {
                "emotion": "neutral",
                "intensity": "low",
                "context": "",
                "keywords": [],
                "confidence": 0.0
            }
        
        text_lower = text.lower().strip()
        
        # Calculate emotion scores
        emotion_scores = {}
        detected_keywords = {}
        
        # Split text into words for proximity analysis
        words = text_lower.split()
        word_positions = {word: i for i, word in enumerate(words)}
        
        for emotion, data in self.EMOTION_KEYWORDS.items():
            score = 0
            found_keywords = []
            intensifier_boosts = 0
            
            # Check for keywords with whole word matching
            for keyword in data["keywords"]:
                # Whole word match (highest score) - using word boundaries
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    # Count occurrences
                    match_count = len(matches)
                    score += match_count * 3  # Increased weight for whole word matches
                    found_keywords.extend([keyword] * match_count)
            
            # Check for intensifiers with proximity analysis
            for intensifier in data.get("intensifiers", []):
                intensifier_pattern = r'\b' + re.escape(intensifier) + r'\b'
                intensifier_matches = re.finditer(intensifier_pattern, text_lower, re.IGNORECASE)
                
                for intensifier_match in intensifier_matches:
                    intensifier_start = intensifier_match.start()
                    # Check proximity to emotion keywords (within 5 words)
                    for keyword in data["keywords"]:
                        keyword_pattern = r'\b' + re.escape(keyword) + r'\b'
                        keyword_matches = re.finditer(keyword_pattern, text_lower, re.IGNORECASE)
                        
                        for keyword_match in keyword_matches:
                            keyword_start = keyword_match.start()
                            # Calculate word distance (approximate)
                            distance = abs(intensifier_start - keyword_start)
                            # If within ~30 characters (roughly 5 words), boost
                            if distance < 30:
                                score += 2  # Increased boost for proximity
                                intensifier_boosts += 1
                                break
                        if intensifier_boosts > 0:
                            break
            
            # Remove duplicates from found_keywords
            found_keywords = list(dict.fromkeys(found_keywords))
            
            if score > 0:
                emotion_scores[emotion] = score
                detected_keywords[emotion] = found_keywords
        
        # Check context patterns with improved logic
        context_boost = {}
        negative_context = bool(re.search(self.CONTEXT_PATTERNS["negative_context"], text_lower, re.IGNORECASE))
        positive_context = bool(re.search(self.CONTEXT_PATTERNS["positive_context"], text_lower, re.IGNORECASE))
        intensity_markers = len(re.findall(self.CONTEXT_PATTERNS["intensity_markers"], text_lower, re.IGNORECASE))
        
        for pattern_name, pattern in self.CONTEXT_PATTERNS.items():
            if pattern_name in ["negative_context", "positive_context", "intensity_markers"]:
                continue  # Handled separately
                
            if re.search(pattern, text_lower, re.IGNORECASE):
                # Boost relevant emotions based on context
                if pattern_name == "feeling" or pattern_name == "emotion_statement":
                    # Boost all detected emotions more significantly
                    for emotion in emotion_scores:
                        emotion_scores[emotion] = emotion_scores.get(emotion, 0) + 2
                elif pattern_name == "romantic_context":
                    emotion_scores["romantic"] = emotion_scores.get("romantic", 0) + 4
                    emotion_scores["flirty"] = emotion_scores.get("flirty", 0) + 3
                elif pattern_name == "study_context":
                    emotion_scores["studying"] = emotion_scores.get("studying", 0) + 4
                    emotion_scores["confused"] = emotion_scores.get("confused", 0) + 2
        
        # Apply negative/positive context adjustments
        if negative_context:
            # Reduce positive emotions, boost negative ones
            for emotion in ["happy", "excited", "confident", "grateful", "motivated"]:
                if emotion in emotion_scores:
                    emotion_scores[emotion] = max(0, emotion_scores[emotion] - 2)
            for emotion in ["sad", "frustrated", "anxious", "stressed"]:
                emotion_scores[emotion] = emotion_scores.get(emotion, 0) + 2
        
        if positive_context:
            # Boost positive emotions
            for emotion in ["happy", "excited", "confident", "grateful", "motivated"]:
                emotion_scores[emotion] = emotion_scores.get(emotion, 0) + 2
        
        # Apply intensity marker boost
        if intensity_markers > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] = emotion_scores.get(emotion, 0) + min(intensity_markers, 3)
        
        # Use conversation context if available (improved analysis)
        if context:
            recent_emotions = self._analyze_context(context)
            sentiment_trend = self._analyze_sentiment_trend(context)
            
            # Apply context boosts
            for emotion, boost in recent_emotions.items():
                emotion_scores[emotion] = emotion_scores.get(emotion, 0) + boost
            
            # Apply sentiment trend (emotional continuity)
            if sentiment_trend == "positive":
                for emotion in ["happy", "excited", "confident", "grateful"]:
                    emotion_scores[emotion] = emotion_scores.get(emotion, 0) + 1
            elif sentiment_trend == "negative":
                for emotion in ["sad", "frustrated", "anxious", "stressed", "lonely"]:
                    emotion_scores[emotion] = emotion_scores.get(emotion, 0) + 1
        
        # Determine primary emotion
        if not emotion_scores:
            return {
                "emotion": "neutral",
                "intensity": "low",
                "context": text[:100],
                "keywords": [],
                "confidence": 0.0
            }
        
        # Get top emotion
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[primary_emotion]
        
        # Calculate intensity based on score (improved thresholds)
        if max_score >= 12:
            intensity = "high"
        elif max_score >= 6:
            intensity = "medium"
        else:
            intensity = "low"
        
        # Calculate confidence (0-1) with improved formula
        total_score = sum(emotion_scores.values())
        if total_score == 0:
            confidence = 0.0
        else:
            # Confidence based on dominance of top emotion
            score_ratio = max_score / total_score
            # Also consider absolute score
            score_factor = min(max_score / 15.0, 1.0)  # Normalize to max expected score
            confidence = (score_ratio * 0.6 + score_factor * 0.4)
            confidence = min(confidence, 0.95)  # Cap at 0.95 to allow for uncertainty
        
        # Get keywords for primary emotion
        keywords = detected_keywords.get(primary_emotion, [])
        
        # Store in history
        self.emotion_history.append({
            "emotion": primary_emotion,
            "intensity": intensity,
            "timestamp": datetime.now().isoformat(),
            "text": text[:100]
        })
        
        # Keep only last 50 emotions
        if len(self.emotion_history) > 50:
            self.emotion_history = self.emotion_history[-50:]
        
        return {
            "emotion": primary_emotion,
            "intensity": intensity,
            "context": text[:200],
            "keywords": keywords[:5],  # Top 5 keywords
            "confidence": round(confidence, 2),
            "score": max_score,
            "all_scores": emotion_scores
        }
    
    def _analyze_context(self, context: List[Dict]) -> Dict[str, int]:
        """Analyze conversation context for emotion patterns (improved)."""
        boosts = {}
        
        # Look at last few messages for emotional continuity
        recent_messages = context[-5:] if len(context) > 5 else context
        
        # Track emotion history from context
        for msg in recent_messages:
            if msg.get("role") == "user":
                text = msg.get("content", "").lower()
                # Use whole word matching for better accuracy
                for emotion, data in self.EMOTION_KEYWORDS.items():
                    for keyword in data["keywords"]:
                        pattern = r'\b' + re.escape(keyword) + r'\b'
                        if re.search(pattern, text, re.IGNORECASE):
                            boosts[emotion] = boosts.get(emotion, 0) + 2  # Increased weight
                            break
        
        # Check emotion history for patterns
        if self.emotion_history:
            recent_history = self.emotion_history[-3:]  # Last 3 emotions
            for entry in recent_history:
                emotion = entry.get("emotion")
                intensity = entry.get("intensity", "low")
                if emotion:
                    # Boost based on recent emotional state
                    boost_value = 2 if intensity == "high" else 1
                    boosts[emotion] = boosts.get(emotion, 0) + boost_value
        
        return boosts
    
    def _analyze_sentiment_trend(self, context: List[Dict]) -> str:
        """Analyze sentiment trend from conversation context."""
        if not context:
            return "neutral"
        
        positive_count = 0
        negative_count = 0
        
        recent_messages = context[-5:] if len(context) > 5 else context
        
        for msg in recent_messages:
            if msg.get("role") == "user":
                text = msg.get("content", "").lower()
                # Check for positive indicators
                positive_keywords = ["happy", "great", "good", "love", "excited", "awesome", "wonderful", "amazing", "yes", "yeah"]
                negative_keywords = ["sad", "bad", "hate", "angry", "frustrated", "stressed", "worried", "no", "not", "don't"]
                
                pos_matches = sum(1 for kw in positive_keywords if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE))
                neg_matches = sum(1 for kw in negative_keywords if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE))
                
                positive_count += pos_matches
                negative_count += neg_matches
        
        if positive_count > negative_count + 2:
            return "positive"
        elif negative_count > positive_count + 2:
            return "negative"
        else:
            return "neutral"
    
    def get_emotion_history(self, limit: int = 20) -> List[Dict]:
        """Get recent emotion history."""
        return self.emotion_history[-limit:] if limit else self.emotion_history
    
    def get_emotion_stats(self) -> Dict:
        """Get emotion statistics."""
        if not self.emotion_history:
            return {
                "total": 0,
                "by_emotion": {},
                "by_intensity": {"low": 0, "medium": 0, "high": 0},
                "most_common": None
            }
        
        by_emotion = {}
        by_intensity = {"low": 0, "medium": 0, "high": 0}
        
        for entry in self.emotion_history:
            emotion = entry["emotion"]
            intensity = entry["intensity"]
            
            by_emotion[emotion] = by_emotion.get(emotion, 0) + 1
            by_intensity[intensity] = by_intensity.get(intensity, 0) + 1
        
        most_common = max(by_emotion, key=by_emotion.get) if by_emotion else None
        
        return {
            "total": len(self.emotion_history),
            "by_emotion": by_emotion,
            "by_intensity": by_intensity,
            "most_common": most_common
        }

