/**
 * Chat Interface Controller
 * Manages chat messages, history, and interactions
 */

class ChatController {
    constructor() {
        this.messagesContainer = document.getElementById('messagesContainer');
        this.messagesList = document.getElementById('messagesList');
        this.welcomeMessage = document.getElementById('welcomeMessage');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.typingIndicator = document.getElementById('typingIndicator');
        
        this.setupEventListeners();
        this.loadHistory();
    }

    setupEventListeners() {
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        this.messageInput.addEventListener('input', () => {
            // Auto-resize textarea
            this.messageInput.classList.add('auto-height');
            this.messageInput.style.height = this.messageInput.scrollHeight + 'px';
        });

        // Listen for voice transcripts
        document.addEventListener('voiceTranscript', (e) => {
            this.messageInput.value = e.detail;
            this.messageInput.dispatchEvent(new Event('input'));
        });
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message) return;

        // Hide welcome message
        if (this.welcomeMessage) {
            this.welcomeMessage.classList.add('hidden');
        }

        // Add user message
        this.addMessage('user', message);
        
        // Clear input
        this.messageInput.value = '';
        this.messageInput.classList.add('auto-height');
        this.messageInput.style.height = 'auto';
        
        // Disable input
        this.setInputEnabled(false);
        
        // Show typing indicator
        this.showTyping();
        avatar.thinking();

        try {
            const response = await api.sendMessage(message);
            
            // Hide typing indicator
            this.hideTyping();
            
            // Check if response has metadata for routing
            // Ensure responseContent is always a string
            let responseContent = response.response || '';
            if (typeof responseContent !== 'string') {
                responseContent = String(responseContent);
            }
            
            let responseMetadata = response.metadata || {};
            
            // Route to research canvas if research query
            if (responseMetadata.is_research && response.research_data && typeof researchCanvas !== 'undefined') {
                researchCanvas.show(message, response.research_data);
                // Still show a brief message in chat
                responseContent = `🔬 Research complete! Check the research canvas for detailed results.`;
            }
            
            // Add assistant response
            this.addMessage('assistant', responseContent);
            
            // Auto-show code panel if code blocks are detected or if code query
            // Ensure responseContent is a string before calling includes
            if (responseMetadata.is_code || (typeof responseContent === 'string' && responseContent.includes('```'))) {
                this.autoShowCodePanel(responseContent);
            }
            
            // Speak response if TTS enabled (only if not research - research is in canvas)
            if (!responseMetadata.is_research && window.appConfig && window.appConfig.tts_enabled) {
                voice.speak(responseContent);
            } else {
                avatar.idle();
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTyping();
            this.addMessage('assistant', `❌ Error: ${error.message}`, true);
            avatar.error();
        } finally {
            this.setInputEnabled(true);
            this.scrollToBottom();
        }
    }

