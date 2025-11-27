/**
 * UI Controller
 * Manages UI interactions, modals, sidebar, settings
 */

class UIController {
    constructor() {
        this.sidebar = document.getElementById('sidebar');
        this.sidebarToggle = document.getElementById('sidebarToggle');
        this.sidebarOverlay = document.getElementById('sidebarOverlay');
        this.settingsModal = document.getElementById('settingsModal');
        this.memoryModal = document.getElementById('memoryModal');
        this.memoryList = document.getElementById('memoryList');
        
        // Load sidebar state from localStorage
        const sidebarOpen = localStorage.getItem('sidebarOpen') === 'true';
        if (sidebarOpen) {
            this.sidebar.classList.add('open');
            this.updateMainContentClass();
            this.updateOverlay();
        }
        
        // Load collapsed sections state
        this.loadCollapsedSections();
        
        // Load panel state
        this.loadPanelState();
        
        this.setupEventListeners();
        this.loadMemories();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    setupEventListeners() {
        // Sidebar toggle
        this.sidebarToggle.addEventListener('click', () => {
            this.toggleSidebar();
        });
        
        // Sidebar overlay click to close
        if (this.sidebarOverlay) {
            this.sidebarOverlay.addEventListener('click', () => {
                this.closeSidebar();
            });
        }
        
        // Collapsible sections
        document.querySelectorAll('.collapsible-header').forEach(header => {
            header.addEventListener('click', (e) => {
                // Don't toggle if clicking the add memory button
                if (e.target.closest('#addMemoryBtn')) {
                    return;
                }
                this.toggleSection(header);
            });
        });
        
        // Panel toggles
        const layoutToggle = document.getElementById('layoutToggle');
        const chatPanelToggle = document.getElementById('chatPanelToggle');
        
        if (layoutToggle) {
            layoutToggle.addEventListener('click', () => {
                this.toggleLayout();
            });
        }
        
        if (chatPanelToggle) {
            chatPanelToggle.addEventListener('click', () => {
                this.toggleChatPanel();
            });
        }
        
        // Code panel controls
        const codePanelClose = document.getElementById('codePanelClose');
        const codePanelCopy = document.getElementById('codePanelCopy');
        const codePanelFullscreen = document.getElementById('codePanelFullscreen');
        
        if (codePanelClose) {
            codePanelClose.addEventListener('click', () => {
                this.closeCodePanel();
            });
        }
        
        if (codePanelCopy) {
            codePanelCopy.addEventListener('click', () => {
                this.copyCodePanelContent();
            });
        }
        
        if (codePanelFullscreen) {
            codePanelFullscreen.addEventListener('click', () => {
                this.toggleCodePanelFullscreen();
            });
        }
        
        // Initialize resizer
        this.initResizer();
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + B to toggle sidebar
            if ((e.ctrlKey || e.metaKey) && e.key === 'b') {
                e.preventDefault();
                this.toggleSidebar();
            }
            
            // Ctrl/Cmd + Shift + C to toggle chat panel
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'C') {
                e.preventDefault();
                this.toggleChatPanel();
            }
            
            // Ctrl/Cmd + \ to toggle layout
            if ((e.ctrlKey || e.metaKey) && e.key === '\\') {
                e.preventDefault();
                this.toggleLayout();
            }
            
            // Ctrl/Cmd + Shift + K to toggle code panel
            if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'K') {
                e.preventDefault();
                this.toggleCodePanel();
            }
            
