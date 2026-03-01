<p align="center">
  <img src="https://img.shields.io/badge/NOVA-AI%20Assistant-8b5cf6?style=for-the-badge&logo=atom&logoColor=white" alt="NOVA Badge"/>
</p>

<h1 align="center">✨ NOVA — Your Intelligent AI Companion</h1>

<p align="center">
  <em>A comprehensive, voice-enabled AI assistant with emotional intelligence, persistent memory, and proactive care — built with Python, Flask, and modern LLMs.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-2.x-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/Groq-Llama%203.1-F55036?style=flat-square&logo=meta&logoColor=white" alt="Groq"/>
  <img src="https://img.shields.io/badge/Gemini-Pro-4285F4?style=flat-square&logo=google&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/WebSocket-Real--time-010101?style=flat-square&logo=socket.io&logoColor=white" alt="WebSocket"/>
  <img src="https://img.shields.io/badge/License-Personal-lightgrey?style=flat-square" alt="License"/>
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#️-tech-stack">Tech Stack</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-usage">Usage</a> •
  <a href="#-commands">Commands</a> •
  <a href="#-api-reference">API Reference</a> •
  <a href="#-project-structure">Project Structure</a>
</p>

---

## 🎯 What is NOVA?

**NOVA** (Next-gen Omniscient Virtual Assistant) is a full-stack AI assistant that goes beyond simple chat — it understands emotions, builds relationships, tracks milestones, manages schedules, and proactively cares about your well-being. It features both a beautiful **web interface** and a powerful **CLI** with voice support.

Unlike generic chatbots, NOVA has:
- 🧠 **Persistent memory** — Remembers facts, preferences, and conversations across sessions
- 😊 **Emotional intelligence** — Detects and responds to your emotional state
- 💙 **Relationship evolution** — Tracks trust, intimacy, and milestones over time
- 🧬 **Adaptive personality** — Dynamically adjusts response style based on context
- 🎯 **Proactive care** — Schedules follow-ups and wellness check-ins

---

## ✨ Features

### 🌐 Dual Interface
| Web Interface | CLI Interface |
|:---:|:---:|
| Modern, responsive design | Voice & text modes |
| Real-time WebSocket updates | System-level TTS |
| Animated avatar with states | Full command support |
| Dark/light theme toggle | Minimal dependencies |
| Code syntax highlighting | Portable & fast |

### Core Capabilities
- 💬 **Multi-LLM Conversational AI** — Intelligent routing between Groq (Llama 3.1) and Google Gemini
- 🎤 **Voice I/O** — Speech recognition via Google Speech API + TTS via Edge-TTS (CLI) / Web Speech API (browser)
- 🔍 **Real-Time Web Search** — DuckDuckGo integration for up-to-date information
- 💻 **Code Assistant** — Generate, explain, debug, and review code with optional Cursor API
- 📝 **Chat History** — Persistent conversation logs with export to file
- 📅 **Schedule Management** — Track classes, assignments, and deadlines with auto-reminders
- 🎉 **Milestone Tracking** — Track birthdays, anniversaries, and recurring events

### Intelligence Engine
- 🧠 **Context-Aware Memory** — Tag-based, emotion-categorized memory retrieval with relevance scoring
- 😊 **Emotion Detection** — Keyword + context + pattern analysis for 8+ emotion categories
- 🧬 **Personality Modes** — Emotional support, academic, code review, casual, motivational, and deep conversation
- 💙 **Relationship Stages** — Stranger → Acquaintance → Friend → Close Friend → Best Friend progression
- 🎯 **Proactive Care** — Automated wellness check-ins & mood follow-ups

### Language & Localization
- 🌐 **Multi-Language Speech** — Input in any language, auto-translated to English
- 🗣️ **GenZ Slang Decoder** — Understands modern slang like "no cap", "bussin", "slay"
- 🇮🇳 **Hinglish Support** — Decodes Hindi-English code-mixed text seamlessly
- ✍️ **Text Normalization** — Handles abbreviations, numbers, and informal text

