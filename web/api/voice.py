"""
Voice API endpoints
Handles voice input/output operations.
"""
from flask import Blueprint, request, jsonify
import logging
import sys
import os
import base64
import io

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from SpeechToText import SpeechRecognition
from TextToSpeech import TextToSpeech
from config import Config

logger = logging.getLogger(__name__)

bp = Blueprint('voice', __name__)

@bp.route('/transcribe', methods=['POST'])
def transcribe_audio():
    """
    Transcribe audio file.
    Expects audio file in request or base64 encoded audio.
    """
    try:
        # Check if audio file is uploaded
        if 'audio' in request.files:
            audio_file = request.files['audio']
            # For now, return a message - actual implementation would process the audio
            # This is a placeholder - browser Web Speech API will handle most of this
            return jsonify({
                'success': True,
                'message': 'Audio received. Use browser Web Speech API for transcription.',
                'note': 'For server-side transcription, implement audio processing here'
            })
        
        # Check for base64 encoded audio
        data = request.get_json()
        if data and 'audio_base64' in data:
            # Decode and process audio
            # Placeholder for actual audio processing
            return jsonify({
                'success': True,
                'message': 'Audio received in base64 format'
            })
        
        return jsonify({'error': 'No audio data provided'}), 400
    
    except Exception as e:
        logger.error(f"Error in transcribe_audio: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@bp.route('/synthesize', methods=['POST'])
def synthesize_speech():
    """
    Synthesize text to speech.
    Returns audio file or base64 encoded audio.
    """
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text'].strip()
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        # Generate speech using TextToSpeech
        # Note: This creates a file, we'll need to return it
        # For web, we might want to use browser TTS instead
        # This endpoint can be used for server-side TTS if needed
        
        return jsonify({
            'success': True,
            'message': 'Use browser Web Speech API for TTS, or implement server-side TTS here',
            'text': text,
            'note': 'For server-side TTS, generate audio and return as base64 or file'
        })
    
    except Exception as e:
        logger.error(f"Error in synthesize_speech: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@bp.route('/languages', methods=['GET'])
def get_languages():
    """Get supported languages for speech recognition."""
    return jsonify({
        'success': True,
        'languages': [
            {'code': 'en-US', 'name': 'English (US)'},
            {'code': 'en-GB', 'name': 'English (UK)'},
            {'code': 'hi-IN', 'name': 'Hindi (India)'},
            {'code': 'es-ES', 'name': 'Spanish (Spain)'},
            {'code': 'fr-FR', 'name': 'French (France)'},
            {'code': 'de-DE', 'name': 'German (Germany)'},
        ],
        'current': Config.INPUT_LANGUAGE
    })

