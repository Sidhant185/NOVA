"""
Hinglish Decoder
Decodes Hinglish (Hindi words written in English script) to proper form.
"""
import re
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class HinglishDecoder:
    """Decodes Hinglish transliteration patterns."""
    
    # Common Hindi words in English script
    HINDI_WORDS = {
        # Greetings and common phrases
        "kkrho": "kya kar rahe ho",
        "kkrha": "kya kar raha",
        "kkrhi": "kya kar rahi",
        "kya": "kya",
        "haan": "haan",
        "nahi": "nahi",
        "na": "na",
        "hain": "hain",
        "hai": "hai",
        "ho": "ho",
        "hoga": "hoga",
        "hogi": "hogi",
        "honge": "honge",
        
        # Common words
        "acha": "acha",
        "theek": "theek",
        "sahi": "sahi",
        "galat": "galat",
        "kyu": "kyu",
        "kaise": "kaise",
        "kab": "kab",
        "kahan": "kahan",
        "kya": "kya",
        "kisne": "kisne",
        "kisko": "kisko",
        "kisliye": "kisliye",
        
        # Actions
        "kar": "kar",
        "kara": "kara",
        "kari": "kari",
        "kiya": "kiya",
        "kiye": "kiye",
        "kar raha": "kar raha",
        "kar rahe": "kar rahe",
        "kar rahi": "kar rahi",
        "kar raha ho": "kar raha ho",
        "kar rahe ho": "kar rahe ho",
        "kar rahi ho": "kar rahi ho",
        
        # Questions
        "kya haal": "kya haal",
        "kya chal raha": "kya chal raha",
        "kya ho raha": "kya ho raha",
        "kaise ho": "kaise ho",
        "kya kar rahe ho": "kya kar rahe ho",
        "kya kar raha hai": "kya kar raha hai",
        "kya kar rahi hai": "kya kar rahi hai",
        
        # Common phrases
        "matlab": "matlab",
        "yaar": "yaar",
        "dost": "dost",
        "bhai": "bhai",
        "behen": "behen",
        "didi": "didi",
        "bhaiya": "bhaiya",
        
        # Feelings
        "achha": "achha",
        "bura": "bura",
        "thik": "thik",
        "mast": "mast",
        "zabardast": "zabardast",
        
        # Time and place
        "abhi": "abhi",
        "ab": "ab",
        "pehle": "pehle",
        "baad": "baad",
        "yahan": "yahan",
        "wahan": "wahan",
        "idhar": "idhar",
        "udhar": "udhar",
        
        # Common verbs
        "ja": "ja",
        "a": "a",
        "de": "de",
        "le": "le",
        "kar": "kar",
        "ho": "ho",
        "raha": "raha",
        "rahe": "rahe",
        "rahi": "rahi",
    }
    
    # Common Hinglish patterns with expansions
    PATTERNS = {
        r'\bkkrho\b': 'kya kar rahe ho',
        r'\bkkrha\b': 'kya kar raha',
        r'\bkkrhi\b': 'kya kar rahi',
        r'\bkya\s+haal\b': 'kya haal',
        r'\bkya\s+chal\s+raha\b': 'kya chal raha',
        r'\bkya\s+ho\s+raha\b': 'kya ho raha',
        r'\bkaise\s+ho\b': 'kaise ho',
        r'\bkya\s+kar\s+rahe\s+ho\b': 'kya kar rahe ho',
        r'\bkya\s+kar\s+raha\s+hai\b': 'kya kar raha hai',
        r'\bkya\s+kar\s+rahi\s+hai\b': 'kya kar rahi hai',
        r'\bhaan\s+yaar\b': 'haan yaar',
        r'\bnahi\s+yaar\b': 'nahi yaar',
        r'\bacha\s+theek\b': 'acha theek',
    }
    
    def __init__(self):
        """Initialize Hinglish decoder."""
        pass
    
    def decode(self, text: str) -> Tuple[str, bool]:
        """
        Decode Hinglish text.
        
        Args:
            text: Text that may contain Hinglish
            
        Returns:
            Tuple of (decoded_text, has_hinglish)
        """
        if not text:
            return text, False
        
        original_text = text
        decoded_text = text
        has_hinglish = False
        
        # Check for common Hinglish patterns
        text_lower = text.lower()
        
        # Apply pattern replacements
        for pattern, replacement in self.PATTERNS.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                decoded_text = re.sub(pattern, replacement, decoded_text, flags=re.IGNORECASE)
                has_hinglish = True
        
        # Check for individual Hindi words
        words = decoded_text.split()
        decoded_words = []
        for word in words:
            word_lower = word.lower()
            # Remove punctuation for matching
            word_clean = re.sub(r'[^\w]', '', word_lower)
            
            if word_clean in self.HINDI_WORDS:
                # Replace with expanded form, preserving original case/punctuation
                expanded = self.HINDI_WORDS[word_clean]
                # Preserve original word's punctuation
                punctuation = re.sub(r'[\w]', '', word)
                decoded_words.append(expanded + punctuation)
                has_hinglish = True
            else:
                decoded_words.append(word)
        
        if has_hinglish:
            decoded_text = ' '.join(decoded_words)
        
        return decoded_text, has_hinglish
    
    def detect_hinglish(self, text: str) -> bool:
        """Detect if text contains Hinglish."""
        _, has_hinglish = self.decode(text)
        return has_hinglish
    
    def get_hinglish_context(self, text: str) -> str:
        """Get context about Hinglish in text for LLM understanding."""
        if not self.detect_hinglish(text):
            return ""
        
        decoded, _ = self.decode(text)
        return f"Note: The user's message contains Hinglish (Hindi written in English script). The normalized form is: '{decoded}'. Understand the meaning and respond naturally, using appropriate language."