---

## 🛠️ Tech Stack

### Backend
| Technology | Role | Details |
|:---|:---|:---|
| **Python 3.9+** | Core Runtime | Main application language |
| **Flask 2.x** | Web Framework | Serves web interface, REST APIs |
| **Flask-SocketIO** | WebSocket | Real-time bidirectional communication |
| **Flask-CORS** | CORS | Cross-origin resource sharing |
| **Groq SDK** | LLM Provider | Access to Llama 3.1 (70B/8B) |
| **google-generativeai** | LLM Provider | Access to Gemini Pro models |
| **edge-tts** | Text-to-Speech | Neural TTS with 50+ voices |
| **SpeechRecognition** | Speech-to-Text | Google Speech API integration |
| **mtranslate** | Translation | Multi-language to English translation |
| **DuckDuckGo Search** | Web Search | Real-time search with no API key |
| **pygame** | Audio Playback | TTS audio playback engine |
| **python-dotenv** | Config | Environment variable management |
| **Rich** | CLI Formatting | Beautiful terminal output |

### Frontend (Web Interface)
| Technology | Role | Details |
|:---|:---|:---|
| **HTML5** | Structure | Semantic markup with Jinja2 templating |
| **Vanilla CSS** | Styling | Custom design system with CSS variables |
| **Vanilla JavaScript** | Logic | Modular ES6+ with 9 JS modules |
| **Web Speech API** | Browser Voice | Native speech recognition & synthesis |
| **Socket.IO Client** | Real-Time | WebSocket for live message streaming |
| **CSS Animations** | UX | Smooth transitions and micro-animations |

### Data & Storage
| Technology | Role | Details |
|:---|:---|:---|
| **JSON Files** | Persistence | User data, memories, relationships, schedules |
| **File System** | Logging | Structured logging with rotation support |

### Development & Tooling
| Technology | Role |
|:---|:---|
| **Git** | Version control |
| **venv** | Python virtual environment |
| **argparse** | CLI argument parsing |
| **asyncio** | Async TTS generation |

---

## 🏗 Architecture

### High-Level System Design

```
┌──────────────────────────────────────────────────────────────────┐
│                        USER INTERFACES                           │
├──────────────────┬───────────────────┬───────────────────────────┤
│   Web Browser    │   CLI (Voice)     │   CLI (Text)              │
│   localhost:5001 │   python main.py  │   python main.py --text   │
└────────┬─────────┴─────────┬─────────┴────────────┬──────────────┘
         │                   │                      │
         ▼                   ▼                      ▼
┌──────────────────┐  ┌──────────────┐  ┌───────────────────┐
│  Flask + SocketIO│  │ SpeechToText │  │  Direct stdin     │
│  (web/app.py)    │  │   Module     │  │  Input            │
│  10 API Blueprints│  │ (Google ASR) │  │                   │
└────────┬─────────┘  └──────┬───────┘  └─────────┬─────────┘
         │                   │                      │
         └───────────────────┼──────────────────────┘
                             ▼
              ┌──────────────────────────────┐
              │       CHATBOT ENGINE         │
              │       (Chatbot.py)           │
              │  • Command Processing        │
              │  • Memory Management         │
              │  • Context Assembly          │
              │  • Response Orchestration    │
              └──────────────┬───────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ LLM Provider │  │ Intelligence     │  │  Utilities       │
│              │  │ Engine           │  │                  │
│ • Groq       │  │ • EmotionDetect  │  │ • WebSearch      │
│ • Gemini     │  │ • Personality    │  │ • CodeAssistant  │
│ • Cursor     │  │ • Relationship   │  │ • TextNormalizer │
│ (auto-route) │  │ • ProactiveCare  │  │ • GenZSlang      │
│              │  │ • Milestones     │  │ • Hinglish       │
│              │  │ • Schedule       │  │ • ResponseLength │
└──────────────┘  └──────────────────┘  └──────────────────┘
                             │
                             ▼
              ┌──────────────────────────────┐
              │      DATA PERSISTENCE        │
              │      (Data/ directory)       │
              │                              │
              │  • {UserID}_ChatLog.json     │
              │  • {UserID}_Memory.json      │
              │  • {UserID}_Relationship.json│
              │  • {UserID}_Milestones.json  │
              │  • {UserID}_ProactiveCare.json│
              │  • default_Profile.json      │
              └──────────────────────────────┘
```

