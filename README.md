# NOVA Assistant

A comprehensive, voice-enabled AI assistant powered by Groq's Llama 3.1 or Google's Gemini, featuring advanced conversational capabilities, persistent memory, emotion detection, and proactive care.

## ✨ Features

### Core Capabilities
- 🌐 **Modern Web Interface**: Beautiful, responsive web-based interface with real-time updates via WebSocket
- 🎤 **Voice Input/Output**: Natural speech recognition and text-to-speech (browser-based in web mode, system-based in CLI)
- 🧠 **Persistent Memory**: Remembers important facts, preferences, and conversation context
- 💬 **Advanced Conversational AI**: Powered by Groq's Llama 3.1 or Google's Gemini models
- 📝 **Chat History**: Persistent conversation history with export functionality

### Advanced Features
- 🔍 **Web Search**: Real-time web search via DuckDuckGo integration
- 💻 **Code Assistant**: Generate, explain, debug, and review code with Cursor API support
- 😊 **Emotion Detection**: Analyzes emotional patterns in conversations
- 💙 **Relationship Tracking**: Tracks and evolves relationship dynamics over time
- 🎯 **Proactive Care**: Automated check-ins and wellness reminders
- 🎉 **Milestone Tracking**: Track important dates, events, and recurring milestones
- 📅 **Schedule Management**: Manage classes, assignments, and deadlines
- 🎨 **Animated Avatar**: Visual feedback with animated avatar states
- 🧬 **Personality Engine**: Dynamic personality adaptation based on interactions
- 🌐 **Multi-language Support**: Hinglish decoder and text normalization
- 🗣️ **GenZ Slang Support**: Understands modern slang and casual language
- 🌓 **Themes**: Dark and light theme support
- ⚙️ **Highly Configurable**: Extensive configuration options via `.env` file

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **Microphone**: Required for voice mode (CLI)
- **API Key**: At least one of the following:
  - Groq API key ([Get one here](https://console.groq.com/))
  - Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- **Browser**: Modern browser (Chrome, Edge, or Safari) for web interface voice features

## 🚀 Installation

### Step 1: Clone or Navigate to Project
```bash
cd NOVA
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r Requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root (or copy from `.env.example` if available):

```bash
# Create .env file
touch .env
```

Add your configuration to `.env`:

```env
# Required: At least one API key must be provided
GROQ_API_KEY=your_groq_api_key_here
# OR
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Code Assistant (for enhanced code features)
CURSOR_API_KEY=your_cursor_api_key_here

# User Configuration
Username=Sidhant
UserID=Sidhant
AssistantName=Nova

# Speech Recognition
InputLanguage=en-US

# Text-to-Speech
AssistantVoice=en-US-AriaNeural
TTSEnabled=true
TTSSpeed=+1%

# Chat Settings
MaxChatHistory=10

# Logging
LogLevel=INFO
LogToFile=true
```

## ⚙️ Configuration

### Required Settings

At least **one** of the following API keys must be configured:
- `GROQ_API_KEY`: Your Groq API key
- `GEMINI_API_KEY`: Your Google Gemini API key

### Optional Settings

#### User Configuration
- `Username`: Your name (default: "Sidhant")
- `UserID`: User identifier - must be "Sidhant" or "default" (default: "Sidhant")
- `AssistantName`: Assistant name (default: "Nova")

#### Speech & Voice
- `InputLanguage`: Speech recognition language (default: "en-US")
- `AssistantVoice`: TTS voice identifier (default: "en-US-AriaNeural")
- `TTSEnabled`: Enable/disable text-to-speech (default: "true")
- `TTSSpeed`: TTS speed adjustment (default: "+1%")

#### Chat Settings
- `MaxChatHistory`: Number of recent messages in context (default: 10)

#### Logging
- `LogLevel`: Logging level - DEBUG, INFO, WARNING, ERROR, CRITICAL (default: "INFO")
- `LogToFile`: Enable file logging (default: "true")

#### Advanced Features
- `CURSOR_API_KEY`: Cursor API key for enhanced code assistance (optional)

### Available TTS Voices

You can change `AssistantVoice` to any edge-tts voice. Common options:
- `en-US-AriaNeural` (default, female)
- `en-US-JennyNeural` (female)
- `en-US-GuyNeural` (male)
- `en-GB-SoniaNeural` (British female)
- `en-AU-NatashaNeural` (Australian female)

To see all available voices:
```bash
edge-tts --list-voices
```

## 🎮 Usage

### Web Interface (Recommended) 🌐

The web interface provides the best user experience with a modern UI, real-time updates, and browser-based voice features.

**Start the web server:**
```bash
python run_web.py
```

**Access the interface:**
Open your browser and navigate to:
```
http://localhost:5001
```

**Web Interface Features:**
- ✨ Modern, responsive design
- 💬 Real-time chat with message history
- 🎤 Voice input/output (browser-based Web Speech API)
- 🎨 Animated avatar with different states
- 🧠 Memory management panel
- 🌓 Dark/light theme toggle
- 💻 Code syntax highlighting
- 🔄 WebSocket for real-time updates
- 📊 Emotion and relationship insights
- 📅 Schedule and milestone views

### CLI Voice Mode 🎤

Run NOVA with voice input/output in terminal:
```bash
python main.py
```

**Features:**
- Voice input via microphone
- Text-to-speech output
- Full command support
- Persistent memory

### CLI Text-Only Mode 💬

Run NOVA without voice (text input only):
```bash
python main.py --text
```

**Features:**
- Text-based conversation
- All commands available
- No microphone required
- Faster response times

### CLI Voice Mode (No TTS) 🔇

Run in voice mode but disable text-to-speech:
```bash
python main.py --no-tts
```

**Use cases:**
- Voice input with text-only output
- Faster responses without TTS delay
- Quiet environments

### Standalone Chatbot 🤖

Run the chatbot directly (text-only, no voice):
```bash
python Chatbot.py
```

## 📖 Commands

NOVA supports a comprehensive set of commands organized by category:

### Basic Commands

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/clear` | Clear chat history |
| `/time` | Show current date and time |
| `/whoami` | Show user information |
| `/bye`, `/exit`, `/quit` | Exit the assistant |

### Memory Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/remember <fact>` | Save a memory | `/remember birthday: August 9, 2006` |
| `/memories` | List all saved memories | `/memories` |
| `/forget <key>` | Remove a memory by key | `/forget birthday` |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/search <query>` | Search the web |
| `/summary` | Get conversation summary |
| `/export` | Export chat history to file |

### Code Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/code <description>` | Generate code | `/code create a function to sort a list` |
| `/explain <code>` | Explain what code does | `/explain def sort_list(lst): return sorted(lst)` |
| `/debug <code>` | Help debug code issues | `/debug [your code here]` |
| `/review <code>` | Review code for best practices | `/review [your code here]` |

### Personalization Commands

| Command | Description |
|---------|-------------|
| `/relationship` | Show relationship status and insights |
| `/mood` | Show recent emotional patterns |
| `/emotions` | Show emotion history |
| `/check-in` | Show pending proactive check-ins |
| `/milestones` | List all milestones |
| `/upcoming` | Show upcoming milestones |
| `/add_milestone <type>\|<date>\|<description>\|[importance]\|[recurring]` | Add a milestone |

**Milestone Example:**
```
/add_milestone birthday|2024-08-09|My Birthday|high|true
```

### Schedule Commands

| Command | Description |
|---------|-------------|
| `/schedule` | Show upcoming classes and assignments |
| `/add_class <name> \| <days> \| <time> \| [location]` | Add a class |
| `/add_assignment <title> \| <due_date> \| [class_name] \| [description]` | Add an assignment |

**Class Example:**
```
/add_class Computer Science|Mon,Wed,Fri|10:00 AM|Room 101
```

**Assignment Example:**
```
/add_assignment Final Project|2024-12-15|Computer Science|Build a web app
```

## 📁 Project Structure

```
NOVA/
├── main.py                    # CLI entry point
├── run_web.py                 # Web interface entry point
├── Chatbot.py                 # Core chatbot logic
├── SpeechToText.py            # Speech recognition
├── TextToSpeech.py            # Text-to-speech
├── config.py                  # Configuration management
│
├── web/                       # Web interface
│   ├── app.py                 # Flask application
│   ├── session_manager.py     # Session management
│   ├── api/                   # API endpoints
│   │   ├── chat.py            # Chat API
│   │   ├── memory.py          # Memory API
│   │   ├── voice.py           # Voice API
│   │   ├── websocket.py       # WebSocket handlers
│   │   ├── profile.py         # User profile API
│   │   ├── search.py          # Web search API
│   │   ├── emotions.py        # Emotion tracking API
│   │   ├── care.py            # Proactive care API
│   │   └── milestones.py      # Milestone tracking API
│   ├── templates/
│   │   └── index.html         # Main HTML template
│   └── static/
│       ├── css/               # Stylesheets
│       │   ├── style.css
│       │   ├── theme.css
│       │   └── components/    # Component styles
│       ├── js/                # JavaScript files
│       │   ├── main.js
│       │   ├── chat.js
│       │   ├── api.js
│       │   └── ...
│       └── images/            # Images and assets
│
├── utils/                     # Utility modules
│   ├── logger.py              # Logging setup
│   ├── llm_provider.py        # LLM provider abstraction (Groq/Gemini)
│   ├── code_assistant.py      # Code generation and assistance
│   ├── emotion_detector.py    # Emotion detection
│   ├── relationship_tracker.py # Relationship tracking
│   ├── personality_engine.py  # Personality adaptation
│   ├── proactive_care.py      # Proactive care system
│   ├── milestone_tracker.py   # Milestone management
│   ├── schedule_tracker.py    # Schedule management
│   ├── text_normalizer.py    # Text normalization
│   ├── response_enhancer.py   # Response enhancement
│   ├── response_length_detector.py # Response length detection
│   ├── genz_slang.py         # GenZ slang support
│   ├── hinglish_decoder.py   # Hinglish language support
│   └── __init__.py
│
├── Data/                      # User data storage
│   ├── default_Profile.json  # Default user profile
│   ├── Sidhant_ChatLog.json  # Chat history
│   ├── Sidhant_Memory.json   # User memories
│   ├── Sidhant_Milestones.json # Milestones
│   ├── Sidhant_ProactiveCare.json # Proactive care data
│   ├── Sidhant_Relationship.json # Relationship data
│   └── ...
│
├── logs/                      # Application logs
│   └── nova.log              # Main log file
│
├── Requirements.txt           # Python dependencies
├── .env                       # Environment configuration (create this)
└── README.md                  # This file
```

## 🔧 Troubleshooting

### Web Interface Issues

**"Connection refused"**
- Ensure `run_web.py` is running
- Check if port 5001 is available
- Try a different port by modifying `run_web.py`

**"Module not found"**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r Requirements.txt`
- Ensure Flask dependencies are installed: `pip install flask flask-socketio flask-cors`

**WebSocket connection fails**
- Check browser console for errors (F12)
- Ensure firewall allows connections
- Try refreshing the page
- Check that SocketIO is properly initialized

**Voice not working in browser**
- Grant microphone permissions in browser settings
- Use Chrome, Edge, or Safari (best Web Speech API support)
- Check browser console for permission errors
- Ensure HTTPS or localhost (required for microphone access)

**Avatar not animating**
- Check browser console for JavaScript errors
- Ensure all static files are loading correctly
- Clear browser cache and refresh

### Speech Recognition Issues

**"No speech detected"**
- Check microphone permissions (system and browser)
- Ensure microphone is working (test in other apps)
- Adjust microphone volume in system settings
- Speak clearly and wait for the listening indicator

**"Could not understand audio"**
- Speak more clearly and slowly
- Reduce background noise
- Adjust microphone volume
- Check microphone quality

**Language issues**
- Set `InputLanguage` in `.env` to match your language
- Supported languages: `en-US`, `en-GB`, `es-ES`, `fr-FR`, etc.
- Restart the application after changing language settings

**Browser compatibility**
- Web Speech API works best in Chrome, Edge, or Safari
- Firefox has limited support
- Ensure you're using a recent browser version

### TTS (Text-to-Speech) Issues

**No audio output**
- Check system volume and audio settings
- Test audio in other applications
- Verify audio output device is selected
- Check browser audio permissions (web mode)

**Wrong voice**
- Verify `AssistantVoice` in `.env` is a valid edge-tts voice
- List available voices: `edge-tts --list-voices`
- Restart application after changing voice

**Audio lag**
- Reduce `TTSSpeed` in `.env` (e.g., `+0%` or `-10%`)
- Disable TTS for faster responses: `TTSEnabled=false`
- Check system performance and close other applications

**Browser TTS not working**
- Use Chrome/Edge for best Web Speech API support
- Check browser console for errors
- Ensure browser audio is not muted

### API Issues

**"Missing API keys"**
- Ensure `.env` file exists in project root
- Add at least one API key: `GROQ_API_KEY` or `GEMINI_API_KEY`
- Check for typos in variable names
- Restart application after adding keys

**Rate limiting**
- Groq and Gemini have rate limits
- Wait a moment and try again
- Consider upgrading API tier if needed
- Check API usage dashboard

**API errors**
- Verify API key is valid and active
- Check API service status
- Review error messages in logs (`logs/nova.log`)
- Ensure internet connection is stable

### General Issues

**Import errors**
- Activate virtual environment: `source venv/bin/activate`
- Reinstall dependencies: `pip install -r Requirements.txt`
- Check Python version: `python3 --version` (requires 3.9+)

**File not found errors**
- Ensure `Data/` directory exists
- Check file permissions for `Data/` and `logs/` directories
- Verify `UserID` in `.env` matches data file names

**Permission errors**
- Check file permissions for `Data/` and `logs/` directories
- Ensure write permissions: `chmod -R 755 Data logs`
- On Windows, run as administrator if needed

**Port already in use**
- Change port in `run_web.py` or `web/app.py` (default is 5001)
- Find process using port: `lsof -i :5001` (macOS/Linux) or `netstat -ano | findstr :5001` (Windows)
- Kill process or use different port

**Configuration validation errors**
- Ensure `UserID` is either "Sidhant" or "default"
- Check `.env` file format (no spaces around `=`)
- Verify all required settings are present

## 🧪 Development

### Testing Individual Components

Test speech recognition:
```bash
python SpeechToText.py
```

Test text-to-speech:
```bash
python TextToSpeech.py
```

Test chatbot:
```bash
python Chatbot.py
```

### Logging

Logs are written to `logs/nova.log` by default (if `LogToFile=true`).

**Log Levels:**
- `DEBUG`: Detailed information for debugging
- `INFO`: General information about operations
- `WARNING`: Warning messages for potential issues
- `ERROR`: Error messages for failures
- `CRITICAL`: Critical errors requiring immediate attention

**View logs:**
```bash
# View recent logs
tail -f logs/nova.log

# Search logs
grep "ERROR" logs/nova.log
```

### Memory System

Memories are stored in `Data/{UserID}_Memory.json`. The chatbot automatically loads memories into context for personalized responses.

**Memory Format:**
- Key-value pairs stored as JSON
- Automatically loaded on startup
- Persisted after each `/remember` command
- Used to enhance conversation context

### Data Files

All user data is stored in the `Data/` directory:
- `{UserID}_ChatLog.json`: Conversation history
- `{UserID}_Memory.json`: Saved memories
- `{UserID}_Milestones.json`: Tracked milestones
- `{UserID}_ProactiveCare.json`: Proactive care data
- `{UserID}_Relationship.json`: Relationship tracking data

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Submit issues for bugs or feature requests
- Create pull requests for improvements
- Share feedback and suggestions

## 📄 License

This project is for personal use.

## 🙏 Credits

- **Groq**: LLM API provider (Llama 3.1)
- **Google**: Gemini API provider
- **edge-tts**: Text-to-speech synthesis
- **speech_recognition**: Speech recognition library
- **DuckDuckGo**: Web search integration
- **Flask**: Web framework
- **SocketIO**: Real-time WebSocket communication

---

Made with ❤️ by Sidhant Pande
