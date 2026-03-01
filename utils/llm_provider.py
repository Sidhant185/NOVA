"""
Multi-API LLM Provider
Intelligently routes queries to the best API (Gemini, Groq, or Cursor).
"""
import sys
import os

# Import compatibility fix FIRST - before any imports that might use importlib.metadata
# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    import compat  # This patches importlib.metadata for Python 3.9
except ImportError:
    pass  # If compat module doesn't exist, continue (might be Python 3.10+)

import logging
import re
from typing import Dict, List, Optional, Tuple, Any
from groq import Groq
import google.generativeai as genai
from config import Config

logger = logging.getLogger(__name__)

class LLMProvider:
    """Intelligent multi-API provider for routing queries to optimal LLM."""
    
    # Research keywords - use Gemini
    RESEARCH_KEYWORDS = [
        "research", "find information", "tell me about", "what is known about",
        "investigate", "study", "analyze", "explore", "discover", "comprehensive",
        "detailed analysis", "deep dive", "thorough"
    ]
    
    # Code keywords - use Cursor (if available) or Gemini
    CODE_KEYWORDS = [
        "code", "function", "class", "program", "script", "debug", "error",
        "syntax", "algorithm", "implement", "create", "build", "develop",
        "fix", "refactor", "optimize", "test", "deploy"
    ]
    
    # Fast response keywords - use Groq
    FAST_KEYWORDS = [
        "quick", "fast", "simple", "just", "yes or no", "brief", "short answer"
    ]
    
    def __init__(self):
        """Initialize LLM provider with available APIs."""
        self.groq_client = None
        self.gemini_client = None
        self.cursor_api_key = None
        
        # Initialize Groq
        if Config.GROQ_API_KEY:
            try:
                self.groq_client = Groq(api_key=Config.GROQ_API_KEY)
                logger.info("Groq API initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Groq: {e}")
        
        # Initialize Gemini
        if Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.gemini_client = genai.GenerativeModel('gemini-pro')
                logger.info("Gemini API initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini: {e}")
        
        # Check Cursor API
        if Config.CURSOR_API_KEY:
            self.cursor_api_key = Config.CURSOR_API_KEY
            logger.info("Cursor API key available")
    
    def select_api(self, query: str, query_type: Optional[str] = None) -> Tuple[str, str]:
        """
        Select the best API for the given query (improved routing logic).
        
        Args:
            query: User query
            query_type: Pre-detected query type (research, code, casual)
            
        Returns:
            Tuple of (api_name, reason)
        """
        query_lower = query.lower()
        
        # Research queries -> Gemini (best for comprehensive responses)
        research_matches = sum(1 for kw in self.RESEARCH_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        if query_type == "research" or research_matches > 0:
            if self.gemini_client:
                return ("gemini", "Research query - Gemini provides comprehensive responses")
            elif self.groq_client:
                return ("groq", "Research query - Gemini unavailable, using Groq")
            else:
                return ("groq", "No API available, using Groq as fallback")
        
        # Code queries -> Cursor (if available) or Gemini (better for code explanations)
        code_matches = sum(1 for kw in self.CODE_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        if query_type == "code" or code_matches > 0:
            if self.cursor_api_key:
                return ("cursor", "Code query - Cursor API optimized for code")
            elif self.gemini_client:
                return ("gemini", "Code query - Cursor unavailable, using Gemini for better code understanding")
            elif self.groq_client:
                return ("groq", "Code query - Using Groq as fallback")
            else:
                return ("groq", "No API available")
        
        # Fast/simple queries -> Groq (fastest)
        fast_matches = sum(1 for kw in self.FAST_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', query_lower))
        if fast_matches > 0:
            if self.groq_client:
                return ("groq", "Fast query - Groq provides fastest responses")
            elif self.gemini_client:
                return ("gemini", "Fast query - Groq unavailable, using Gemini")
            else:
                return ("groq", "No API available")
        
        # Default: Analyze complexity more intelligently
        word_count = len(query.split())
        has_question = "?" in query
        has_multiple_questions = query.count("?") > 1
        has_complex_patterns = bool(re.search(r'\b(how|why|what|when|where|which|who)\s+', query_lower))
        is_complex = word_count > 15 or has_multiple_questions or (has_question and has_complex_patterns)
        
        if is_complex:
            if self.gemini_client:
                return ("gemini", "Complex query - Gemini provides better reasoning and context understanding")
            elif self.groq_client:
                return ("groq", "Complex query - Gemini unavailable, using Groq")
        else:
            if self.groq_client:
                return ("groq", "Simple query - Groq provides fast responses")
            elif self.gemini_client:
                return ("gemini", "Simple query - Groq unavailable, using Gemini")
        
        # Final fallback
        return ("groq", "Default fallback")
    
    def generate(self, messages: List[Dict], model: Optional[str] = None,
                 max_tokens: int = 500, temperature: float = 0.7,
                 stream: bool = False, query: Optional[str] = None) -> Tuple[str, str]:
        """
        Generate response using the best API.
        
        Args:
            messages: Conversation messages
            model: Specific model to use (optional)
            max_tokens: Maximum tokens
            temperature: Temperature
            stream: Whether to stream response
            query: Original query for API selection
            
        Returns:
            Tuple of (response, api_used)
        """
        # Select API if not specified
        if not model and query:
            api_name, reason = self.select_api(query)
        else:
            # Try to infer from model name
            if model and "gemini" in model.lower():
                api_name = "gemini"
            elif model and "groq" in model.lower():
                api_name = "groq"
            else:
                api_name, reason = self.select_api(messages[-1].get("content", "") if messages else "")
        
        logger.info(f"Using API: {api_name}")
        
        try:
            if api_name == "gemini" and self.gemini_client:
                return self._generate_gemini(messages, max_tokens, temperature, stream), "gemini"
            elif api_name == "groq" and self.groq_client:
                return self._generate_groq(messages, max_tokens, temperature, stream), "groq"
            elif api_name == "cursor" and self.cursor_api_key:
                return self._generate_cursor(messages, max_tokens, temperature), "cursor"
            else:
                # Fallback chain
                if self.groq_client:
                    return self._generate_groq(messages, max_tokens, temperature, stream), "groq"
                elif self.gemini_client:
                    return self._generate_gemini(messages, max_tokens, temperature, stream), "gemini"
                else:
                    raise Exception("No API available")
        except Exception as e:
            logger.error(f"Error with {api_name} API: {e}", exc_info=True)
            # Try fallback with better error handling
            fallback_attempted = False
            if api_name != "groq" and self.groq_client:
                try:
                    logger.info("Falling back to Groq")
                    return self._generate_groq(messages, max_tokens, temperature, stream), "groq"
                except Exception as fallback_error:
                    logger.error(f"Groq fallback also failed: {fallback_error}")
                    fallback_attempted = True
            
            if not fallback_attempted and api_name != "gemini" and self.gemini_client:
                try:
                    logger.info("Falling back to Gemini")
                    return self._generate_gemini(messages, max_tokens, temperature, stream), "gemini"
                except Exception as fallback_error:
                    logger.error(f"Gemini fallback also failed: {fallback_error}")
            
            # If all APIs failed, raise with helpful message
            raise Exception(f"All API attempts failed. Last error: {str(e)}")
    
    def _generate_groq(self, messages: List[Dict], max_tokens: int,
                      temperature: float, stream: bool = False) -> str:
        """Generate response using Groq API."""
        # Convert messages format
        groq_messages = []
        for msg in messages:
            if isinstance(msg, dict):
                groq_messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
        
        model = "llama-3.1-8b-instant"
        
        if stream:
            response_text = ""
            completion = self.groq_client.chat.completions.create(
                model=model,
                messages=groq_messages,
                max_tokens=max_tokens,
                temperature=temperature,
                stream=True
            )
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    response_text += chunk.choices[0].delta.content
            return response_text
        else:
            completion = self.groq_client.chat.completions.create(
                model=model,
                messages=groq_messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return completion.choices[0].message.content
    
    def _generate_gemini(self, messages: List[Dict], max_tokens: int,
                        temperature: float, stream: bool = False) -> str:
        """Generate response using Gemini API (improved format handling)."""
        try:
            # Convert messages to Gemini format
            # Gemini uses a different message format
            prompt_parts = []
            system_parts = []
            
            for msg in messages:
                role = msg.get("role", "user")
                content = msg.get("content", "")
                
                if role == "system":
                    # Collect all system messages
                    system_parts.append(content)
                elif role == "user":
                    prompt_parts.append(f"User: {content}\n")
                elif role == "assistant":
                    prompt_parts.append(f"Assistant: {content}\n")
            
            # Prepend all system messages at the beginning
            if system_parts:
                system_text = "\n".join(system_parts)
                full_prompt = f"System Instructions:\n{system_text}\n\n" + "".join(prompt_parts)
            else:
                full_prompt = "".join(prompt_parts)
            
            # Configure generation with improved settings
            generation_config = {
                "temperature": min(max(temperature, 0.0), 1.0),  # Clamp between 0 and 1
                "max_output_tokens": min(max_tokens, 8192),  # Gemini max is 8192
            }
            
            if stream:
                # Handle streaming (if supported)
                response = self.gemini_client.generate_content(
                    full_prompt,
                    generation_config=generation_config,
                    stream=True
                )
                # Collect streamed chunks
                full_text = ""
                for chunk in response:
                    if chunk.text:
                        full_text += chunk.text
                return full_text
            else:
                response = self.gemini_client.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )
                return response.text
        except Exception as e:
            logger.error(f"Gemini API error: {e}", exc_info=True)
            raise
    
    def _generate_cursor(self, messages: List[Dict], max_tokens: int,
                         temperature: float) -> str:
        """Generate response using Cursor API (for code-specific tasks)."""
        # Cursor API implementation would go here
        # For now, fallback to Gemini or Groq for code
        # This can be enhanced when Cursor API details are available
        
        # Extract code-related context
        code_context = ""
        for msg in messages:
            if "code" in msg.get("content", "").lower():
                code_context += msg.get("content", "") + "\n"
        
        # Use Gemini for code if available, else Groq
        if self.gemini_client:
            return self._generate_gemini(messages, max_tokens, temperature)
        elif self.groq_client:
            return self._generate_groq(messages, max_tokens, temperature)
        else:
            raise Exception("No API available for code generation")

