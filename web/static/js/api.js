/**
 * API Client for NOVA Web Interface
 * Handles all API communication
 */

class APIClient {
    constructor() {
        this.baseURL = '';
        this.sessionId = this.getOrCreateSessionId();
    }

    getOrCreateSessionId() {
        let sessionId = localStorage.getItem('nova_session_id');
        if (!sessionId) {
            sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('nova_session_id', sessionId);
        }
        return sessionId;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const method = options.method || 'GET';
        const config = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-Session-ID': this.sessionId,
                ...(options.headers || {})
            }
        };

        if (options.body && typeof options.body === 'object') {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    // Chat methods
    async sendMessage(message) {
        return this.request('/api/chat/send', {
            method: 'POST',
            body: { message, session_id: this.sessionId }
        });
    }

    async getHistory() {
        return this.request(`/api/chat/history?session_id=${this.sessionId}`);
    }

    async clearHistory() {
        return this.request('/api/chat/clear', {
            method: 'POST',
            body: { session_id: this.sessionId }
        });
    }

    async exportHistory() {
        return this.request(`/api/chat/export?session_id=${this.sessionId}`);
    }

    // Memory methods
    async getMemories() {
        return this.request(`/api/memory?session_id=${this.sessionId}`, {
            method: 'GET'
        });
    }

    async addMemory(key, value) {
        return this.request('/api/memory', {
            method: 'POST',
            body: { key, value, session_id: this.sessionId }
        });
    }

    async deleteMemory(key) {
        return this.request(`/api/memory/${key}?session_id=${this.sessionId}`, {
            method: 'DELETE'
        });
    }

    // Config methods
    async getConfig() {
        return this.request('/api/config');
    }

    // Voice methods
    async getLanguages() {
        return this.request('/api/voice/languages');
    }
    
    // Profile API
    async getProfile(userId = 'default') {
        return this.request(`/api/profile/get?user_id=${userId}`, {
            method: 'GET'
        });
    }
    
    async updateProfile(userId, updates) {
        return this.request('/api/profile/update', {
            method: 'POST',
            body: {
                user_id: userId,
                updates: updates
            }
        });
    }
    
    async updatePreferences(userId, preferences) {
        return this.request('/api/profile/preferences', {
            method: 'POST',
            body: {
                user_id: userId,
                preferences: preferences
            }
        });
    }
    
    // Search API
    async search(query, maxResults = 5) {
        return this.request('/api/search', {
            method: 'POST',
            body: {
                query: query,
                max_results: maxResults
            }
        });
    }
    
    async getSearchSuggestions(query) {
        return this.request(`/api/search/suggest?q=${encodeURIComponent(query)}`, {
            method: 'GET'
        });
    }
}

// Export singleton instance
// Initialize API client immediately (no DOM dependency)
const api = new APIClient();
window.api = api; // Make available globally

