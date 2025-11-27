/**
 * Voice Input/Output Handler
 * Manages browser-based speech recognition and synthesis
 */

class VoiceController {
    constructor() {
        this.recognition = null;
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.isSpeaking = false;
        this.voiceButton = document.getElementById('voiceButton');
        this.voiceStatus = document.getElementById('voiceStatus');
        this.voiceStatusText = document.getElementById('voiceStatusText');
        
        if (this.voiceButton) {
            this.initSpeechRecognition();
            this.setupEventListeners();
        }
    }

    initSpeechRecognition() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported in this browser');
            this.voiceButton.classList.add('hidden');
            return;
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US'; // Default, can be changed from config
        
        this.recognition.onstart = () => {
            this.isListening = true;
            this.voiceButton.classList.add('recording');
            this.voiceButton.title = 'Click to stop recording';
            this.voiceStatus.classList.add('visible', 'flex', 'active');
            this.voiceStatusText.textContent = 'Listening...';
            avatar.listening();
        };

        this.recognition.onresult = (event) => {
            let transcript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            
            // Update status with interim results
            if (!event.results[event.resultIndex].isFinal) {
                this.voiceStatusText.textContent = `Listening: ${transcript}`;
            } else {
                this.voiceStatusText.textContent = `Heard: ${transcript}`;
            }
            
            // Dispatch event with transcript
            if (event.results[event.resultIndex].isFinal) {
                const event = new CustomEvent('voiceTranscript', { detail: transcript });
                document.dispatchEvent(event);
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.stopListening();
            
            let errorMsg = 'Error occurred';
            if (event.error === 'no-speech') {
                errorMsg = 'No speech detected';
            } else if (event.error === 'audio-capture') {
                errorMsg = 'Microphone not found';
            } else if (event.error === 'not-allowed') {
                errorMsg = 'Microphone permission denied';
            }
            
            this.voiceStatusText.textContent = errorMsg;
            avatar.error();
            
            setTimeout(() => {
                this.voiceStatus.classList.remove('visible', 'flex', 'active');
            }, 3000);
        };

        this.recognition.onend = () => {
            this.stopListening();
        };
    }

    setupEventListeners() {
        this.voiceButton.addEventListener('click', () => {
            if (this.isListening) {
                this.stopListening();
            } else {
                this.startListening();
            }
        });

        // Listen for transcript events
        document.addEventListener('voiceTranscript', (e) => {
            const transcript = e.detail;
            const messageInput = document.getElementById('messageInput');
            if (messageInput) {
                messageInput.value = transcript;
                messageInput.dispatchEvent(new Event('input'));
                
                // Auto-focus input after voice input
                messageInput.focus();
                
                // Auto-send voice input to chat (default enabled)
                const autoSend = localStorage.getItem('voice_auto_send') !== 'false'; // Default to true
                if (autoSend && transcript.trim()) {
                    setTimeout(() => {
                        const sendButton = document.getElementById('sendButton');
                        if (sendButton) {
                            sendButton.click();
                        }
                    }, 300);
                }
            }
        });
        
        // Keyboard shortcut: Space to start/stop (when input is not focused)
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && document.activeElement !== document.getElementById('messageInput')) {
                e.preventDefault();
                if (this.isListening) {
                    this.stopListening();
                } else {
                    this.startListening();
                }
            }
        });
    }

    startListening() {
        if (!this.recognition) {
            alert('Speech recognition is not supported in your browser');
            return;
        }

        try {
            this.recognition.start();
        } catch (error) {
            console.error('Error starting recognition:', error);
            this.voiceStatusText.textContent = 'Error starting voice input';
        }
    }

    stopListening() {
        if (this.recognition && this.isListening) {
            this.recognition.stop();
        }
        
        this.isListening = false;
        this.voiceButton.classList.remove('recording');
        this.voiceButton.title = 'Voice Input (Click to start/stop)';
        avatar.idle();
    }

    speak(text) {
        if (!this.synthesis) {
            console.warn('Speech synthesis not supported');
            return;
        }

        // Cancel any ongoing speech
        this.synthesis.cancel();

        // Remove emojis from text before speaking - comprehensive pattern
        // This pattern covers all emoji ranges including variations and modifiers
        // Using multiple patterns to catch all emoji types
        let textWithoutEmojis = text;
        
        // Remove emojis using Unicode ranges
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{1F300}-\u{1F9FF}]/gu, ''); // Miscellaneous Symbols and Pictographs
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{1F600}-\u{1F64F}]/gu, ''); // Emoticons
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{1F680}-\u{1F6FF}]/gu, ''); // Transport and Map Symbols
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{1F1E0}-\u{1F1FF}]/gu, ''); // Regional Indicator Symbols (flags)
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{2600}-\u{26FF}]/gu, ''); // Miscellaneous Symbols
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{2700}-\u{27BF}]/gu, ''); // Dingbats
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{1F900}-\u{1F9FF}]/gu, ''); // Supplemental Symbols and Pictographs
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{1FA00}-\u{1FA6F}]/gu, ''); // Chess Symbols
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{1FA70}-\u{1FAFF}]/gu, ''); // Symbols and Pictographs Extended-A
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{FE00}-\u{FE0F}]/gu, ''); // Variation Selectors
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{200D}]/gu, ''); // Zero Width Joiner
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{20E3}]/gu, ''); // Combining Enclosing Keycap
        textWithoutEmojis = textWithoutEmojis.replace(/[\u{FE0F}]/gu, ''); // Variation Selector-16
        
        // Clean up multiple spaces and trim
        textWithoutEmojis = textWithoutEmojis.replace(/\s+/g, ' ').trim();
        
        // Skip if text is empty after removing emojis
        if (!textWithoutEmojis) {
            return;
        }

        const utterance = new SpeechSynthesisUtterance(textWithoutEmojis);
        
        // Get available voices and select a good one
        const voices = this.synthesis.getVoices();
        const preferredVoice = voices.find(voice => 
            voice.name.includes('Neural') || 
            voice.name.includes('Aria') ||
            voice.lang.startsWith('en')
        );
        
        if (preferredVoice) {
            utterance.voice = preferredVoice;
        }
        
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        utterance.onstart = () => {
            this.isSpeaking = true;
            avatar.speaking();
        };

        utterance.onend = () => {
            this.isSpeaking = false;
            avatar.idle();
        };

        utterance.onerror = (event) => {
            console.error('Speech synthesis error:', event);
            this.isSpeaking = false;
            avatar.error();
        };

        this.synthesis.speak(utterance);
    }

    stopSpeaking() {
        if (this.synthesis) {
            this.synthesis.cancel();
            this.isSpeaking = false;
            avatar.idle();
        }
    }

    setLanguage(lang) {
        if (this.recognition) {
            this.recognition.lang = lang;
        }
    }
}

// Export singleton instance
// Initialize voice controller after DOM is ready
let voice;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        voice = new VoiceController();
        window.voice = voice; // Make available globally
    });
} else {
    voice = new VoiceController();
    window.voice = voice; // Make available globally
}

