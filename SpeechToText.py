"""
Speech-to-Text module for NOVA Assistant.
Uses speech_recognition library directly (removed Selenium dependency).
"""
import speech_recognition as sr
import logging
import mtranslate as mt
from typing import Optional
from config import Config

logger = logging.getLogger(__name__)

class SpeechRecognition:
    """Speech recognition class using direct speech_recognition library."""
    
    def __init__(self):
        """Initialize speech recognizer."""
        self.recognizer = sr.Recognizer()
        self.input_language = Config.INPUT_LANGUAGE
        
        # Try to set FLAC converter path (for macOS)
        try:
            sr.FLAC_CONVERTER = "/opt/homebrew/bin/flac"
        except:
            pass  # Will use default if not found
        
        logger.info(f"Speech recognition initialized with language: {self.input_language}")

    def QueryModifier(self, query: str) -> str:
        """
        Modify a query to ensure proper punctuation and formatting.
        
        Args:
            query: Raw query text
        
        Returns:
            Formatted query with proper punctuation
        """
        if not query:
            return ""
        
        new_query = query.lower().strip()
        query_words = new_query.split()
        
        if not query_words:
            return ""
        
        question_words = [
            "how", "what", "who", "where", "when", "why", "which", 
            "whose", "whom", "can you", "what's", "where's", "how's"
        ]

        # Check if it's a question
        is_question = any(word + " " in new_query for word in question_words)
        
        # Get last character
        last_char = query_words[-1][-1] if query_words else ""
        
        # Add appropriate punctuation
        if is_question:
            if last_char in ['.', '?', '!']:
                new_query = new_query[:-1] + "?"
            else:
                new_query += "?"
        else:
            if last_char in ['.', '?', '!']:
                new_query = new_query[:-1] + "."
            else:
                new_query += "."
        
        return new_query.capitalize()

    def recognize_speech(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Recognize speech from microphone.
        
        Args:
            timeout: Maximum seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for a phrase
        
        Returns:
            Recognized text or None if failed
        """
        try:
            with sr.Microphone() as source:
                logger.debug("Adjusting for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                logger.debug("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            
            logger.debug("Recognizing speech...")
            
            # Use Google Speech Recognition
            # Language code format: "en-US", "hi-IN", etc.
            text = self.recognizer.recognize_google(audio, language=self.input_language)
            
            logger.info(f"Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            logger.warning("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in speech recognition: {e}")
            return None

    def UniversalTranslator(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Recognize speech and translate to English if needed.
        
        Args:
            timeout: Maximum seconds to wait for speech
            phrase_time_limit: Maximum seconds for a phrase
        
        Returns:
            Formatted and translated text, or None if failed
        """
        text = self.recognize_speech(timeout, phrase_time_limit)
        
        if not text:
            return None
        
        # Translate if not English
        if self.input_language.lower()[:2] != "en":
            try:
                logger.info("Translating to English...")
                translated_text = mt.translate(text, "en")
                return self.QueryModifier(translated_text)
            except Exception as e:
                logger.error(f"Translation error: {e}")
                # Return original text if translation fails
                return self.QueryModifier(text)
        else:
            return self.QueryModifier(text)

if __name__ == "__main__":
    from utils.logger import setup_logging
    setup_logging()
    
    print("Speech Recognition Test Mode")
    print("Speak into your microphone (or Ctrl+C to exit):\n")
    
    speech_recognition = SpeechRecognition()
    while True:
        try:
            text = speech_recognition.UniversalTranslator()
            if text:
                print(f"Recognized: {text}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
