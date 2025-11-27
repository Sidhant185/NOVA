"""
NOVA Assistant - Main Entry Point
Voice-enabled AI assistant with speech recognition and text-to-speech.
"""
import signal
import sys
import argparse
import logging
from typing import Optional
from Chatbot import Chatbot
from TextToSpeech import TextToSpeech
from SpeechToText import SpeechRecognition
from utils.logger import setup_logging
from config import Config

logger = logging.getLogger(__name__)

# Global variables for graceful shutdown
chatbot = None
running = True

def signal_handler(sig, frame):
    """Handle interrupt signals for graceful shutdown."""
    global running
    logger.info("Shutdown signal received")
    print(f"\n{Config.ASSISTANT_NAME}: Goodbye! 🌸")
    running = False
    sys.exit(0)

def listen_to_audio() -> Optional[str]:
    """
    Listen to audio input and return recognized text.
    
    Returns:
        Recognized text or None if failed
    """
    try:
        speech_rec = SpeechRecognition()
        text = speech_rec.UniversalTranslator(timeout=5, phrase_time_limit=10)
        return text
    except Exception as e:
        logger.error(f"Error in speech recognition: {e}")
        print("❌ Error with speech recognition. Please try again.")
        return None

def main_voice_mode():
    """Run NOVA in voice mode."""
    global chatbot, running
    
    logger.info("Starting NOVA in voice mode")
    chatbot = Chatbot()
    
    print(f"🎤 {Config.ASSISTANT_NAME} is ready! Speak into your microphone.")
    print("Say 'goodbye' or press Ctrl+C to exit.\n")
    
    while running:
        try:
            user_input = listen_to_audio()
            
            if user_input:
                print(f"You: {user_input}")
                
                # Check for exit commands
                if user_input.lower() in ['goodbye', 'exit', 'quit', 'bye']:
                    print(f"{Config.ASSISTANT_NAME}: Goodbye! 🌸")
                    break
                
                response = chatbot.chat(user_input)
                
                # Text-to-speech
                if Config.TTS_ENABLED and response:
                    TextToSpeech(response)
            
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            print(f"\n{Config.ASSISTANT_NAME}: Goodbye! 🌸")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"❌ An error occurred: {e}")
            print("Continuing...")

def main_text_mode():
    """Run NOVA in text-only mode."""
    global chatbot, running
    
    logger.info("Starting NOVA in text mode")
    chatbot = Chatbot()
    
    print(f"💬 {Config.ASSISTANT_NAME} is ready! Type your messages.")
    print(f"Type /help for commands or /bye to exit.\n")
    
    while running:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Check for exit commands
            if user_input.lower() in ['goodbye', 'exit', 'quit', 'bye']:
                print(f"{Config.ASSISTANT_NAME}: Goodbye! 🌸")
                break
            
            response = chatbot.chat(user_input)
            
            # No TTS in text mode
            
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
            print(f"\n{Config.ASSISTANT_NAME}: Goodbye! 🌸")
            break
        except EOFError:
            # Handle EOF (Ctrl+D)
            print(f"\n{Config.ASSISTANT_NAME}: Goodbye! 🌸")
            break
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            print(f"❌ An error occurred: {e}")
            print("Continuing...")

def main():
    """Main entry point."""
    # Setup signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Setup logging
    setup_logging()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description=f"{Config.ASSISTANT_NAME} - AI Assistant")
    parser.add_argument(
        '--text',
        action='store_true',
        help='Run in text-only mode (no voice input/output)'
    )
    parser.add_argument(
        '--no-tts',
        action='store_true',
        help='Disable text-to-speech (voice mode only)'
    )
    
    args = parser.parse_args()
    
    # Override TTS setting if requested
    if args.no_tts:
        Config.TTS_ENABLED = False
        logger.info("TTS disabled via command line")
    
    # Validate configuration
    is_valid, error_msg = Config.validate()
    if not is_valid:
        logger.error(error_msg)
        print(error_msg)
        sys.exit(1)
    
    try:
        if args.text:
            main_text_mode()
        else:
            main_voice_mode()
    except Exception as e:
        logger.critical(f"Fatal error: {e}", exc_info=True)
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
