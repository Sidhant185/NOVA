"""
Text-to-Speech module for NOVA Assistant.
Uses edge-tts for synthesis and pygame for playback.
"""
import pygame
import random
import asyncio
import edge_tts
import os
import logging
from config import Config

logger = logging.getLogger(__name__)

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text: str) -> str:
    """Convert text to audio file asynchronously."""
    file_path = "Data/speech.mp3"
    
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            logger.warning(f"Could not remove existing audio file: {e}")
    
    try:
        communicate = edge_tts.Communicate(text, voice=Config.ASSISTANT_VOICE, rate=Config.TTS_SPEED)
        await communicate.save(file_path)
        return file_path
    except Exception as e:
        logger.error(f"Error generating audio: {e}")
        raise

# Function to manage Text-to-Speech (TTS) functionality
def TTS(text: str, func=lambda r=None: True) -> bool:
    """
    Play text as speech.
    
    Args:
        text: Text to convert to speech
        func: Optional callback function that can return False to stop playback
    
    Returns:
        True if successful, False otherwise
    """
    if not Config.TTS_ENABLED:
        logger.debug("TTS is disabled")
        return False
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Convert text to audio file asynchronously
            file_path = asyncio.run(TextToAudioFile(text))
            
            # Initialize pygame mixer for audio playback
            pygame.mixer.init()
            
            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            # Wait until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:
                    pygame.mixer.music.stop()
                    break
                pygame.time.Clock().tick(10)
            
            return True
        
        except Exception as e:
            logger.error(f"Error in TTS (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                continue
            return False
        
        finally:
            try:
                # Ensure proper cleanup of pygame mixer
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
            except Exception as e:
                logger.warning(f"Error cleaning up pygame: {e}")

# List of predefined responses for cases where the text is too long
LONG_TEXT_RESPONSES = [
    "The rest of the result has been printed to the chat screen, kindly check it out.",
    "The rest of the text is now on the chat screen, please check it.",
    "You can see the rest of the text on the chat screen.",
    "The remaining part of the text is now on the chat screen.",
    "You'll find more text on the chat screen for you to see.",
    "The rest of the answer is now on the chat screen.",
    "Please look at the chat screen, the rest of the answer is there.",
    "You'll find the complete answer on the chat screen.",
    "The next part of the text is on the chat screen.",
    "Please check the chat screen for more information.",
    "There's more text on the chat screen for you.",
    "Take a look at the chat screen for additional text.",
    "You'll find more to read on the chat screen.",
    "Check the chat screen for the rest of the text.",
    "The chat screen has the rest of the text.",
    "There's more to see on the chat screen, please look.",
    "The chat screen holds the continuation of the text.",
    "You'll find the complete answer on the chat screen, kindly check it out.",
    "Please review the chat screen for the rest of the text.",
    "Look at the chat screen for the complete answer."
]

# Function to manage text to speech with additional responses for long text
def TextToSpeech(text: str, func=lambda r=None: True) -> bool:
    """
    Convert text to speech, handling long texts appropriately.
    
    Args:
        text: Text to convert to speech
        func: Optional callback function
    
    Returns:
        True if successful, False otherwise
    """
    if not text or not text.strip():
        logger.warning("Empty text provided to TextToSpeech")
        return False
    
    # Split text by sentences (periods, exclamation, question marks)
    sentences = [s.strip() for s in text.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    
    # Improved long text detection: more than 5 sentences OR more than 500 characters
    # (Changed from 100 sentences AND 50000 chars - was too strict)
    if len(sentences) > 5 or len(text) > 500:
        # For long text, speak first 2 sentences + a message
        first_part = ". ".join(sentences[:2])
        if first_part and not first_part.endswith('.'):
            first_part += "."
        message = random.choice(LONG_TEXT_RESPONSES)
        short_text = f"{first_part} {message}"
        logger.info(f"Long text detected ({len(sentences)} sentences, {len(text)} chars), truncating TTS")
        return TTS(short_text, func)
    else:
        # Normal text, play the whole thing
        return TTS(text, func)

# Main Execution Loop
if __name__ == "__main__":
    from utils.logger import setup_logging
    setup_logging()
    
    print("Text-to-Speech Test Mode")
    print("Enter text to convert to speech (or 'quit' to exit):\n")
    while True:
        text = input("Enter text: ")
        if text.lower() in ['quit', 'exit', 'q']:
            break
        TextToSpeech(text)