            // Esc to close sidebar, modals, or code panel
            if (e.key === 'Escape') {
                if (this.sidebar.classList.contains('open')) {
                    this.closeSidebar();
                }
                if (this.settingsModal.style.display === 'flex') {
                    this.closeSettings();
                }
                if (this.memoryModal.style.display === 'flex') {
                    this.closeMemoryModal();
                }
                const codePanel = document.getElementById('codePanel');
                if (codePanel && !codePanel.classList.contains('hidden')) {
                    this.closeCodePanel();
                }
            }
        });

        // Settings
        document.getElementById('settingsBtn').addEventListener('click', () => {
            this.openSettings();
        });

        document.getElementById('closeSettingsBtn').addEventListener('click', () => {
            this.closeSettings();
        });

        // Memory management
        document.getElementById('addMemoryBtn').addEventListener('click', () => {
            this.openMemoryModal();
        });

        document.getElementById('closeMemoryBtn').addEventListener('click', () => {
            this.closeMemoryModal();
        });

        document.getElementById('saveMemoryBtn').addEventListener('click', () => {
            this.saveMemory();
        });

        // Theme toggle
        const themeSelect = document.getElementById('themeSelect');
        if (themeSelect) {
            themeSelect.addEventListener('change', async (e) => {
                this.setTheme(e.target.value);
                // Save to profile
                if (window.profileController) {
                    await window.profileController.updatePreferences({
                        theme: e.target.value
                    });
                }
            });
        }

        // TTS toggle
        const ttsEnabled = document.getElementById('ttsEnabled');
        ttsEnabled.addEventListener('change', (e) => {
            if (window.appConfig) {
                window.appConfig.tts_enabled = e.target.checked;
                localStorage.setItem('tts_enabled', e.target.checked);
            }
        });

        // Quick actions
        document.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.target.dataset.action;
                if (action === 'help') {
                    chat.addMessage('assistant', 'Type /help to see all available commands!');
                } else if (action === 'memories') {
                    this.openSidebar();
                }
            });
        });

        // Close modals on outside click
        [this.settingsModal, this.memoryModal].forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.style.display = 'none';
                }
            });
        });
    }

    openSettings() {
        // Load current settings
        const theme = localStorage.getItem('theme') || 'dark';
        document.getElementById('themeSelect').value = theme;
        
        const ttsEnabled = localStorage.getItem('tts_enabled') !== 'false';
        document.getElementById('ttsEnabled').checked = ttsEnabled;
        
        this.settingsModal.style.display = 'flex';
    }

    closeSettings() {
        this.settingsModal.style.display = 'none';
    }

    setTheme(theme) {
        document.body.className = `theme-${theme}`;
        localStorage.setItem('theme', theme);
    }

    openMemoryModal() {
        document.getElementById('memoryKey').value = '';
        document.getElementById('memoryValue').value = '';
        this.memoryModal.style.display = 'flex';
    }

    closeMemoryModal() {
        this.memoryModal.style.display = 'none';
    }

    async saveMemory() {
        const key = document.getElementById('memoryKey').value.trim();
        const value = document.getElementById('memoryValue').value.trim();

        if (!key || !value) {
            alert('Please fill in both key and value');
            return;
        }

        try {
            await api.addMemory(key, value);
            this.closeMemoryModal();
            this.loadMemories();
        } catch (error) {
            console.error('Error saving memory:', error);
            alert('Error saving memory: ' + error.message);
        }
    }

    async loadMemories() {
        try {
            const response = await api.getMemories();
            if (response.success) {
                this.renderMemories(response.memories);
            }
        } catch (error) {
            console.error('Error loading memories:', error);
        }
    }

    renderMemories(memories) {
        if (!memories || Object.keys(memories).length === 0) {
            this.memoryList.innerHTML = '<p class="empty-state">No memories yet</p>';
            return;
        }

        this.memoryList.innerHTML = '';
        
        Object.entries(memories).forEach(([key, data]) => {
            const value = typeof data === 'object' ? data.value : data;
            
            const item = document.createElement('div');
            item.className = 'memory-item';
            
            item.innerHTML = `
                <div class="memory-content">
                    <div class="memory-key">${this.escapeHtml(key)}</div>
                    <div class="memory-value">${this.escapeHtml(value)}</div>
                </div>
                <button class="memory-delete" data-key="${this.escapeHtml(key)}">×</button>
            `;
            
            item.querySelector('.memory-delete').addEventListener('click', async () => {
                if (confirm(`Delete memory "${key}"?`)) {
                    try {
                        await api.deleteMemory(key);
                        this.loadMemories();
                    } catch (error) {
                        console.error('Error deleting memory:', error);
                        alert('Error deleting memory');
                    }
                }
            });
            
            this.memoryList.appendChild(item);
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    toggleSidebar() {
        this.sidebar.classList.toggle('open');
        this.updateMainContentClass();
        this.updateOverlay();
        localStorage.setItem('sidebarOpen', this.sidebar.classList.contains('open'));
    }
    
    openSidebar() {
        this.sidebar.classList.add('open');
        this.updateMainContentClass();
        this.updateOverlay();
        localStorage.setItem('sidebarOpen', 'true');
    }
    
    closeSidebar() {
        this.sidebar.classList.remove('open');
        this.updateMainContentClass();
        this.updateOverlay();
        localStorage.setItem('sidebarOpen', 'false');
    }
    
    updateMainContentClass() {
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            if (this.sidebar.classList.contains('open') && window.innerWidth > 768) {
                mainContent.classList.add('sidebar-open');
            } else {
                mainContent.classList.remove('sidebar-open');
            }
        }
    }
    
    updateOverlay() {
        if (this.sidebarOverlay) {
            if (this.sidebar.classList.contains('open') && window.innerWidth <= 768) {
                this.sidebarOverlay.classList.add('active');
            } else {
                this.sidebarOverlay.classList.remove('active');
            }
        }
    }
    
    // Handle window resize to update sidebar state
    handleResize() {
        this.updateMainContentClass();
        this.updateOverlay();
    }
    
    toggleSection(header) {
        const section = header.dataset.section;
        const content = document.querySelector(`.collapsible-content[data-section="${section}"]`);
        
        if (!content) return;
        
        const isCollapsed = header.classList.contains('collapsed');
        
        if (isCollapsed) {
            header.classList.remove('collapsed');
            content.classList.remove('collapsed');
            localStorage.setItem(`section_${section}_collapsed`, 'false');
        } else {
            header.classList.add('collapsed');
            content.classList.add('collapsed');
            localStorage.setItem(`section_${section}_collapsed`, 'true');
        }
    }
    
    loadCollapsedSections() {
        document.querySelectorAll('.collapsible-header').forEach(header => {
            const section = header.dataset.section;
            const isCollapsed = localStorage.getItem(`section_${section}_collapsed`) === 'true';
            
            if (isCollapsed) {
                header.classList.add('collapsed');
                const content = document.querySelector(`.collapsible-content[data-section="${section}"]`);
                if (content) {
                    content.classList.add('collapsed');
                }
            }
        });
    }
    
    toggleLayout() {
        const chatPanel = document.getElementById('chatPanel');
        const codePanel = document.getElementById('codePanel');
        
        if (codePanel.classList.contains('hidden')) {
            // Switch to split view
            if (window.codeBlocks && window.codeBlocks.length > 0) {
                codePanel.classList.remove('hidden');
                chatPanel.classList.remove('full');
                chatPanel.classList.add('half');
            }
        } else {
            // Toggle between split and chat-only
            if (chatPanel.classList.contains('half')) {
                // Go to chat-only
                codePanel.classList.add('hidden');
                chatPanel.classList.remove('half');
                chatPanel.classList.add('full');
            } else {
                // Go to split
                codePanel.classList.remove('hidden');
                chatPanel.classList.remove('full');
                chatPanel.classList.add('half');
            }
        }
        
        this.savePanelState();
    }
    
    toggleChatPanel() {
        const chatPanel = document.getElementById('chatPanel');
        
        if (chatPanel.classList.contains('hidden')) {
            chatPanel.classList.remove('hidden');
            chatPanel.classList.add('full');
        } else if (chatPanel.classList.contains('full')) {
            chatPanel.classList.remove('full');
            chatPanel.classList.add('half');
        } else if (chatPanel.classList.contains('half')) {
            chatPanel.classList.remove('half');
            chatPanel.classList.add('collapsed');
        } else {
            chatPanel.classList.remove('collapsed');
            chatPanel.classList.add('hidden');
        }
        
        this.savePanelState();
    }
    
    toggleCodePanel() {
        const codePanel = document.getElementById('codePanel');
        const chatPanel = document.getElementById('chatPanel');
        
        if (codePanel.classList.contains('hidden')) {
            if (window.codeBlocks && window.codeBlocks.length > 0) {
                codePanel.classList.remove('hidden');
                chatPanel.classList.remove('full');
                chatPanel.classList.add('half');
            }
        } else {
            codePanel.classList.add('hidden');
            chatPanel.classList.remove('half');
            chatPanel.classList.add('full');
        }
        
        this.savePanelState();
    }
    
    closeCodePanel() {
        const codePanel = document.getElementById('codePanel');
        const chatPanel = document.getElementById('chatPanel');
        
        codePanel.classList.add('hidden');
        chatPanel.classList.remove('half');
        chatPanel.classList.add('full');
        
        this.savePanelState();
    }
    
    copyCodePanelContent() {
        const codePanelContent = document.getElementById('codePanelContent');
        const codeElement = codePanelContent.querySelector('code');
        
        if (codeElement) {
            const code = codeElement.textContent;
            navigator.clipboard.writeText(code).then(() => {
                const btn = document.getElementById('codePanelCopy');
                const originalHTML = btn.innerHTML;
                btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"><polyline points="20 6 9 17 4 12"></polyline></svg>';
                btn.style.color = 'var(--success)';
                setTimeout(() => {
                    btn.innerHTML = originalHTML;
                    btn.style.color = '';
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy:', err);
            });
        }
    }
    
    toggleCodePanelFullscreen() {
        const codePanel = document.getElementById('codePanel');
        codePanel.classList.toggle('fullscreen');
        
        const btn = document.getElementById('codePanelFullscreen');
        if (codePanel.classList.contains('fullscreen')) {
            btn.title = 'Exit Fullscreen';
        } else {
            btn.title = 'Fullscreen';
        }
    }
    
    initResizer() {
        const resizer = document.getElementById('resizer');
        const chatPanel = document.getElementById('chatPanel');
        const codePanel = document.getElementById('codePanel');
        
        if (!resizer || !chatPanel || !codePanel) return;
        
        let isResizing = false;
        let startX = 0;
        let startY = 0;
        let startChatWidth = 0;
        let startCodeWidth = 0;
        let startChatHeight = 0;
        let startCodeHeight = 0;
        let isMobile = window.innerWidth <= 768;
        
        const handleResizeStart = (e) => {
            isResizing = true;
            if (isMobile) {
                startY = e.clientY || e.touches[0].clientY;
                startChatHeight = chatPanel.offsetHeight;
                startCodeHeight = codePanel.offsetHeight;
            } else {
                startX = e.clientX || e.touches[0].clientX;
                startChatWidth = chatPanel.offsetWidth;
                startCodeWidth = codePanel.offsetWidth;
            }
            resizer.classList.add('active');
            document.body.classList.add('panel-resizing');
            e.preventDefault();
        };
        
        const handleResizeMove = (e) => {
            if (!isResizing) return;
            
            if (isMobile) {
                const deltaY = (e.clientY || e.touches[0].clientY) - startY;
                const containerHeight = document.getElementById('splitPaneContainer').offsetHeight;
                
                const newChatHeight = startChatHeight + deltaY;
                const newCodeHeight = startCodeHeight - deltaY;
                
                const minHeight = 200;
                
                if (newChatHeight >= minHeight && newCodeHeight >= minHeight) {
                    chatPanel.style.height = `${newChatHeight}px`;
                    codePanel.style.height = `${newCodeHeight}px`;
                }
            } else {
                const deltaX = (e.clientX || e.touches[0].clientX) - startX;
                
                const newChatWidth = startChatWidth + deltaX;
                const newCodeWidth = startCodeWidth - deltaX;
                
                const minChatWidth = 300;
                const minCodeWidth = 400;
                
                if (newChatWidth >= minChatWidth && newCodeWidth >= minCodeWidth) {
                    chatPanel.style.width = `${newChatWidth}px`;
                    codePanel.style.width = `${newCodeWidth}px`;
                    chatPanel.classList.remove('half', 'full');
                    codePanel.classList.remove('half', 'full');
                }
            }
        };
        
        const handleResizeEnd = () => {
            if (isResizing) {
                isResizing = false;
                resizer.classList.remove('active');
                document.body.classList.remove('panel-resizing');
                this.savePanelState();
            }
        };
        
        resizer.addEventListener('mousedown', handleResizeStart);
        resizer.addEventListener('touchstart', handleResizeStart, { passive: false });
        
        document.addEventListener('mousemove', handleResizeMove);
        document.addEventListener('touchmove', handleResizeMove, { passive: false });
        
        document.addEventListener('mouseup', handleResizeEnd);
        document.addEventListener('touchend', handleResizeEnd);
        
        // Update mobile state on resize
        window.addEventListener('resize', () => {
            isMobile = window.innerWidth <= 768;
        });
    }
    
    savePanelState() {
        const chatPanel = document.getElementById('chatPanel');
        const codePanel = document.getElementById('codePanel');
        
        const state = {
            chatPanelState: chatPanel.className.split(' ').find(c => ['full', 'half', 'collapsed', 'hidden'].includes(c)) || 'full',
            codePanelVisible: !codePanel.classList.contains('hidden'),
            chatPanelWidth: chatPanel.style.width || '',
            codePanelWidth: codePanel.style.width || ''
        };
        
        localStorage.setItem('panelState', JSON.stringify(state));
    }
    
    loadPanelState() {
        const saved = localStorage.getItem('panelState');
        if (!saved) return;
        
        try {
            const state = JSON.parse(saved);
            const chatPanel = document.getElementById('chatPanel');
            const codePanel = document.getElementById('codePanel');
            
            if (chatPanel) {
                chatPanel.classList.remove('full', 'half', 'collapsed', 'hidden');
                chatPanel.classList.add(state.chatPanelState);
                if (state.chatPanelWidth) {
                    chatPanel.style.width = state.chatPanelWidth;
                }
            }
            
            if (codePanel) {
                if (!state.codePanelVisible) {
                    codePanel.classList.add('hidden');
                } else {
                    codePanel.classList.remove('hidden');
                }
                if (state.codePanelWidth) {
                    codePanel.style.width = state.codePanelWidth;
                }
            }
        } catch (e) {
            console.error('Error loading panel state:', e);
        }
    }
}

// Export singleton instance
// Initialize UI controller after DOM is ready
let ui;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        ui = new UIController();
        window.ui = ui; // Make available globally
    });
} else {
    ui = new UIController();
    window.ui = ui; // Make available globally
}

