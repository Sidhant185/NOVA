/**
 * Search Controller
 * Handles real-time web search functionality
 */

class SearchController {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.searchContainer = document.getElementById('searchContainer');
        this.searchSuggestions = document.getElementById('searchSuggestions');
        this.searchWebButton = document.getElementById('searchWebButton');
        this.suggestionTimeout = null;
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        if (!this.searchInput) return;
        
        // Search input events
        this.searchInput.addEventListener('input', (e) => {
            this.handleSearchInput(e.target.value);
        });
        
        this.searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.performSearch(this.searchInput.value);
            } else if (e.key === 'Escape') {
                this.hideSuggestions();
            }
        });
        
        this.searchInput.addEventListener('focus', () => {
            if (this.searchInput.value.length >= 2) {
                this.showSuggestions();
            }
        });
        
        // Search web button
        if (this.searchWebButton) {
            this.searchWebButton.addEventListener('click', () => {
                const messageInput = document.getElementById('messageInput');
                if (messageInput && messageInput.value.trim()) {
                    this.performSearch(messageInput.value);
                } else {
                    this.searchInput.focus();
                }
            });
        }
        
        // Click outside to close suggestions
        document.addEventListener('click', (e) => {
            if (!this.searchContainer.contains(e.target)) {
                this.hideSuggestions();
            }
        });
    }
    
    async handleSearchInput(query) {
        if (this.suggestionTimeout) {
            clearTimeout(this.suggestionTimeout);
        }
        
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        this.suggestionTimeout = setTimeout(async () => {
            await this.fetchSuggestions(query);
        }, 300);
    }
    
    async fetchSuggestions(query) {
        try {
            const response = await fetch(`/api/search/suggest?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success && data.suggestions.length > 0) {
                this.showSuggestions(data.suggestions);
            } else {
                this.hideSuggestions();
            }
        } catch (error) {
            console.error('Error fetching suggestions:', error);
            this.hideSuggestions();
        }
    }
    
    showSuggestions(suggestions = []) {
        if (!this.searchSuggestions) return;
        
        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        this.searchSuggestions.innerHTML = '';
        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'search-suggestion-item';
            item.textContent = suggestion;
            item.addEventListener('click', () => {
                this.searchInput.value = suggestion;
                this.hideSuggestions();
                this.performSearch(suggestion);
            });
            this.searchSuggestions.appendChild(item);
        });
        
        this.searchSuggestions.classList.add('visible');
    }
    
    hideSuggestions() {
        if (this.searchSuggestions) {
            this.searchSuggestions.classList.remove('visible');
            this.searchSuggestions.innerHTML = '';
        }
    }
    
    async performSearch(query) {
        if (!query || !query.trim()) return;
        
        const searchQuery = query.trim();
        this.hideSuggestions();
        
        // Add search query to chat input and send
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.value = `/search ${searchQuery}`;
            messageInput.dispatchEvent(new Event('input'));
            
            // Trigger send
            const sendButton = document.getElementById('sendButton');
            if (sendButton) {
                sendButton.click();
            }
        }
        
        // Clear search input
        if (this.searchInput) {
            this.searchInput.value = '';
        }
    }
}

// Initialize search controller
let searchController;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        searchController = new SearchController();
        window.searchController = searchController;
    });
} else {
    searchController = new SearchController();
    window.searchController = searchController;
}