    addMessage(role, content, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // FIRST: Extract code blocks BEFORE any processing
        // More flexible regex: handles code blocks with or without newline after language
        const codeBlockRegex = /```(\w+)?\s*\n?([\s\S]*?)```/g;
        const codeBlocks = [];
        let codeMatch;
        let codeLastIndex = 0;
        const segments = [];
        
        // Extract all code blocks and their positions
        while ((codeMatch = codeBlockRegex.exec(content)) !== null) {
            // Add text before code block
            if (codeMatch.index > codeLastIndex) {
                segments.push({
                    type: 'text',
                    content: content.substring(codeLastIndex, codeMatch.index)
                });
            }
            
            // Store code block
            const language = codeMatch[1] || 'text';
            let codeContent = codeMatch[2];
            // Remove leading/trailing whitespace but preserve internal formatting
            codeContent = codeContent.replace(/^\s+/, '').replace(/\s+$/, '');
            // If code doesn't have proper line breaks, try to format it better
            // For languages like Java, add line breaks after semicolons and braces
            if (language && ['java', 'javascript', 'js', 'cpp', 'c', 'csharp', 'cs'].includes(language.toLowerCase())) {
                // Add line breaks after semicolons (but not in strings)
                codeContent = codeContent.replace(/;\s*(?![^"']*["'])/g, ';\n');
                // Add line breaks after opening braces
                codeContent = codeContent.replace(/\{\s*/g, '{\n');
                // Add line breaks before closing braces
                codeContent = codeContent.replace(/\s*\}/g, '\n}');
                // Clean up multiple consecutive newlines
                codeContent = codeContent.replace(/\n{3,}/g, '\n\n');
            }
            
            const codeId = 'code-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9) + '-' + codeBlocks.length;
            codeBlocks.push({
                codeId: codeId,
                language: language,
                code: codeContent
            });
            
            segments.push({
                type: 'code',
                codeId: codeId
            });
            
            codeLastIndex = codeMatch.index + codeMatch[0].length;
        }
        
        // Add remaining text
        if (codeLastIndex < content.length) {
            segments.push({
                type: 'text',
                content: content.substring(codeLastIndex)
            });
        }
        
        // Build the content using DOM methods
        segments.forEach(segment => {
            if (segment.type === 'text') {
                // Process text for markdown (bold, italic, inline code, line breaks)
                const processedText = this.formatTextOnly(segment.content);
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = processedText;
                while (tempDiv.firstChild) {
                    contentDiv.appendChild(tempDiv.firstChild);
                }
            } else if (segment.type === 'code') {
                // Find the code block data
                const codeBlock = codeBlocks.find(cb => cb.codeId === segment.codeId);
                if (codeBlock) {
                    // Create code block using DOM methods to preserve formatting
                    const wrapper = document.createElement('div');
                    wrapper.className = 'code-block-wrapper';
                    wrapper.setAttribute('data-code-id', codeBlock.codeId);
                    wrapper.setAttribute('data-language', codeBlock.language);
                    
                    const header = document.createElement('div');
                    header.className = 'code-block-header';
                    header.innerHTML = `
                        <span class="code-block-language">${codeBlock.language}</span>
                        <div class="code-block-actions">
                            <button class="code-block-view-panel-btn" data-code-id="${codeBlock.codeId}" data-language="${codeBlock.language}" title="View in Code Panel">
                                <span>📋</span>
                                <span>View in Panel</span>
                            </button>
                            <button class="code-copy-btn" data-code-id="${codeBlock.codeId}" title="Copy code">
                                <span class="copy-icon">📋</span>
                                <span class="copy-text">Copy</span>
                            </button>
                        </div>
                    `;
                    
                    const pre = document.createElement('pre');
                    const code = document.createElement('code');
                    code.id = codeBlock.codeId;
                    code.className = `language-${codeBlock.language}`;
                    // CRITICAL: Use textContent to preserve all formatting including newlines
                    // This preserves the exact formatting without any HTML processing
                    code.textContent = codeBlock.code;
                    code.classList.add('code-preserve-format');
                    
                    pre.classList.add('code-preserve-format');
                    pre.style.margin = '0';
                    pre.style.padding = '0';
                    pre.appendChild(code);
                    
                    wrapper.appendChild(header);
                    wrapper.appendChild(pre);
                    contentDiv.appendChild(wrapper);
                }
            }
        });
        
        bubble.appendChild(contentDiv);
        
        // Add timestamp and actions
        const footer = document.createElement('div');
        footer.classList.add('flex', 'flex-col', 'gap-1');
        
        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString();
        footer.appendChild(timestamp);
        
        // Add message actions (copy, etc.)
        if (role === 'assistant') {
            const actions = document.createElement('div');
            actions.className = 'message-actions';
            
            const copyBtn = document.createElement('button');
            copyBtn.className = 'message-action-btn';
            copyBtn.innerHTML = '<span>📋</span> <span>Copy</span>';
            copyBtn.title = 'Copy message';
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(content).then(() => {
                    copyBtn.innerHTML = '<span>✓</span> <span>Copied</span>';
                    setTimeout(() => {
                        copyBtn.innerHTML = '<span>📋</span> <span>Copy</span>';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy:', err);
                });
            });
            
            actions.appendChild(copyBtn);
            footer.appendChild(actions);
        }
        
        bubble.appendChild(footer);
        
        messageDiv.appendChild(bubble);
        
        if (isError) {
            messageDiv.classList.add('error');
        }
        
        this.messagesList.appendChild(messageDiv);
        
        // Setup code copy buttons
        this.setupCodeCopyButtons(messageDiv);
        
        // Highlight code blocks - but preserve formatting
        if (typeof Prism !== 'undefined') {
            const codeElements = messageDiv.querySelectorAll('code');
            
            // Store original text content before Prism modifies it
            const originalTexts = new Map();
            codeElements.forEach(codeEl => {
                originalTexts.set(codeEl, codeEl.textContent);
                // Set styles before Prism
                codeEl.classList.add('code-preserve-format');
                
                const preEl = codeEl.parentElement;
                if (preEl && preEl.tagName === 'PRE') {
                    preEl.classList.add('code-preserve-format');
                }
            });
            
            Prism.highlightAllUnder(messageDiv);
            
            // After Prism, ensure formatting is still preserved
            codeElements.forEach(codeEl => {
                // Re-apply styles
                codeEl.classList.add('code-preserve-format');
                
                // If Prism removed newlines, restore them
                const originalText = originalTexts.get(codeEl);
                if (originalText && codeEl.textContent !== originalText) {
                    // Prism might have modified the content, but we need to preserve formatting
                    // The innerHTML from Prism should preserve newlines if CSS is correct
                }
                
                const preEl = codeEl.parentElement;
                if (preEl && preEl.tagName === 'PRE') {
                    preEl.classList.add('code-preserve-format');
                }
            });
        }
        
        this.scrollToBottom();
    }
    
    setupCodeCopyButtons(container) {
        const copyButtons = container.querySelectorAll('.code-copy-btn');
        copyButtons.forEach(btn => {
            btn.addEventListener('click', async () => {
                const codeId = btn.dataset.codeId;
                const codeElement = document.getElementById(codeId);
                if (!codeElement) return;
                
                const code = codeElement.textContent;
                
                try {
                    await navigator.clipboard.writeText(code);
                    
                    // Update button state
                    const copyText = btn.querySelector('.copy-text');
                    const originalText = copyText.textContent;
                    copyText.textContent = 'Copied!';
                    btn.classList.add('copied');
                    
                    setTimeout(() => {
                        copyText.textContent = originalText;
                        btn.classList.remove('copied');
                    }, 2000);
                } catch (err) {
                    console.error('Failed to copy code:', err);
                    // Fallback for older browsers
                    const textArea = document.createElement('textarea');
                    textArea.value = code;
                    textArea.style.position = 'fixed';
                    textArea.style.opacity = '0';
                    document.body.appendChild(textArea);
                    textArea.select();
                    try {
                        document.execCommand('copy');
                        btn.querySelector('.copy-text').textContent = 'Copied!';
                    } catch (e) {
                        btn.querySelector('.copy-text').textContent = 'Failed';
                    }
                    document.body.removeChild(textArea);
                }
            });
        });
        
        // Setup "View in Panel" buttons
        const viewPanelButtons = container.querySelectorAll('.code-block-view-panel-btn');
        viewPanelButtons.forEach(btn => {
            btn.addEventListener('click', () => {
                const codeId = btn.dataset.codeId;
                const language = btn.dataset.language || 'text';
                const codeElement = document.getElementById(codeId);
                if (!codeElement) return;
                
                const code = codeElement.textContent;
                this.showCodeInPanel(code, language, codeId);
            });
        });
    }
    
    showCodeInPanel(code, language, codeId) {
        // Show code panel
        const codePanel = document.getElementById('codePanel');
        if (!codePanel) return;
        
        codePanel.classList.remove('hidden');
        
        // Update panel content
        const codePanelContent = document.getElementById('codePanelContent');
        const codePanelLanguage = document.getElementById('codePanelLanguage');
        const codePanelName = document.getElementById('codePanelName');
        
        if (codePanelLanguage) {
            codePanelLanguage.textContent = language.toUpperCase();
        }
        if (codePanelName) {
            codePanelName.textContent = `code.${language}`;
        }
        
        // Clear empty state
        if (codePanelContent) {
            codePanelContent.innerHTML = '';
        }
        
        // Store code block data
        if (!window.codeBlocks) {
            window.codeBlocks = [];
        }
        
        const codeBlockData = {
            id: codeId,
            language: language,
            code: code,
            timestamp: Date.now()
        };
        
        // Check if code block already exists
        const existingIndex = window.codeBlocks.findIndex(cb => cb.id === codeId);
        if (existingIndex >= 0) {
            window.codeBlocks[existingIndex] = codeBlockData;
        } else {
            window.codeBlocks.push(codeBlockData);
        }
        
        // Update tabs
        this.updateCodePanelTabs();
        
        // Set active tab
        this.setActiveCodeTab(codeId);
        
        // Adjust chat panel to half width
        const chatPanel = document.getElementById('chatPanel');
        if (chatPanel) {
            chatPanel.classList.remove('full');
            chatPanel.classList.add('half');
        }
    }
    
    updateCodePanelTabs() {
        const tabsContainer = document.getElementById('codePanelTabs');
        if (!tabsContainer) return;
        
        tabsContainer.innerHTML = '';
        
        if (!window.codeBlocks || window.codeBlocks.length === 0) {
            return;
        }
        
        // Only show tabs if there are multiple code blocks
        if (window.codeBlocks.length <= 1) {
            return;
        }
        
        window.codeBlocks.forEach((codeBlock, index) => {
            const tab = document.createElement('div');
            tab.className = 'code-panel-tab';
            if (index === window.codeBlocks.length - 1) {
                tab.classList.add('active');
            }
            tab.innerHTML = `
                <span>💻</span>
                <span>${codeBlock.language.toUpperCase()}</span>
            `;
            tab.addEventListener('click', () => {
                this.setActiveCodeTab(codeBlock.id);
            });
            tabsContainer.appendChild(tab);
        });
    }
    
    setActiveCodeTab(codeId) {
        const codeBlock = window.codeBlocks.find(cb => cb.id === codeId);
        if (!codeBlock) return;
        
        // Update active tab
        const tabs = document.querySelectorAll('.code-panel-tab');
        tabs.forEach((tab, index) => {
            const block = window.codeBlocks[index];
            if (block && block.id === codeId) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });
        
        // Update panel content
        const codePanelContent = document.getElementById('codePanelContent');
        const codePanelLanguage = document.getElementById('codePanelLanguage');
        const codePanelName = document.getElementById('codePanelName');
        
        if (codePanelLanguage) {
            codePanelLanguage.textContent = codeBlock.language.toUpperCase();
        }
        if (codePanelName) {
            codePanelName.textContent = `code.${codeBlock.language}`;
        }
        
        if (codePanelContent) {
            codePanelContent.innerHTML = '';
            const codeDiv = document.createElement('div');
            codeDiv.className = 'code-panel-code';
            const pre = document.createElement('pre');
            const code = document.createElement('code');
            code.className = `language-${codeBlock.language}`;
            code.textContent = codeBlock.code; // Use textContent to preserve formatting
            code.classList.add('code-preserve-format');
            pre.appendChild(code);
            codeDiv.appendChild(pre);
            codePanelContent.appendChild(codeDiv);
            
            // Highlight syntax
            if (typeof Prism !== 'undefined') {
                Prism.highlightAllUnder(codeDiv);
                // Re-apply formatting after Prism
                code.classList.add('code-preserve-format');
            }
        }
    }
    
    autoShowCodePanel(content) {
        // Check if content contains code blocks
        // More flexible regex: handles code blocks with or without newline after language
        const codeBlockRegex = /```(\w+)?\s*\n?([\s\S]*?)```/g;
        const matches = [...content.matchAll(codeBlockRegex)];
        
        if (matches.length > 0) {
            // Wait for DOM to be updated with code blocks
            setTimeout(() => {
                const codeWrappers = document.querySelectorAll('.code-block-wrapper');
                
                if (codeWrappers.length > 0) {
                    // Automatically add ALL code blocks to the panel
                    const codeBlocks = [];
                    codeWrappers.forEach((wrapper, index) => {
                        const codeId = wrapper.dataset.codeId;
                        const language = wrapper.dataset.language || 'text';
                        const codeElement = wrapper.querySelector('code');
                        
                        if (codeElement && codeId) {
                            codeBlocks.push({
                                id: codeId,
                                language: language,
                                code: codeElement.textContent,
                                title: `${language.toUpperCase()} Code ${index + 1}`
                            });
                        }
                    });
                    
                    // Show all code blocks in panel with tabs
                    if (codeBlocks.length > 0) {
                        this.showAllCodeInPanel(codeBlocks);
                    }
                } else {
                    // Fallback: extract from content directly
                    const codeBlocks = matches.map((match, index) => {
                        const language = match[1] || 'text';
                        const code = match[2].trim();
                        const codeId = 'code-' + Date.now() + '-' + index + '-' + Math.random().toString(36).substr(2, 9);
                        return {
                            id: codeId,
                            language: language,
                            code: code,
                            title: `${language.toUpperCase()} Code ${index + 1}`
                        };
                    });
                    this.showAllCodeInPanel(codeBlocks);
                }
            }, 300);
        }
    }
    
    showAllCodeInPanel(codeBlocks) {
        // Show code panel
        const codePanel = document.getElementById('codePanel');
        if (!codePanel || codeBlocks.length === 0) return;
        
        codePanel.classList.remove('hidden');
        
        // Update panel header
        const codePanelLanguage = document.getElementById('codePanelLanguage');
        const codePanelName = document.getElementById('codePanelName');
        
        if (codePanelLanguage) {
            if (codeBlocks.length === 1) {
                codePanelLanguage.textContent = codeBlocks[0].language.toUpperCase();
            } else {
                codePanelLanguage.textContent = `${codeBlocks.length} Files`;
            }
        }
        
        if (codePanelName) {
            codePanelName.textContent = codeBlocks.length === 1 ? 'Code' : 'Code Files';
        }
        
        // Create tabs if multiple code blocks
        const codePanelTabs = document.getElementById('codePanelTabs');
        const codePanelContent = document.getElementById('codePanelContent');
        
        if (!codePanelTabs || !codePanelContent) return;
        
        // Clear existing content
        codePanelTabs.innerHTML = '';
        codePanelContent.innerHTML = '';
        
        // Create tabs for multiple files
        if (codeBlocks.length > 1) {
            codeBlocks.forEach((block, index) => {
                const tab = document.createElement('div');
                tab.className = `code-panel-tab ${index === 0 ? 'active' : ''}`;
                tab.textContent = block.title;
                tab.dataset.codeId = block.id;
                tab.addEventListener('click', () => {
                    // Switch active tab
                    codePanelTabs.querySelectorAll('.code-panel-tab').forEach(t => t.classList.remove('active'));
                    tab.classList.add('active');
                    
                    // Show corresponding code
                    codePanelContent.querySelectorAll('.code-panel-code').forEach(c => {
                        c.style.display = c.dataset.codeId === block.id ? 'block' : 'none';
                    });
                });
                codePanelTabs.appendChild(tab);
            });
        }
        
        // Add all code blocks to content
        codeBlocks.forEach((block, index) => {
            const codeDiv = document.createElement('div');
            codeDiv.className = 'code-panel-code';
            codeDiv.dataset.codeId = block.id;
            codeDiv.style.display = index === 0 ? 'block' : (codeBlocks.length > 1 ? 'none' : 'block');
            
            const pre = document.createElement('pre');
            const code = document.createElement('code');
            code.className = `language-${block.language}`;
            code.textContent = block.code;
            code.classList.add('code-preserve-format');
            
            pre.appendChild(code);
            codeDiv.appendChild(pre);
            codePanelContent.appendChild(codeDiv);
            
            // Highlight syntax if Prism is available
            if (typeof Prism !== 'undefined') {
                Prism.highlightAllUnder(codeDiv);
                code.classList.add('code-preserve-format');
            }
        });
        
        // Update chat panel layout to show code panel
        const chatPanel = document.getElementById('chatPanel');
        if (chatPanel && !chatPanel.classList.contains('half')) {
            chatPanel.classList.remove('full');
            chatPanel.classList.add('half');
        }
    }

    formatTextOnly(text) {
        // Format text only (no code blocks - those are handled separately)
        let formatted = text;
        
        // Inline code (but not code blocks)
        formatted = formatted.replace(/`([^`\n]+)`/g, '<code>$1</code>');
        
        // Bold
        formatted = formatted.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // Italic
        formatted = formatted.replace(/\*(.+?)\*/g, '<em>$1</em>');
        
        // Line breaks
        formatted = formatted.replace(/\n/g, '<br>');
        
        return formatted;
    }
    
    formatMessage(content) {
        // This is now a legacy method - code blocks are handled in addMessage
        // But we keep it for backward compatibility
        return this.formatTextOnly(content);
    }

    escapeHtml(text) {
        // Escape HTML characters but preserve newlines
        // We need to escape HTML entities but keep newlines as-is
        return text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
        // Newlines are preserved as-is and will be respected by white-space: pre
    }

    showTyping() {
        this.typingIndicator.classList.add('visible', 'flex');
        this.scrollToBottom();
    }
    
    showLoadingSkeleton() {
        const skeleton = document.createElement('div');
        skeleton.className = 'message assistant';
        skeleton.innerHTML = `
            <div class="message-bubble">
                <div class="message-content">
                    <div class="skeleton message-skeleton"></div>
                </div>
            </div>
        `;
        this.messagesList.appendChild(skeleton);
        this.scrollToBottom();
        return skeleton;
    }
    
    removeLoadingSkeleton(skeleton) {
        if (skeleton && skeleton.parentNode) {
            skeleton.parentNode.removeChild(skeleton);
        }
    }

    hideTyping() {
        this.typingIndicator.classList.remove('visible', 'flex');
    }

    setInputEnabled(enabled) {
        this.messageInput.disabled = !enabled;
        this.sendButton.disabled = !enabled;
        const voiceButton = document.getElementById('voiceButton');
        if (voiceButton) {
            voiceButton.disabled = !enabled;
        }
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    async loadHistory() {
        try {
            const response = await api.getHistory();
            if (response.success && response.messages.length > 0) {
                // Hide welcome message
                if (this.welcomeMessage) {
                    this.welcomeMessage.style.display = 'none';
                }
                
                // Load messages
                response.messages.forEach(msg => {
                    if (msg.role === 'user' || msg.role === 'assistant') {
                        this.addMessage(msg.role, msg.content);
                    }
                });
                
                this.scrollToBottom();
            }
        } catch (error) {
            console.error('Error loading history:', error);
        }
    }

    async clearChat() {
        try {
            await api.clearHistory();
            this.messagesList.innerHTML = '';
            if (this.welcomeMessage) {
                this.welcomeMessage.classList.remove('hidden');
            }
            
            // Clear code blocks and hide code panel
            window.codeBlocks = [];
            const codePanel = document.getElementById('codePanel');
            if (codePanel) {
                codePanel.classList.add('hidden');
                const codePanelContent = document.getElementById('codePanelContent');
                codePanelContent.innerHTML = `
                    <div class="code-panel-empty">
                        <div class="code-panel-empty-icon">💻</div>
                        <p>No code to display</p>
                        <p class="code-panel-empty-hint">Code blocks will appear here when generated</p>
                    </div>
                `;
            }
            
            // Reset chat panel to full width
            const chatPanel = document.getElementById('chatPanel');
            if (chatPanel) {
                chatPanel.classList.remove('half');
                chatPanel.classList.add('full');
            }
        } catch (error) {
            console.error('Error clearing chat:', error);
        }
    }
}

// Export singleton instance
// Initialize chat controller after DOM is ready
let chat;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        chat = new ChatController();
        window.chat = chat; // Make available globally
    });
} else {
    chat = new ChatController();
    window.chat = chat; // Make available globally
}

