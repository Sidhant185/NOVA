/**
 * Profile Controller
 * Manages user profile, preferences, and personalization
 */

class ProfileController {
    constructor() {
        this.profile = null;
        this.userId = 'default';
        this.loadProfile();
    }
    
    async loadProfile() {
        try {
            const response = await api.getProfile(this.userId);
            if (response.success) {
                this.profile = response.profile;
                this.applyPreferences();
            }
        } catch (error) {
            console.error('Error loading profile:', error);
        }
    }
    
    async updateProfile(updates) {
        try {
            const response = await api.updateProfile(this.userId, updates);
            if (response.success) {
                this.profile = response.profile;
                this.applyPreferences();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error updating profile:', error);
            return false;
        }
    }
    
    async updatePreferences(preferences) {
        try {
            const response = await api.updatePreferences(this.userId, preferences);
            if (response.success) {
                if (this.profile) {
                    this.profile.preferences = { ...this.profile.preferences, ...preferences };
                }
                this.applyPreferences();
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error updating preferences:', error);
            return false;
        }
    }
    
    applyPreferences() {
        if (!this.profile || !this.profile.preferences) return;
        
        const prefs = this.profile.preferences;
        
        // Apply theme
        if (prefs.theme) {
            document.body.classList.remove('theme-dark', 'theme-light');
            document.body.classList.add(`theme-${prefs.theme}`);
        }
        
        // Apply chat style
        if (prefs.chat_style) {
            document.body.setAttribute('data-chat-style', prefs.chat_style);
        }
        
        // Apply message theme
        if (prefs.message_theme) {
            document.body.setAttribute('data-message-theme', prefs.message_theme);
        }
    }
    
    getProfile() {
        return this.profile;
    }
    
    getPreferences() {
        return this.profile ? this.profile.preferences : null;
    }
}

// Initialize profile controller
let profileController;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        profileController = new ProfileController();
        window.profileController = profileController;
    });
} else {
    profileController = new ProfileController();
    window.profileController = profileController;
}