### LLM Routing Strategy

The `LLMProvider` intelligently routes queries to the optimal model:

| Query Type | Primary Model | Fallback | Reason |
|:---|:---|:---|:---|
| **Research / Factual** | Gemini Pro | Groq Llama 3.1 | Gemini has broader knowledge |
| **Code Generation** | Cursor API | Groq Llama 3.1 | Specialized code models |
| **Casual Conversation** | Groq Llama 3.1 | Gemini Pro | Faster response times |
| **Emotional / Sensitive** | Groq Llama 3.1 | Gemini Pro | Better nuanced responses |

### Web API Architecture

The web interface is built with **10 Flask Blueprint modules**, each handling a specific domain:

| Blueprint | Prefix | Responsibility |
|:---|:---|:---|
| `chat` | `/api/chat` | Send messages, get responses |
| `memory` | `/api/memory` | CRUD operations on memories |
| `voice` | `/api/voice` | Voice synthesis & recognition |
| `profile` | `/api/profile` | User profile management |
| `search` | `/api/search` | Web search queries |
| `emotions` | `/api/emotions` | Emotion history & stats |
| `care` | `/api/care` | Proactive care check-ins |
| `milestones` | `/api/milestones` | Milestone CRUD & reminders |
| `websocket` | — | Real-time event handling |

### Frontend Module Map

| Module | Size | Responsibility |
|:---|:---|:---|
| `main.js` | 5.7 KB | App initialization, routing, themes |
| `chat.js` | 32.3 KB | Chat interface, message rendering, markdown |
| `ui.js` | 23.4 KB | UI components, modals, panels, sidebars |
| `api.js` | 4.1 KB | HTTP & WebSocket API abstraction |
| `voice.js` | 9.8 KB | Web Speech API integration |
| `search.js` | 5.0 KB | Search interface & results |
| `research-canvas.js` | 10.1 KB | Research mode with canvas UI |
| `avatar.js` | 2.4 KB | Animated avatar state machine |
| `profile.js` | 2.8 KB | User profile panel |

---

## 📋 Prerequisites

