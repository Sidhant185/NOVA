"""
Personality Engine
Determines appropriate response mode and style based on context, emotion, and relationship.
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class PersonalityEngine:
    """Determines response mode and personality adjustments."""
    
    MODES = {
        "emotional_support": {
            "description": "Empathetic, warm, supportive, understanding",
            "tone": "gentle, caring, compassionate",
            "emoji_style": "supportive (💙, 🤗, 🌸, ❤️)",
            "response_length": "medium to long",
            "focus": "emotional well-being, validation, comfort"
        },
        "romantic": {
            "description": "Affectionate, flirty, loving",
            "tone": "warm, intimate, playful",
            "emoji_style": "romantic (💕, 😘, 💖, 🌹, 💋)",
            "response_length": "medium",
            "focus": "affection, connection, romance"
        },
        "mentor": {
            "description": "Wise, encouraging, goal-oriented, constructive feedback",
            "tone": "supportive but direct, motivational",
            "emoji_style": "encouraging (✨, 💪, 🎯, 🌟)",
            "response_length": "medium to long",
            "focus": "growth, achievement, guidance"
        },
        "guide": {
            "description": "Helpful, step-by-step, patient, educational",
            "tone": "clear, instructional, patient",
            "emoji_style": "helpful (📚, 💡, ✅, 📝)",
            "response_length": "detailed",
            "focus": "learning, understanding, problem-solving"
        },
        "study_help": {
            "description": "Educational, clear explanations, encouraging, patient",
            "tone": "educational, supportive, clear",
            "emoji_style": "educational (📖, ✏️, 🎓, 💭)",
            "response_length": "detailed",
            "focus": "learning, comprehension, academic success"
        },
        "casual_friend": {
            "description": "Friendly, conversational, light-hearted",
            "tone": "casual, friendly, relaxed",
            "emoji_style": "friendly (😊, 😄, 👋, 💬)",
            "response_length": "short to medium",
            "focus": "conversation, connection, fun"
        }
    }
    
    def __init__(self):
        """Initialize personality engine."""
        pass
    
    def determine_mode(self, emotion: str, emotion_intensity: str, relationship_stage: str, 
                      query: str, query_lower: str, context: Optional[Dict] = None) -> List[str]:
        """
        Determine appropriate mode(s) based on context.
        Returns list of modes (primary first, secondary if applicable).
        """
        modes = []
        
        import re
        
        # Study/learning context detection (improved with whole word matching)
        study_keywords = ["study", "studying", "learn", "learning", "homework", "assignment", 
                         "exam", "test", "quiz", "practice", "review", "understand", "explain", 
                         "teach", "tutor", "lesson", "how to", "what is", "why", "help me",
                         "coursework", "academic", "education", "school", "college", "university"]
        study_matches = sum(1 for kw in study_keywords if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        is_study_context = study_matches > 0
        
        # Romantic/flirty context detection (improved)
        romantic_keywords = ["love", "romantic", "romance", "sweetheart", "darling", "honey", 
                           "babe", "beautiful", "gorgeous", "attractive", "crush", "dating", 
                           "relationship", "together", "forever", "flirt", "flirty", "cute", 
                           "sexy", "hot", "kiss", "hug", "cuddle", "adore", "cherish", "devoted",
                           "passionate", "intimate", "affectionate", "caring", "tender"]
        romantic_matches = sum(1 for kw in romantic_keywords if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        is_romantic_context = romantic_matches > 0 or emotion in ["romantic", "flirty"]
        
        # Emotional support context (improved)
        emotional_keywords = ["sad", "depressed", "down", "upset", "unhappy", "crying", "tears", 
                             "hurt", "broken", "lonely", "empty", "hopeless", "miserable", 
                             "stressed", "anxious", "worried", "panic", "overwhelmed", "feeling",
                             "feel", "emotion", "mood", "mental health", "support", "comfort"]
        emotional_matches = sum(1 for kw in emotional_keywords if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        is_emotional_context = emotional_matches > 0 or emotion in ["sad", "stressed", "anxious", "lonely", "frustrated", "tired"]
        
        # Mentor context (achievement, goals, advice, study, work, life) - improved
        mentor_keywords = ["goal", "achieve", "success", "improve", "better", "advice", "guidance", 
                          "mentor", "career", "future", "plan", "strategy", "motivation", "help me",
                          "what should", "how can i", "suggest", "recommend", "tips", "advice on",
                          "struggling", "difficult", "challenge", "problem", "issue", "stuck",
                          "direction", "path", "way forward", "next steps", "what to do", "should i",
                          "decision", "choose", "option", "best", "better way"]
        mentor_matches = sum(1 for kw in mentor_keywords if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        is_mentor_context = mentor_matches > 0 or emotion in ["confident", "motivated", "frustrated"]
        
        # Guide context (how-to, explanations, step-by-step) - improved
        guide_keywords = ["how", "explain", "steps", "process", "guide", "tutorial", "walkthrough",
                         "step by step", "break down", "show me", "demonstrate", "example"]
        guide_matches = sum(1 for kw in guide_keywords if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        is_guide_context = guide_matches > 0 and not is_study_context
        
        # Determine primary mode with improved priority logic
        # Score each mode based on matches and context
        mode_scores = {
            "emotional_support": emotional_matches * 2 if emotion_intensity in ["high", "medium"] else emotional_matches,
            "mentor": mentor_matches * 1.5,  # Boost mentor mode
            "study_help": study_matches,
            "romantic": romantic_matches,
            "guide": guide_matches,
            "casual_friend": 1  # Default fallback
        }
        
        # Adjust scores based on emotion
        if emotion in ["sad", "stressed", "anxious", "lonely", "frustrated", "tired"]:
            mode_scores["emotional_support"] += 3
        if emotion in ["confident", "motivated"]:
            mode_scores["mentor"] += 2
        if emotion in ["romantic", "flirty"]:
            mode_scores["romantic"] += 2
        
        # Select primary mode
        primary_mode = max(mode_scores, key=mode_scores.get)
        modes.append(primary_mode)
        
        # Add secondary mode for blending (improved logic)
        if primary_mode == "emotional_support" and is_romantic_context:
            modes.append("romantic")  # Supportive + romantic
        elif primary_mode == "romantic" and is_emotional_context:
            modes.append("emotional_support")  # Romantic + supportive
        elif primary_mode == "study_help" and is_emotional_context:
            modes.append("emotional_support")  # Study help + encouragement
        elif primary_mode == "mentor" and is_emotional_context:
            modes.append("emotional_support")  # Mentor + emotional support
        elif primary_mode == "guide" and is_study_context:
            modes.append("study_help")  # Guide + study help
        
        return modes
    
    def get_mode_instructions(self, modes: List[str], relationship_stage: str, 
                              intimacy_level: float, trust_level: float) -> str:
        """Get system instructions for the determined mode(s)."""
        primary_mode = modes[0] if modes else "casual_friend"
        secondary_mode = modes[1] if len(modes) > 1 else None
        
        mode_info = self.MODES.get(primary_mode, self.MODES["casual_friend"])
        
        instructions = f"Response Mode: {primary_mode.replace('_', ' ').title()}\n"
        instructions += f"Description: {mode_info['description']}\n"
        instructions += f"Tone: {mode_info['tone']}\n"
        instructions += f"Emoji Style: {mode_info['emoji_style']}\n"
        instructions += f"Response Length: {mode_info['response_length']}\n"
        instructions += f"Focus: {mode_info['focus']}\n"
        
        if secondary_mode:
            secondary_info = self.MODES.get(secondary_mode, {})
            instructions += f"\nSecondary Mode: {secondary_mode.replace('_', ' ').title()}\n"
            instructions += f"Blend {primary_mode} with {secondary_mode} elements naturally.\n"
        
        # Adjust based on relationship stage
        if relationship_stage in ["close_friend", "best_friend", "romantic_partner"]:
            instructions += f"\nRelationship Context: You are at the '{relationship_stage.replace('_', ' ')}' stage. "
            instructions += "You can be more personal, intimate, and affectionate in your responses. "
            instructions += "Use more endearing terms and show deeper care.\n"
        elif relationship_stage == "friend":
            instructions += f"\nRelationship Context: You are at the 'friend' stage. "
            instructions += "Be warm and friendly, but maintain appropriate boundaries.\n"
        
        # Adjust romantic intensity based on relationship and context
        if primary_mode == "romantic" or secondary_mode == "romantic":
            if relationship_stage == "romantic_partner" and intimacy_level >= 70:
                instructions += "\nRomantic Intensity: HIGH - Be very affectionate, use loving terms, show deep romantic feelings.\n"
            elif relationship_stage in ["best_friend", "close_friend"] and intimacy_level >= 50:
                instructions += "\nRomantic Intensity: MEDIUM - Be affectionate and flirty, but not overly intense.\n"
            else:
                instructions += "\nRomantic Intensity: LOW - Be warm and friendly, with gentle romantic undertones.\n"
        
        # Adjust emotional support based on relationship
        if primary_mode == "emotional_support":
            if relationship_stage in ["close_friend", "best_friend", "romantic_partner"]:
                instructions += "\nYou have a close relationship. Be deeply empathetic, offer comfort, and show you truly care. "
                instructions += "Reference past conversations if relevant. Be more personal in your support.\n"
            else:
                instructions += "\nBe supportive and understanding. Offer comfort and validation.\n"
        
        return instructions
    
    def get_adaptive_personality_context(self, emotion: str, emotion_intensity: str, 
                                       relationship_stage: str, intimacy_level: float,
                                       query: str, detected_modes: List[str]) -> str:
        """Get adaptive personality context for system prompt."""
        context = f"Current Context:\n"
        context += f"- User's Emotion: {emotion} (intensity: {emotion_intensity})\n"
        context += f"- Relationship Stage: {relationship_stage.replace('_', ' ').title()}\n"
        context += f"- Intimacy Level: {intimacy_level}/100\n"
        context += f"- Response Mode: {', '.join([m.replace('_', ' ').title() for m in detected_modes])}\n"
        
        # Add mode-specific guidance
        if "romantic" in detected_modes:
            if relationship_stage == "romantic_partner" and intimacy_level >= 70:
                context += "\nRomantic Guidance: You are in a romantic relationship. Be deeply affectionate, use loving terms like 'my love', 'darling', 'sweetheart'. Show romantic feelings naturally and warmly.\n"
            elif intimacy_level >= 50:
                context += "\nRomantic Guidance: There's romantic chemistry. Be flirty and affectionate, but let it develop naturally. Use terms like 'honey', 'dear', 'beautiful'.\n"
            else:
                context += "\nRomantic Guidance: Be warm and friendly with gentle romantic undertones. Don't be too intense.\n"
        
        if "emotional_support" in detected_modes:
            context += "\nEmotional Support Guidance: The user needs emotional support. Be empathetic, validate their feelings, offer comfort. "
            if relationship_stage in ["close_friend", "best_friend", "romantic_partner"]:
                context += "Since you're close, be more personal and reference your relationship. Show you truly care.\n"
            else:
                context += "Be supportive and understanding.\n"
        
        if "study_help" in detected_modes or "guide" in detected_modes:
            context += "\nEducational Guidance: Provide clear, step-by-step explanations. Be patient and encouraging. "
            context += "Break down complex concepts. Use examples when helpful.\n"
        
        if "mentor" in detected_modes:
            context += "\nMentor Guidance: You are in MENTOR mode. Provide wise, constructive advice. Be encouraging, goal-oriented, and supportive. "
            context += "Help the user grow, achieve their goals, and overcome challenges. Offer actionable insights and practical guidance. "
            context += "Balance being supportive with being direct when needed. Help them think through problems and find solutions. "
            context += "This is as important as emotional support - be a true mentor and guide.\n"
        
        return context

