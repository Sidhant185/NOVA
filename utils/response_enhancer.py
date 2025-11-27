"""
Response Enhancer
Enhances LLM responses to be more natural, human-like, and contextually appropriate.
"""
import re
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class ResponseEnhancer:
    """Enhances response quality and naturalness."""
    
    # Natural transition phrases
    TRANSITIONS = [
        "btw", "also", "speaking of which", "by the way", "oh and", "plus",
        "and", "plus", "also", "additionally", "furthermore", "moreover"
    ]
    
    # Casual connectors
    CASUAL_CONNECTORS = [
        "like", "you know", "i mean", "sort of", "kind of", "pretty much",
        "basically", "literally", "honestly", "tbh", "ngl"
    ]
    
    def __init__(self):
        """Initialize response enhancer."""
        pass
    
    def enhance(self, response: str, relationship_stage: str = "friend", 
                intimacy_level: float = 50.0, mode: str = "casual_friend", 
                style: str = "short") -> str:
        """
        Enhance response for better quality and naturalness.
        
        Args:
            response: Original LLM response
            relationship_stage: Current relationship stage
            intimacy_level: Intimacy level (0-100)
            mode: Response mode
            style: Response style (short/detailed)
            
        Returns:
            Enhanced response
        """
        if not response or not response.strip():
            return response
        
        enhanced = response.strip()
        
        # For short style, ensure it's actually short (max 3-4 sentences)
        # Natural truncation at sentence boundaries - no irritating phrases
        if style == "short":
            sentences = re.split(r'([.!?]+)', enhanced)
            # Recombine sentences with their punctuation
            combined_sentences = []
            for i in range(0, len(sentences) - 1, 2):
                if i + 1 < len(sentences):
                    combined_sentences.append(sentences[i] + sentences[i + 1])
                else:
                    combined_sentences.append(sentences[i])
            
            # Filter out empty sentences
            combined_sentences = [s.strip() for s in combined_sentences if s.strip()]
            
            if len(combined_sentences) > 4:
                # Keep first 3-4 sentences, end naturally
                enhanced = ' '.join(combined_sentences[:4])
                # Ensure it ends with proper punctuation
                if not re.search(r'[.!?]$', enhanced):
                    enhanced += '.'
        
        # Remove excessive newlines
        enhanced = re.sub(r'\n{3,}', '\n\n', enhanced)
        
        # Fix spacing issues
        enhanced = re.sub(r'\s+', ' ', enhanced)
        enhanced = re.sub(r'\s+([.,!?;:])', r'\1', enhanced)
        
        # Ensure proper sentence spacing
        enhanced = re.sub(r'([.!?])([A-Z])', r'\1 \2', enhanced)
        
        # Adjust formality based on relationship
        if relationship_stage in ["close_friend", "best_friend", "romantic_partner"]:
            enhanced = self._make_more_casual(enhanced, intimacy_level)
        elif relationship_stage == "stranger":
            enhanced = self._make_more_formal(enhanced)
        
        # Adjust based on mode
        if mode == "romantic":
            enhanced = self._add_romantic_touches(enhanced, intimacy_level)
        elif mode == "emotional_support":
            enhanced = self._enhance_emotional_support(enhanced)
        elif mode == "casual_friend":
            enhanced = self._make_more_casual(enhanced, intimacy_level)
        
        # Improve emoji usage (natural, not excessive)
        enhanced = self._improve_emoji_usage(enhanced)
        
        # Ensure natural flow
        enhanced = self._improve_flow(enhanced)
        
        return enhanced.strip()
    
    def _make_more_casual(self, text: str, intimacy_level: float) -> str:
        """Make text more casual based on intimacy level."""
        # Don't over-process, just ensure natural tone
        # The LLM should already handle this, but we can make minor adjustments
        return text
    
    def _make_more_formal(self, text: str) -> str:
        """Make text more formal."""
        # Minor adjustments for formality
        return text
    
    def _add_romantic_touches(self, text: str, intimacy_level: float) -> str:
        """Add romantic touches if appropriate."""
        # Don't over-process romantic responses
        # The LLM should already handle this based on personality engine
        return text
    
    def _enhance_emotional_support(self, text: str) -> str:
        """Enhance emotional support responses."""
        # Ensure empathetic tone is maintained
        return text
    
    def _improve_emoji_usage(self, text: str) -> str:
        """Improve emoji usage - natural, not excessive."""
        # Count emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE
        )
        
        emojis = emoji_pattern.findall(text)
        emoji_count = len(emojis)
        
        # If too many emojis, reduce them (keep first few)
        if emoji_count > 5:
            # Keep emojis but reduce frequency
            words = text.split()
            new_words = []
            emoji_seen = 0
            for word in words:
                if emoji_pattern.search(word):
                    if emoji_seen < 3:
                        new_words.append(word)
                        emoji_seen += 1
                    # Skip excessive emojis
                else:
                    new_words.append(word)
            text = ' '.join(new_words)
        
        return text
    
    def _improve_flow(self, text: str) -> str:
        """Improve text flow and readability."""
        # Ensure proper sentence structure
        sentences = re.split(r'([.!?]\s+)', text)
        improved_sentences = []
        
        for i, sentence in enumerate(sentences):
            if not sentence.strip():
                continue
            
            # Capitalize first letter of sentences
            if sentence and sentence[0].isalpha():
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
            
            improved_sentences.append(sentence)
        
        return ''.join(improved_sentences)
    
    def check_quality(self, response: str) -> Dict:
        """Check response quality metrics."""
        metrics = {
            "length": len(response),
            "word_count": len(response.split()),
            "sentence_count": len(re.split(r'[.!?]+', response)),
            "has_emoji": bool(re.search(r'[😀-🙏🌀-🗿]', response)),
            "emoji_count": len(re.findall(r'[😀-🙏🌀-🗿]', response)),
            "readability": "good" if 10 <= len(response.split()) <= 100 else "needs_improvement"
        }
        
        return metrics