- **Python** 3.9 or higher
- **pip** (Python package manager)
- **Microphone** (required for CLI voice mode)
- **API Key** — At least **one** of the following:
  - [**Groq API Key**](https://console.groq.com/) — Free tier available
  - [**Google Gemini API Key**](https://makersuite.google.com/app/apikey) — Free tier available
- **Browser** — Chrome, Edge, or Safari recommended for web interface voice features

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sidhant185/NOVA.git
cd NOVA
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate          # Windows
```

### 3. Install Dependencies

```bash
pip install -r Requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```env
# ───── REQUIRED: At least one ─────
GROQ_API_KEY=gsk_xxxxxxxxxxxx
GEMINI_API_KEY=AIzaxxxxxxxxxx

# ───── Optional ─────
CURSOR_API_KEY=your_cursor_key     # Enhanced code features
FLASK_SECRET_KEY=your_secret_key   # Production web server

# ───── User Config ─────
Username=YourName
UserID=YourName                    # Must be "Sidhant" or "default"
AssistantName=Nova

# ───── Speech & Voice ─────
InputLanguage=en-US
AssistantVoice=en-US-AriaNeural
TTSEnabled=true
TTSSpeed=+1%

# ───── Chat & Logging ─────
MaxChatHistory=10
LogLevel=INFO
LogToFile=true
```

### 5. Run NOVA

```bash
# Web Interface (recommended)
python run_web.py

# CLI Voice Mode
python main.py

# CLI Text Mode
python main.py --text
```

---

## 🎮 Usage

### Web Interface 🌐 *(Recommended)*

```bash
python run_web.py
```

Open **http://localhost:5001** in your browser.

**Web Features:**
- ✨ Modern, responsive chat interface
- 🎤 Voice input/output via Web Speech API
- 🎨 Animated avatar with idle, listening, thinking, and speaking states
- 🌓 Dark / light theme toggle
- 💻 Code blocks with syntax highlighting
- 🧠 Memory management panel
- 📊 Emotion & relationship insights sidebar
- 📅 Schedule & milestone views
- 🔍 Research canvas for deep-dive queries
- 🔄 Real-time updates via WebSocket

### CLI Voice Mode 🎤

```bash
python main.py
```

Speak into your microphone. NOVA responds with text-to-speech.

### CLI Text Mode 💬

```bash
python main.py --text
```

Pure text-based conversation — no microphone needed, fastest response times.

### CLI Voice (No TTS) 🔇

```bash
python main.py --no-tts
```

Voice input only, responses appear as text (no audio playback).

---

## 📖 Commands

### Basic
| Command | Description |
|:---|:---|
| `/help` | Show all available commands |
| `/clear` | Clear chat history |
| `/time` | Show current date and time |
| `/whoami` | Show user information |
| `/bye` `/exit` `/quit` | Exit the assistant |

### Memory
| Command | Description | Example |
|:---|:---|:---|
| `/remember <fact>` | Save a memory | `/remember birthday: August 9` |
| `/memories` | List all saved memories | |
| `/forget <key>` | Remove a memory | `/forget birthday` |

### Utility
| Command | Description |
|:---|:---|
| `/search <query>` | Search the web via DuckDuckGo |
| `/summary` | Get conversation summary |
| `/export` | Export chat history to file |

### Code
| Command | Description | Example |
|:---|:---|:---|
| `/code <desc>` | Generate code | `/code binary search in Python` |
| `/explain <code>` | Explain code | `/explain def fib(n): ...` |
| `/debug <code>` | Debug code issues | `/debug [your code]` |
| `/review <code>` | Review for best practices | `/review [your code]` |

### Personalization
| Command | Description |
|:---|:---|
| `/relationship` | Show relationship status & insights |
| `/mood` | Show recent emotional patterns |
| `/emotions` | Show emotion history |
| `/check-in` | Show pending proactive check-ins |
| `/milestones` | List all milestones |
| `/upcoming` | Show upcoming milestones |
| `/add_milestone <type>\|<date>\|<desc>\|[importance]\|[recurring]` | Add a milestone |

### Schedule
| Command | Description |
|:---|:---|
| `/schedule` | Show upcoming classes & assignments |
| `/add_class <name> \| <days> \| <time> \| [location]` | Add a class |
| `/add_assignment <title> \| <due_date> \| [class] \| [desc]` | Add an assignment |

**Examples:**
```
/add_milestone birthday|2024-08-09|My Birthday|high|true
/add_class Computer Science|Mon,Wed,Fri|10:00 AM|Room 101
/add_assignment Final Project|2024-12-15|CS|Build a web app
```

---

## 🔌 API Reference

All REST endpoints are prefixed with `/api`. Real-time events use WebSocket via Socket.IO.

### Chat
| Method | Endpoint | Description |
|:---|:---|:---|
| `POST` | `/api/chat/send` | Send a message and get AI response |
| `GET` | `/api/chat/history` | Retrieve conversation history |
| `DELETE` | `/api/chat/clear` | Clear chat history |

### Memory
| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/api/memory/` | Get all memories |
| `POST` | `/api/memory/add` | Add a new memory |
| `DELETE` | `/api/memory/forget/<key>` | Delete a memory |

### Emotions & Care
| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/api/emotions/history` | Get emotion history |
| `GET` | `/api/emotions/stats` | Get emotion statistics |
| `GET` | `/api/care/check-ins` | Get pending check-ins |

### Profile & Search
| Method | Endpoint | Description |
|:---|:---|:---|
| `GET` | `/api/profile/` | Get user profile |
| `POST` | `/api/search/query` | Perform web search |

### WebSocket Events
| Event | Direction | Description |
|:---|:---|:---|
| `connect` | Client → Server | Establish connection |
| `send_message` | Client → Server | Send chat message |
| `response` | Server → Client | Receive AI response |
| `typing` | Server → Client | Typing indicator |
| `error` | Server → Client | Error notification |

---

## 📁 Project Structure

```
NOVA/
├── main.py                         # CLI entry point (voice & text modes)
├── run_web.py                      # Web server launcher
├── Chatbot.py                      # Core chatbot engine (1100+ lines)
├── SpeechToText.py                 # Speech recognition with translation
├── TextToSpeech.py                 # Edge-TTS synthesis + pygame playback
├── config.py                       # Centralized configuration management
├── compat.py                       # Python 3.9 compatibility patches
│
├── web/                            # ── Web Interface ──
│   ├── app.py                      # Flask app factory + blueprint registration
│   ├── session_manager.py          # Session lifecycle management
│   ├── api/                        # REST API layer (10 blueprints)
│   │   ├── chat.py                 # Chat send/history/clear
│   │   ├── memory.py               # Memory CRUD
│   │   ├── voice.py                # Voice synthesis endpoints
│   │   ├── websocket.py            # Socket.IO event handlers
│   │   ├── profile.py              # User profile management
│   │   ├── search.py               # Web search proxy
│   │   ├── emotions.py             # Emotion history & stats
│   │   ├── care.py                 # Proactive care endpoints
│   │   └── milestones.py           # Milestone CRUD
│   ├── templates/
│   │   └── index.html              # Main SPA template (Jinja2)
│   └── static/
│       ├── css/                    # Design system
│       │   ├── style.css           # Core layout & typography
│       │   ├── theme.css           # CSS variables, dark/light themes
│       │   ├── animations.css      # Keyframe animations
│       │   ├── enhancements.css    # Visual polish & effects
│       │   └── components/         # 9 component stylesheets
│       │       ├── chat.css        # Chat bubble styles
│       │       ├── sidebar.css     # Sidebar panel
│       │       ├── header.css      # Top navigation
│       │       ├── avatar.css      # Animated avatar
│       │       ├── code-panel.css  # Code syntax blocks
│       │       ├── modals.css      # Modal dialogs
│       │       ├── search.css      # Search interface
│       │       ├── research-canvas.css  # Research mode
│       │       └── utilities.css   # Helper classes
│       ├── js/                     # Frontend modules
│       │   ├── main.js             # App init & theme switching
│       │   ├── chat.js             # Chat logic & rendering
│       │   ├── ui.js               # UI components & interactions
│       │   ├── api.js              # HTTP + WebSocket client
│       │   ├── voice.js            # Web Speech API wrapper
│       │   ├── search.js           # Search UI
│       │   ├── research-canvas.js  # Research mode logic
│       │   ├── avatar.js           # Avatar state machine
│       │   └── profile.js          # Profile panel
│       └── images/                 # Static assets
│
├── utils/                          # ── Intelligence Modules ──
│   ├── llm_provider.py             # Multi-LLM router (Groq/Gemini/Cursor)
│   ├── emotion_detector.py         # Keyword + context emotion analysis
│   ├── personality_engine.py       # Adaptive personality mode selection
│   ├── relationship_tracker.py     # Trust/intimacy/stage progression
│   ├── proactive_care.py           # Wellness check-in scheduler
│   ├── milestone_tracker.py        # Event & milestone management
│   ├── schedule_tracker.py         # Class & assignment tracking
│   ├── code_assistant.py           # Code gen/explain/debug/review
│   ├── response_enhancer.py        # Response quality improvement
│   ├── response_length_detector.py # Dynamic response length control
│   ├── text_normalizer.py          # Text cleanup & formatting
│   ├── genz_slang.py               # GenZ slang dictionary & decoder
│   ├── hinglish_decoder.py         # Hindi-English code-mixing decoder
│   └── logger.py                   # Structured logging setup
│
├── Data/                           # ── User Data (gitignored) ──
│   ├── default_Profile.json        # Default user profile template
│   ├── {UserID}_ChatLog.json       # Conversation history
│   ├── {UserID}_Memory.json        # Saved memories
│   ├── {UserID}_Relationship.json  # Relationship progression
│   ├── {UserID}_Milestones.json    # Tracked milestones
│   └── {UserID}_ProactiveCare.json # Care check-in data
│
├── logs/                           # Application logs (gitignored)
├── Requirements.txt                # Python dependencies (23 packages)
├── .env.example                    # Environment template
├── .gitignore                      # Git exclusions
└── README.md                       # You are here
```

---

## ⚙️ Configuration Reference

### Required Settings

> At least **one** API key must be configured.

| Variable | Description | Required |
|:---|:---|:---:|
| `GROQ_API_KEY` | Groq API key for Llama 3.1 | One of these |
| `GEMINI_API_KEY` | Google Gemini API key | One of these |

### Optional Settings

| Variable | Default | Description |
|:---|:---|:---|
| `Username` | `Sidhant` | Display name |
| `UserID` | `Sidhant` | Data file prefix (`Sidhant` or `default`) |
| `AssistantName` | `Nova` | Assistant's name |
| `InputLanguage` | `en-US` | Speech recognition language code |
| `AssistantVoice` | `en-US-AriaNeural` | Edge-TTS voice identifier |
| `TTSEnabled` | `true` | Enable/disable text-to-speech |
| `TTSSpeed` | `+1%` | TTS playback speed adjustment |
| `MaxChatHistory` | `10` | Messages kept in LLM context |
| `LogLevel` | `INFO` | Logging verbosity |
| `LogToFile` | `true` | Write logs to `logs/nova.log` |
| `CURSOR_API_KEY` | — | Optional Cursor API for code features |
| `FLASK_SECRET_KEY` | auto-generated | Flask session secret (set for production) |

### Available TTS Voices

```bash
edge-tts --list-voices    # List all 300+ voices
```

**Popular choices:**
| Voice | Gender | Accent |
|:---|:---|:---|
| `en-US-AriaNeural` | Female | American (default) |
| `en-US-JennyNeural` | Female | American |
| `en-US-GuyNeural` | Male | American |
| `en-GB-SoniaNeural` | Female | British |
| `en-AU-NatashaNeural` | Female | Australian |
| `en-IN-NeerjaNeural` | Female | Indian |

---

## 🔧 Troubleshooting

<details>
<summary><strong>🌐 Web Interface Issues</strong></summary>

| Problem | Solution |
|:---|:---|
| **"Connection refused"** | Ensure `run_web.py` is running; check port 5001 is free |
| **"Module not found"** | Activate venv: `source venv/bin/activate` → `pip install -r Requirements.txt` |
| **WebSocket fails** | Check browser console (F12); ensure firewall allows connections |
| **Voice not working** | Grant microphone permissions; use Chrome/Edge/Safari |
| **Avatar not animating** | Clear browser cache; check console for JS errors |

</details>

<details>
<summary><strong>🎤 Speech Recognition Issues</strong></summary>

| Problem | Solution |
|:---|:---|
| **"No speech detected"** | Check microphone permissions; test mic in other apps |
| **"Could not understand"** | Reduce background noise; speak clearly |
| **Wrong language** | Set `InputLanguage` in `.env` (e.g., `en-US`, `hi-IN`) |
| **Browser compatibility** | Use Chrome/Edge/Safari for best Web Speech API support |

</details>

<details>
<summary><strong>🔊 TTS Issues</strong></summary>

| Problem | Solution |
|:---|:---|
| **No audio output** | Check system volume; verify audio output device |
| **Wrong voice** | Verify `AssistantVoice` is valid: `edge-tts --list-voices` |
| **Audio lag** | Set `TTSSpeed=+0%` or `TTSEnabled=false` for faster responses |

</details>

<details>
<summary><strong>🔑 API Issues</strong></summary>

| Problem | Solution |
|:---|:---|
| **"Missing API keys"** | Check `.env` exists with at least one key; restart app |
| **Rate limiting** | Wait and retry; consider upgrading API tier |
| **API errors** | Verify key is valid; check `logs/nova.log` for details |

</details>

<details>
<summary><strong>⚠️ General Issues</strong></summary>

| Problem | Solution |
|:---|:---|
| **Import errors** | Activate venv; reinstall deps; check Python ≥ 3.9 |
| **File not found** | Ensure `Data/` dir exists; check `UserID` matches filenames |
| **Permission errors** | `chmod -R 755 Data logs` |
| **Port in use** | `lsof -i :5001` → kill process, or change port in `run_web.py` |

</details>

---

## 🧪 Development

### Testing Individual Components

```bash
# Test speech recognition
python SpeechToText.py

# Test text-to-speech
python TextToSpeech.py

# Test chatbot (standalone text mode)
python Chatbot.py
```

### Viewing Logs

```bash
# Stream logs in real-time
tail -f logs/nova.log

# Search for errors
grep "ERROR" logs/nova.log

# Debug-level logging
# Set LogLevel=DEBUG in .env
```

### Memory System

Memories are stored in `Data/{UserID}_Memory.json` as structured entries:

```json
{
  "birthday": {
    "value": "August 9, 2006",
    "category": "personal",
    "emotion": "happy",
    "tags": ["birthday", "personal"],
    "importance": 8,
    "timestamp": "2024-01-15T10:30:00"
  }
}
```

Memories are automatically loaded into LLM context for personalized responses, with relevance scoring based on keyword matching, tags, and importance.

---

## 📦 Dependencies

All 23 Python packages in `Requirements.txt`:

| Package | Purpose |
|:---|:---|
| `python-dotenv` | Environment variable loading |
| `groq` | Groq LLM API client |
| `google-generativeai` | Google Gemini API client |
| `flask` | Web framework |
| `flask-socketio` | WebSocket support |
| `flask-cors` | CORS middleware |
| `edge-tts` | Neural text-to-speech |
| `pygame` | Audio playback |
| `duckduckgo-search` | Web search |
| `requests` | HTTP client |
| `bs4` | HTML parsing |
| `pillow` | Image processing |
| `rich` | Terminal formatting |
| `keyboard` | Keyboard input handling |
| `mtranslate` | Translation |
| `Appopener` | System app launching |
| `pywhatkit` | WhatsApp & web utilities |
| `cohere` | NLP utilities |
| `googlesearch-python` | Google search fallback |
| `selenium` | Browser automation |
| `webdriver-manager` | Selenium driver management |
| `PyQt5` | GUI framework (legacy) |
| `importlib_metadata` | Python 3.9 compatibility |

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- 🐛 Submit issues for bugs or feature requests
- 🔧 Create pull requests for improvements
- 💡 Share feedback and suggestions

---

## 📄 License

This project is for personal use.

---

## 🙏 Acknowledgments

| Provider | Contribution |
|:---|:---|
| **[Groq](https://groq.com/)** | Ultra-fast LLM inference (Llama 3.1) |
| **[Google](https://ai.google.dev/)** | Gemini Pro LLM API |
| **[Edge-TTS](https://github.com/rany2/edge-tts)** | Microsoft Neural TTS voices |
| **[DuckDuckGo](https://duckduckgo.com/)** | Privacy-focused web search |
| **[Flask](https://flask.palletsprojects.com/)** | Lightweight Python web framework |
| **[Socket.IO](https://socket.io/)** | Real-time bidirectional communication |

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/Sidhant185">Sidhant Pande</a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/Sidhant185/NOVA?style=social" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/Sidhant185/NOVA?style=social" alt="Forks"/>
</p>
