/**
 * Research Canvas Controller
 * Manages the research canvas panel for displaying comprehensive research results
 */
class ResearchCanvasController {
    constructor() {
        this.canvas = document.getElementById('researchCanvas');
        this.content = document.getElementById('researchCanvasContent');
        this.queryElement = document.getElementById('researchCanvasQuery');
        this.currentQuery = '';
        this.currentResearch = null;
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Close button
        const closeBtn = document.getElementById('researchCanvasClose');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.hide());
        }
        
        // Fullscreen button
        const fullscreenBtn = document.getElementById('researchCanvasFullscreen');
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => this.toggleFullscreen());
        }
        
        // Export button
        const exportBtn = document.getElementById('researchCanvasExport');
        if (exportBtn) {
            exportBtn.addEventListener('click', () => this.exportResearch());
        }
    }
    
    show(query, researchData) {
        if (!this.canvas) return;
        
        this.currentQuery = query;
        this.currentResearch = researchData;
        
        // Update query display
        if (this.queryElement) {
            this.queryElement.textContent = `"${query}"`;
        }
        
        // Display research content
        this.displayResearch(researchData);
        
        // Show canvas
        this.canvas.classList.remove('hidden');
        
        // Adjust chat panel
        const chatPanel = document.getElementById('chatPanel');
        if (chatPanel) {
            chatPanel.classList.remove('full');
            chatPanel.classList.add('half');
        }
        
        // Hide code panel if open
        const codePanel = document.getElementById('codePanel');
        if (codePanel && !codePanel.classList.contains('hidden')) {
            codePanel.classList.add('hidden');
        }
    }
    
    hide() {
        if (!this.canvas) return;
        
        this.canvas.classList.add('hidden');
        
        // Restore chat panel
        const chatPanel = document.getElementById('chatPanel');
        if (chatPanel) {
            chatPanel.classList.remove('half');
            chatPanel.classList.add('full');
        }
    }
    
    displayResearch(researchData) {
        if (!this.content) return;
        
        // Clear existing content
        this.content.innerHTML = '';
        
        if (!researchData || !researchData.content) {
            this.content.innerHTML = `
                <div class="research-canvas-empty">
                    <div class="research-canvas-empty-icon">🔬</div>
                    <p>No research data available</p>
                </div>
            `;
            return;
        }
        
        // Create research document
        const researchDoc = document.createElement('div');
        researchDoc.className = 'research-document';
        
        // Overview section
        if (researchData.overview) {
            const overviewSection = this.createSection('Overview', researchData.overview);
            researchDoc.appendChild(overviewSection);
        }
        
        // Key Points section
        if (researchData.keyPoints && researchData.keyPoints.length > 0) {
            const keyPointsSection = this.createKeyPointsSection(researchData.keyPoints);
            researchDoc.appendChild(keyPointsSection);
        }
        
        // Main content
        if (researchData.content) {
            const contentSection = this.createSection('Detailed Analysis', researchData.content);
            researchDoc.appendChild(contentSection);
        }
        
        // Sources section
        if (researchData.sources && researchData.sources.length > 0) {
            const sourcesSection = this.createSourcesSection(researchData.sources);
            researchDoc.appendChild(sourcesSection);
        }
        
        // Additional sections
        if (researchData.additionalInfo) {
            const additionalSection = this.createSection('Additional Information', researchData.additionalInfo);
            researchDoc.appendChild(additionalSection);
        }
        
        this.content.appendChild(researchDoc);
        
        // Scroll to top
        this.content.scrollTop = 0;
    }
    
    createSection(title, content) {
        const section = document.createElement('div');
        section.className = 'research-section';
        
        const titleEl = document.createElement('h2');
        titleEl.className = 'research-section-title';
        titleEl.textContent = title;
        section.appendChild(titleEl);
        
        const contentEl = document.createElement('div');
        contentEl.className = 'research-section-content';
        
        // Format content (markdown-like)
        contentEl.innerHTML = this.formatContent(content);
        
        section.appendChild(contentEl);
        
        return section;
    }
    
    createKeyPointsSection(keyPoints) {
        const section = document.createElement('div');
        section.className = 'research-section';
        
        const titleEl = document.createElement('h2');
        titleEl.className = 'research-section-title';
        titleEl.textContent = 'Key Points';
        section.appendChild(titleEl);
        
        const listEl = document.createElement('ul');
        listEl.className = 'research-key-points';
        
        keyPoints.forEach(point => {
            const li = document.createElement('li');
            li.innerHTML = this.formatContent(point);
            listEl.appendChild(li);
        });
        
        section.appendChild(listEl);
        
        return section;
    }
    
    createSourcesSection(sources) {
        const section = document.createElement('div');
        section.className = 'research-section';
        
        const titleEl = document.createElement('h2');
        titleEl.className = 'research-section-title';
        titleEl.textContent = 'Sources';
        section.appendChild(titleEl);
        
        const sourcesList = document.createElement('div');
        sourcesList.className = 'research-sources';
        
        sources.forEach((source, index) => {
            const sourceEl = document.createElement('div');
            sourceEl.className = 'research-source';
            
            const sourceTitle = document.createElement('div');
            sourceTitle.className = 'research-source-title';
            sourceTitle.textContent = source.title || `Source ${index + 1}`;
            sourceEl.appendChild(sourceTitle);
            
            if (source.url) {
                const sourceLink = document.createElement('a');
                sourceLink.href = source.url;
                sourceLink.target = '_blank';
                sourceLink.rel = 'noopener noreferrer';
                sourceLink.className = 'research-source-link';
                sourceLink.textContent = source.url;
                sourceEl.appendChild(sourceLink);
            }
            
            if (source.description) {
                const sourceDesc = document.createElement('div');
                sourceDesc.className = 'research-source-description';
                sourceDesc.textContent = source.description;
                sourceEl.appendChild(sourceDesc);
            }
            
            sourcesList.appendChild(sourceEl);
        });
        
        section.appendChild(sourcesList);
        
        return section;
    }
    
    formatContent(content) {
        if (typeof content !== 'string') {
            content = String(content);
        }
        
        // Convert markdown-like formatting
        // Bold
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        // Italic
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        // Code
        content = content.replace(/`(.*?)`/g, '<code>$1</code>');
        // Links
        content = content.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>');
        // Line breaks
        content = content.replace(/\n\n/g, '</p><p>');
        content = content.replace(/\n/g, '<br>');
        
        // Wrap in paragraph if not already wrapped
        if (!content.startsWith('<p>')) {
            content = '<p>' + content + '</p>';
        }
        
        return content;
    }
    
    toggleFullscreen() {
        if (!this.canvas) return;
        
        if (this.canvas.classList.contains('fullscreen')) {
            this.canvas.classList.remove('fullscreen');
        } else {
            this.canvas.classList.add('fullscreen');
        }
    }
    
    exportResearch() {
        if (!this.currentResearch) return;
        
        // Create export data
        const exportData = {
            query: this.currentQuery,
            timestamp: new Date().toISOString(),
            research: this.currentResearch
        };
        
        // Convert to JSON
        const jsonData = JSON.stringify(exportData, null, 2);
        
        // Create blob and download
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `research_${this.currentQuery.replace(/[^a-z0-9]/gi, '_')}_${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

// Initialize research canvas controller
let researchCanvas;
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        researchCanvas = new ResearchCanvasController();
    });
} else {
    researchCanvas = new ResearchCanvasController();
}

