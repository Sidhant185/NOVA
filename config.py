"""
Configuration management for NOVA Assistant.
Centralizes all configuration loading and validation.
"""
import os
from dotenv import load_dotenv
from typing import Optional, Tuple

# Load environment variables
load_dotenv()


class Config:
    """Centralized configuration class."""
    
    # API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # User Configuration
    USERNAME: str = os.getenv("Username", "Sidhant")
    USER_ID: str = os.getenv("UserID", "Sidhant")
    ASSISTANT_NAME: str = os.getenv("AssistantName", "Nova")
    
    # Speech Recognition
    INPUT_LANGUAGE: str = os.getenv("InputLanguage", "en-US")
    
    # Text-to-Speech
    ASSISTANT_VOICE: str = os.getenv("AssistantVoice", "en-US-AriaNeural")
    TTS_ENABLED: bool = os.getenv("TTSEnabled", "true").lower() == "true"
    TTS_SPEED: str = os.getenv("TTSSpeed", "+1%")
    
    # Chat Settings
    MAX_CHAT_HISTORY: int = int(os.getenv("MaxChatHistory", "10"))
    
    # Logging
    LOG_LEVEL: str = os.getenv("LogLevel", "INFO")
    LOG_TO_FILE: bool = os.getenv("LogToFile", "true").lower() == "true"
    
    # Code Assistant (Cursor API)
    CURSOR_API_KEY: str = os.getenv("CURSOR_API_KEY", "")
    
    # Data Directory (for backward compatibility)
    DATA_DIR: str = "Data"
    
    @classmethod
    def validate(cls) -> Tuple[bool, Optional[str]]:
        """
        Validate required configuration.
        Returns (is_valid, error_message)
        """
        # At least one API key must be present
        if not cls.GROQ_API_KEY and not cls.GEMINI_API_KEY:
            return False, "❌ Missing API keys in .env file. Please add at least one: GROQ_API_KEY or GEMINI_API_KEY."
        
        if cls.USER_ID not in ["Sidhant", "default"]:
            return False, f"⚠️ UserID should be 'Sidhant' or 'default'. Found: {cls.USER_ID}"
        
        return True, None
    
    @classmethod
    def get_data_path(cls, filename: str) -> str:
        """Get path for data files."""
        return f"Data/{filename}"
    
    @classmethod
    def get_chat_log_path(cls) -> str:
        """Get path for chat log file."""
        return cls.get_data_path(f"{cls.USER_ID}_ChatLog.json")
    
    @classmethod
    def get_memory_path(cls) -> str:
        """Get path for memory file."""
        return cls.get_data_path(f"{cls.USER_ID}_Memory.json")

