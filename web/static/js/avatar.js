/**
 * Avatar Animation Controller
 * Manages avatar states and animations
 */

class AvatarController {
    constructor() {
        this.avatar = document.getElementById('avatar');
        this.avatarStatus = document.getElementById('avatarStatus');
        this.avatarContainer = document.getElementById('avatarContainer');
        this.currentState = 'idle';
    }

    setState(state, message = '') {
        if (this.currentState === state) return;
        
        // Remove all state classes
        this.avatar.classList.remove('listening', 'thinking', 'speaking', 'error', 'success');
        
        // Add new state class
        if (state !== 'idle') {
            this.avatar.classList.add(state);
        }
        
        this.currentState = state;
        
        // Update status message
        if (message) {
            this.avatarStatus.textContent = message;
        } else {
            this.updateStatusMessage(state);
        }
    }

    updateStatusMessage(state) {
        const messages = {
            'idle': 'Ready to help you',
            'listening': 'Listening to you...',
            'thinking': 'Let me think about that...',
            'speaking': 'Speaking to you...',
            'error': 'Oh no! Something went wrong',
            'success': 'All done! ✨'
        };
        
        this.avatarStatus.textContent = messages[state] || 'Ready to help you';
    }

    show() {
        this.avatarContainer.classList.remove('hidden');
    }

    hide() {
        this.avatarContainer.classList.add('hidden');
    }

    // State methods
    idle() {
        this.setState('idle');
    }

    listening() {
        this.setState('listening');
    }

    thinking() {
        this.setState('thinking');
    }

    speaking() {
        this.setState('speaking');
    }

    error() {
        this.setState('error');
        setTimeout(() => this.idle(), 3000);
    }

    success() {
        this.setState('success');
        setTimeout(() => this.idle(), 2000);
    }
}

// Export singleton instance
// Initialize avatar controller after DOM is ready
let avatar;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        avatar = new AvatarController();
        window.avatar = avatar; // Make available globally
    });
} else {
    avatar = new AvatarController();
    window.avatar = avatar; // Make available globally
}

