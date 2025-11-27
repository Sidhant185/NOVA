"""
Gen-Z Slang Dictionary
Comprehensive dictionary of Gen-Z slang, abbreviations, and casual language.
"""
import re
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)

class GenZSlang:
    """Handles Gen-Z slang and abbreviations."""
    
    # Abbreviations and their expansions
    ABBREVIATIONS = {
        # Common abbreviations
        "lol": "laughing out loud",
        "lmao": "laughing my ass off",
        "lmfao": "laughing my fucking ass off",
        "omg": "oh my god",
        "omfg": "oh my fucking god",
        "wtf": "what the fuck",
        "tbh": "to be honest",
        "ngl": "not gonna lie",
        "fr": "for real",
        "frfr": "for real for real",
        "idk": "i don't know",
        "idc": "i don't care",
        "ikr": "i know right",
        "smh": "shaking my head",
        "fyi": "for your information",
        "imo": "in my opinion",
        "imho": "in my humble opinion",
        "nvm": "never mind",
        "ttyl": "talk to you later",
        "brb": "be right back",
        "gtg": "got to go",
        "wyd": "what you doing",
        "wbu": "what about you",
        "hbu": "how about you",
        "wym": "what you mean",
        "wydm": "what you doing man",
        "rn": "right now",
        "asap": "as soon as possible",
        "irl": "in real life",
        "fomo": "fear of missing out",
        "yolo": "you only live once",
        "fml": "fuck my life",
        "stfu": "shut the fuck up",
        "tmi": "too much information",
        "tbh": "to be honest",
        "ngl": "not gonna lie",
        "lowkey": "low key",
        "highkey": "high key",
        "bet": "bet",
        "cap": "lie",
        "no cap": "no lie",
        "facts": "facts",
        "deadass": "dead ass",
        "fr": "for real",
        "periodt": "period",
        "slay": "slay",
        "vibe": "vibe",
        "vibing": "vibing",
        "vibes": "vibes",
        "sus": "suspicious",
        "bussin": "bussin",
        "bussin'": "bussin",
        "bussin": "really good",
        "mid": "mid",
        "fire": "fire",
        "lit": "lit",
        "goat": "greatest of all time",
        "pog": "play of the game",
        "poggers": "poggers",
        "sheesh": "sheesh",
        "bruh": "bruh",
        "bro": "bro",
        "dude": "dude",
        "fam": "family",
        "bestie": "bestie",
        "bff": "best friends forever",
        "bae": "before anyone else",
        "ship": "relationship",
        "shipping": "shipping",
        "stan": "stan",
        "stanning": "stanning",
        "simp": "simp",
        "simping": "simping",
        "ghost": "ghost",
        "ghosting": "ghosting",
        "left on read": "left on read",
        "read": "read",
        "unread": "unread",
        "ty": "thank you",
        "tyvm": "thank you very much",
        "yw": "you're welcome",
        "np": "no problem",
        "ofc": "of course",
        "obv": "obviously",
        "obvs": "obviously",
        "prob": "probably",
        "probs": "probably",
        "def": "definitely",
        "defo": "definitely",
        "k": "okay",
        "kk": "okay okay",
        "ok": "okay",
        "okay": "okay",
        "alr": "alright",
        "alright": "alright",
        "ight": "alright",
        "aight": "alright",
        "yea": "yeah",
        "yeah": "yeah",
        "yep": "yep",
        "yup": "yup",
        "nah": "no",
        "nope": "nope",
        "yass": "yes",
        "yas": "yes",
        "yasss": "yes",
        "periodt": "period",
        "period": "period",
        "slay": "slay",
        "queen": "queen",
        "king": "king",
        "icon": "icon",
        "legend": "legend",
        "mood": "mood",
        "big mood": "big mood",
        "same": "same",
        "same energy": "same energy",
        "vibe check": "vibe check",
        "no cap": "no lie",
        "cap": "lie",
        "capping": "lying",
        "capper": "liar",
        "bet": "bet",
        "bet": "i agree",
        "say less": "say less",
        "say less": "understood",
        "say more": "say more",
        "spill": "spill",
        "spill the tea": "spill the tea",
        "tea": "tea",
        "spill tea": "spill tea",
        "no tea no shade": "no tea no shade",
        "shade": "shade",
        "throwing shade": "throwing shade",
        "drag": "drag",
        "dragging": "dragging",
        "read": "read",
        "reading": "reading",
        "clocked": "clocked",
        "clocking": "clocking",
        "snatched": "snatched",
        "snatching": "snatching",
        "wig": "wig",
        "wig snatched": "wig snatched",
        "wig flew": "wig flew",
        "crying": "crying",
        "dying": "dying",
        "dead": "dead",
        "i'm dead": "i'm dead",
        "i'm crying": "i'm crying",
        "i'm dying": "i'm dying",
        "i can't": "i can't",
        "i can't even": "i can't even",
        "i can't": "i can't handle this",
        "this": "this",
        "this is it": "this is it",
        "this is the one": "this is the one",
        "this hits different": "this hits different",
        "hits different": "hits different",
        "different": "different",
        "it's giving": "it's giving",
        "giving": "giving",
        "giving me": "giving me",
        "giving me life": "giving me life",
        "giving me energy": "giving me energy",
        "main character": "main character",
        "main character energy": "main character energy",
        "protagonist": "protagonist",
        "antagonist": "antagonist",
        "plot twist": "plot twist",
        "character development": "character development",
        "character arc": "character arc",
        "red flag": "red flag",
        "green flag": "green flag",
        "yellow flag": "yellow flag",
        "red flag": "warning sign",
        "green flag": "good sign",
        "yellow flag": "caution sign",
        "toxic": "toxic",
        "red flag": "red flag",
        "green flag": "green flag",
        "yellow flag": "yellow flag",
        "gaslight": "gaslight",
        "gaslighting": "gaslighting",
        "gatekeep": "gatekeep",
        "gatekeeping": "gatekeeping",
        "girlboss": "girlboss",
        "boss": "boss",
        "slay": "slay",
        "queen": "queen",
        "king": "king",
        "icon": "icon",
        "legend": "legend",
        "goat": "greatest of all time",
        "pog": "play of the game",
        "poggers": "poggers",
        "sheesh": "sheesh",
        "bruh": "bruh",
        "bro": "bro",
        "dude": "dude",
        "fam": "family",
        "bestie": "bestie",
        "bff": "best friends forever",
        "bae": "before anyone else",
        "ship": "relationship",
        "shipping": "shipping",
        "stan": "stan",
        "stanning": "stanning",
        "simp": "simp",
        "simping": "simping",
        "ghost": "ghost",
        "ghosting": "ghosting",
        "left on read": "left on read",
        "read": "read",
        "unread": "unread",
        "ty": "thank you",
        "tyvm": "thank you very much",
        "yw": "you're welcome",
        "np": "no problem",
        "ofc": "of course",
        "obv": "obviously",
        "obvs": "obviously",
        "prob": "probably",
        "probs": "probably",
        "def": "definitely",
        "defo": "definitely",
        "k": "okay",
        "kk": "okay okay",
        "ok": "okay",
        "okay": "okay",
        "alr": "alright",
        "alright": "alright",
        "ight": "alright",
        "aight": "alright",
        "yea": "yeah",
        "yeah": "yeah",
        "yep": "yep",
        "yup": "yup",
        "nah": "no",
        "nope": "nope",
        "yass": "yes",
        "yas": "yes",
        "yasss": "yes",
    }
    
    # Slang terms and their meanings (for context, not always expanded)
    SLANG_TERMS = {
        "bruh": "expression of surprise or disbelief",
        "fr": "for real",
        "no cap": "no lie, truthfully",
        "cap": "lie",
        "bet": "agreement or confirmation",
        "periodt": "emphasis, end of discussion",
        "slay": "doing something exceptionally well",
        "vibe": "atmosphere or feeling",
        "sus": "suspicious",
        "bussin": "really good",
        "mid": "mediocre",
        "fire": "excellent",
        "lit": "exciting or amazing",
        "goat": "greatest of all time",
        "pog": "play of the game",
        "sheesh": "expression of surprise or admiration",
        "bestie": "best friend",
        "bae": "before anyone else, significant other",
        "stan": "to be a big fan of",
        "simp": "someone who does too much for someone they like",
        "ghost": "to ignore someone",
        "tea": "gossip or information",
        "spill the tea": "share gossip",
        "shade": "subtle insult",
        "snatched": "looking good",
        "wig": "expression of shock or excitement",
        "mood": "relatable feeling",
        "main character": "protagonist of one's own life",
        "red flag": "warning sign",
        "green flag": "good sign",
        "toxic": "harmful or negative",
        "gaslight": "manipulate someone into questioning their reality",
        "gatekeep": "keep something exclusive",
        "girlboss": "strong, independent woman",
        "hits different": "feels special or unique",
        "it's giving": "it's giving off a certain vibe",
        "say less": "understood, no need to explain",
        "spill": "share information",
        "clocked": "exposed or caught",
        "reading": "criticizing or calling out",
        "dragging": "criticizing harshly",
        "crying": "laughing really hard",
        "dying": "laughing really hard",
        "dead": "laughing really hard",
        "i can't": "i can't handle this",
        "this": "this is it",
        "different": "special or unique",
        "giving": "giving off a vibe",
        "protagonist": "main character",
        "antagonist": "villain",
        "plot twist": "unexpected turn of events",
        "character development": "personal growth",
        "character arc": "character's journey",
        "yellow flag": "caution sign",
    }
    
    def __init__(self):
        """Initialize Gen-Z slang handler."""
        pass
    
    def expand_abbreviations(self, text: str) -> Tuple[str, bool]:
        """
        Expand abbreviations in text.
        
        Args:
            text: Text that may contain abbreviations
            
        Returns:
            Tuple of (expanded_text, has_abbreviations)
        """
        if not text:
            return text, False
        
        has_abbreviations = False
        words = text.split()
        expanded_words = []
        
        for word in words:
            # Remove punctuation for matching
            word_clean = re.sub(r'[^\w]', '', word)
            punctuation = re.sub(r'[\w]', '', word)
            
            word_lower = word_clean.lower()
            
            # Check for abbreviations
            if word_lower in self.ABBREVIATIONS:
                expanded = self.ABBREVIATIONS[word_lower]
                # Preserve original case
                if word_clean.isupper():
                    expanded = expanded.upper()
                elif word_clean and word_clean[0].isupper():
                    expanded = expanded.capitalize()
                # Add back punctuation
                expanded_words.append(expanded + punctuation)
                has_abbreviations = True
            else:
                expanded_words.append(word)
        
        if has_abbreviations:
            expanded_text = ' '.join(expanded_words)
        else:
            expanded_text = text
        
        return expanded_text, has_abbreviations
    
    def get_slang_context(self, text: str) -> str:
        """Get context about slang in text for LLM understanding."""
        text_lower = text.lower()
        found_slang = []
        
        for slang, meaning in self.SLANG_TERMS.items():
            if slang in text_lower:
                found_slang.append(f"{slang} (meaning: {meaning})")
        
        if found_slang:
            return f"Note: The user's message contains Gen-Z slang: {', '.join(found_slang[:5])}. Understand the casual, friendly tone and respond naturally."
        
        return ""
    
    def detect_slang(self, text: str) -> bool:
        """Detect if text contains Gen-Z slang."""
        text_lower = text.lower()
        for slang in self.SLANG_TERMS.keys():
            if slang in text_lower:
                return True
        return False

