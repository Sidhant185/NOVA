/**
 * Main Entry Point for NOVA Web Interface
 * Initializes all components and sets up WebSocket connection
 */

// Global state
window.appConfig = {
    tts_enabled: true,
    theme: 'dark'
};

// Initialize Socket.IO connection
let socket;

document.addEventListener('DOMContentLoaded', async () => {
    console.log('NOVA Web Interface Initializing...');
    
    // Wait for all components to be initialized
    const waitForComponents = () => {
        return new Promise((resolve) => {
            const checkComponents = () => {
                if (window.chat && window.ui && window.avatar && window.voice && window.api) {
                    resolve();
                } else {
                    setTimeout(checkComponents, 50);
                }
            };
            checkComponents();
        });
    };
    
    await waitForComponents();
    console.log('All components initialized');
    
    // Load configuration
    try {
        const config = await api.getConfig();
        window.appConfig = { ...window.appConfig, ...config };
        
        // Set TTS enabled state
        if (localStorage.getItem('tts_enabled') !== null) {
            window.appConfig.tts_enabled = localStorage.getItem('tts_enabled') === 'true';
        }
        
        // Load theme
        const savedTheme = localStorage.getItem('theme') || 'dark';
        document.body.className = `theme-${savedTheme}`;
        
    } catch (error) {
        console.error('Error loading config:', error);
    }
    
    // Initialize Socket.IO
    socket = io();
    
    socket.on('connect', () => {
        console.log('Connected to server');
        updateStatus('online');
        if (avatar) avatar.success();
        
        socket.emit('get_history', { session_id: api.sessionId });
    });
    
    socket.on('disconnect', () => {
        console.log('Disconnected from server');
        updateStatus('offline');
        if (avatar) avatar.error();
    });
    
    socket.on('connected', (data) => {
        console.log('Server connection confirmed:', data);
    });
    
    socket.on('chat_response', (data) => {
        if (chat) {
            chat.hideTyping();
            chat.addMessage('assistant', data.response);
        }
        if (avatar) avatar.idle();
        
        if (window.appConfig.tts_enabled && voice) {
            voice.speak(data.response);
        }
    });
    
    socket.on('stream_token', (data) => {
        // Handle streaming tokens
        // For now, we'll use regular API, but this is ready for streaming
    });
    
    socket.on('typing', (data) => {
        if (data.status) {
            if (chat) chat.showTyping();
            if (avatar) avatar.thinking();
        } else {
            if (chat) chat.hideTyping();
        }
    });
    
    socket.on('history', (data) => {
        if (data.messages && data.messages.length > 0 && chat) {
            chat.loadHistory();
        }
    });
    
    socket.on('error', (data) => {
        console.error('Server error:', data);
        if (chat) chat.addMessage('assistant', `❌ Error: ${data.message}`, true);
        if (avatar) avatar.error();
    });
    
    // Load voice languages
    try {
        const langResponse = await api.getLanguages();
        if (langResponse.success) {
            const select = document.getElementById('voiceLanguageSelect');
            langResponse.languages.forEach(lang => {
                const option = document.createElement('option');
                option.value = lang.code;
                option.textContent = lang.name;
                if (lang.code === langResponse.current) {
                    option.selected = true;
                }
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading languages:', error);
    }
    
    // Hide avatar when messages appear
    if (chat && chat.messagesList) {
        const observer = new MutationObserver(() => {
            if (chat.messagesList.children.length > 0) {
                if (avatar) avatar.hide();
            } else {
                if (avatar) avatar.show();
            }
        });
        
        observer.observe(chat.messagesList, { childList: true });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K to focus input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const messageInput = document.getElementById('messageInput');
            if (messageInput) {
                messageInput.focus();
            }
        }
        
        // Ctrl/Cmd + / for help
        if ((e.ctrlKey || e.metaKey) && e.key === '/') {
            e.preventDefault();
            if (chat) chat.addMessage('assistant', 'Type /help to see all available commands!');
        }
    });
    
    console.log('NOVA Web Interface Ready!');
});

function updateStatus(status) {
    const statusIndicator = document.getElementById('statusIndicator');
    const statusDot = statusIndicator.querySelector('.status-dot');
    const statusText = statusIndicator.querySelector('.status-text');
    
    statusText.textContent = status === 'online' ? 'Online' : 'Offline';
    // Update status dot color using class
    statusDot.classList.remove('status-online', 'status-offline');
    statusDot.classList.add(status === 'online' ? 'status-online' : 'status-offline');
}

// Handle page visibility
document.addEventListener('visibilitychange', () => {
    if (document.hidden && voice) {
        voice.stopSpeaking();
    }
});

// Handle before unload
window.addEventListener('beforeunload', () => {
    if (socket) {
        socket.disconnect();
    }
});

