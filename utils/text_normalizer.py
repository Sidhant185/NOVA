"""
Text Normalizer
Normalizes text by expanding abbreviations, decoding Hinglish, and handling Gen-Z slang.
"""
import re
import logging
from typing import Dict, Tuple
from utils.hinglish_decoder import HinglishDecoder
from utils.genz_slang import GenZSlang

logger = logging.getLogger(__name__)

class TextNormalizer:
    """Normalizes text for better understanding."""
    
    def __init__(self):
        """Initialize text normalizer."""
        self.hinglish_decoder = HinglishDecoder()
        self.genz_slang = GenZSlang()
    
    def normalize(self, text: str) -> Dict[str, any]:
        """
        Normalize text by expanding abbreviations, decoding Hinglish, etc.
        
        Args:
            text: Original text to normalize
            
        Returns:
            Dict with:
                - original: Original text
                - normalized: Normalized text
                - has_hinglish: Boolean
                - has_slang: Boolean
                - has_abbreviations: Boolean
                - context: Context string for LLM
        """
        if not text or not text.strip():
            return {
                "original": text,
                "normalized": text,
                "has_hinglish": False,
                "has_slang": False,
                "has_abbreviations": False,
                "context": ""
            }
        
        original = text
        normalized = text
        
        # Step 1: Expand abbreviations
        normalized, has_abbreviations = self.genz_slang.expand_abbreviations(normalized)
        
        # Step 2: Decode Hinglish
        normalized, has_hinglish = self.hinglish_decoder.decode(normalized)
        
        # Step 3: Detect slang
        has_slang = self.genz_slang.detect_slang(original)
        
        # Step 4: Build context for LLM
        context_parts = []
        
        if has_hinglish:
            hinglish_context = self.hinglish_decoder.get_hinglish_context(original)
            if hinglish_context:
                context_parts.append(hinglish_context)
        
        if has_slang:
            slang_context = self.genz_slang.get_slang_context(original)
            if slang_context:
                context_parts.append(slang_context)
        
        if has_abbreviations:
            context_parts.append("The user used abbreviations which have been expanded for better understanding.")
        
        context = " ".join(context_parts)
        
        return {
            "original": original,
            "normalized": normalized,
            "has_hinglish": has_hinglish,
            "has_slang": has_slang,
            "has_abbreviations": has_abbreviations,
            "context": context
        }
    
    def normalize_simple(self, text: str) -> str:
        """Simple normalization that just returns normalized text."""
        result = self.normalize(text)
        return result["normalized"]

