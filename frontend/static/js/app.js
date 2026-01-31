// AI Fashion Chatbot - Frontend JavaScript

class FashionChatbot {
    constructor() {
        this.userId = null;
        this.sessionId = null;
        this.initializeElements();
        this.attachEventListeners();
        this.loadAccessibilitySettings();
    }

    initializeElements() {
        // Chat elements
        this.chatMessages = document.getElementById('chatMessages');
        this.chatForm = document.getElementById('chatForm');
        this.messageInput = document.getElementById('messageInput');
        this.imageUpload = document.getElementById('imageUpload');
        this.uploadImageBtn = document.getElementById('uploadImageBtn');
        
        // Quick actions
        this.quickActionBtns = document.querySelectorAll('.quick-action-btn');
        
        // Try-on panel
        this.tryonPanel = document.getElementById('tryonPanel');
        this.uploadPhotoBtn = document.getElementById('uploadPhotoBtn');
        this.productUrlInput = document.getElementById('productUrlInput');
        this.processTryonBtn = document.getElementById('processTryonBtn');
        
        // Modals
        this.settingsModal = document.getElementById('settingsModal');
        this.privacyModal = document.getElementById('privacyModal');
        this.accessibilityModal = document.getElementById('accessibilityModal');
        
        // Modal buttons
        this.settingsBtn = document.getElementById('settingsBtn');
        this.privacyBtn = document.getElementById('privacyBtn');
        this.accessibilityBtn = document.getElementById('accessibilityBtn');
        
        // Settings form
        this.measurementsForm = document.getElementById('measurementsForm');
        
        // Privacy buttons
        this.exportDataBtn = document.getElementById('exportDataBtn');
        this.deleteDataBtn = document.getElementById('deleteDataBtn');
        
        // Accessibility settings
        this.fontSizeSelect = document.getElementById('fontSizeSelect');
        this.contrastToggle = document.getElementById('contrastToggle');
        this.screenReaderMode = document.getElementById('screenReaderMode');
        
        // Screen reader status
        this.srStatus = document.getElementById('srStatus');
    }

    attachEventListeners() {
        // Chat form
        this.chatForm.addEventListener('submit', (e) => this.handleSendMessage(e));
        
        // Image upload
        this.uploadImageBtn.addEventListener('click', () => this.imageUpload.click());
        this.imageUpload.addEventListener('change', (e) => this.handleImageUpload(e));
        
        // Quick actions
        this.quickActionBtns.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleQuickAction(e));
        });
        
        // Try-on panel
        if (this.uploadPhotoBtn) {
            this.uploadPhotoBtn.addEventListener('click', () => this.imageUpload.click());
        }
        if (this.processTryonBtn) {
            this.processTryonBtn.addEventListener('click', () => this.processTryOn());
        }
        
        // Modal triggers
        this.settingsBtn.addEventListener('click', () => this.openModal(this.settingsModal));
        this.privacyBtn.addEventListener('click', () => this.openModal(this.privacyModal));
        this.accessibilityBtn.addEventListener('click', () => this.openModal(this.accessibilityModal));
        
        // Close buttons
        document.querySelectorAll('.close-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                const panel = e.target.closest('.tryon-panel');
                if (modal) this.closeModal(modal);
                if (panel) panel.hidden = true;
            });
        });
        
        // Settings form
        if (this.measurementsForm) {
            this.measurementsForm.addEventListener('submit', (e) => this.saveMeasurements(e));
        }
        
        // Privacy actions
        if (this.exportDataBtn) {
            this.exportDataBtn.addEventListener('click', () => this.exportData());
        }
        if (this.deleteDataBtn) {
            this.deleteDataBtn.addEventListener('click', () => this.deleteData());
        }
        
        // Accessibility settings
        if (this.fontSizeSelect) {
            this.fontSizeSelect.addEventListener('change', (e) => this.changeFontSize(e.target.value));
        }
        if (this.contrastToggle) {
            this.contrastToggle.addEventListener('change', (e) => this.toggleHighContrast(e.target.checked));
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }

    async handleSendMessage(e) {
        e.preventDefault();
        
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        this.messageInput.value = '';
        
        // Show typing indicator
        const typingId = this.showTypingIndicator();
        
        try {
            // Send message to backend
            const response = await fetch('/api/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator(typingId);
            
            if (data.success) {
                // Add bot response
                this.addMessage(data.response, 'bot');
                
                // Handle suggestions
                if (data.suggestions && data.suggestions.length > 0) {
                    this.addSuggestions(data.suggestions);
                }
                
                // Handle actions
                if (data.action === 'request_tryon_input') {
                    this.showTryOnPanel();
                }
                
                // Announce to screen reader
                this.announceToScreenReader(`Bot responded: ${data.response}`);
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        } catch (error) {
            this.removeTypingIndicator(typingId);
            console.error('Error sending message:', error);
            this.addMessage('Sorry, I could not connect to the server. Please try again later.', 'bot');
        }
    }

    addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}-message`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = type === 'bot' ? '<i class="fas fa-robot"></i>' : '<i class="fas fa-user"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.textContent = text;
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(content);
        
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    addSuggestions(suggestions) {
        const suggestionDiv = document.createElement('div');
        suggestionDiv.className = 'message bot-message';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-lightbulb"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        
        const title = document.createElement('p');
        title.textContent = 'Quick suggestions:';
        title.style.fontWeight = '600';
        title.style.marginBottom = '0.5rem';
        content.appendChild(title);
        
        suggestions.forEach(suggestion => {
            const btn = document.createElement('button');
            btn.className = 'btn btn-secondary';
            btn.style.marginRight = '0.5rem';
            btn.style.marginBottom = '0.5rem';
            btn.textContent = suggestion;
            btn.onclick = () => {
                this.messageInput.value = suggestion;
                this.messageInput.focus();
            };
            content.appendChild(btn);
        });
        
        suggestionDiv.appendChild(avatar);
        suggestionDiv.appendChild(content);
        
        this.chatMessages.appendChild(suggestionDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showTypingIndicator() {
        const id = `typing-${Date.now()}`;
        const typingDiv = document.createElement('div');
        typingDiv.id = id;
        typingDiv.className = 'message bot-message';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = '<i class="fas fa-robot"></i>';
        
        const content = document.createElement('div');
        content.className = 'message-content';
        content.innerHTML = '<div class="loading"></div>';
        
        typingDiv.appendChild(avatar);
        typingDiv.appendChild(content);
        
        this.chatMessages.appendChild(typingDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        
        return id;
    }

    removeTypingIndicator(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    async handleImageUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('image', file);
        
        try {
            const response = await fetch('/api/tryon/upload-image', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage('Photo uploaded successfully! Now paste a product URL to try it on.', 'bot');
                this.userImagePath = data.file_path;
                this.announceToScreenReader('Photo uploaded successfully');
            } else {
                this.addMessage('Failed to upload photo. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Error uploading image:', error);
            this.addMessage('Error uploading photo. Please try again.', 'bot');
        }
    }

    handleQuickAction(e) {
        const action = e.currentTarget.dataset.action;
        
        const actionMessages = {
            'tryon': 'Try on clothes virtually',
            'size': 'Get size recommendations',
            'style': 'Get styling advice',
            'search': 'Find similar items'
        };
        
        const message = actionMessages[action] || action;
        this.messageInput.value = message;
        this.handleSendMessage(new Event('submit'));
    }

    showTryOnPanel() {
        if (this.tryonPanel) {
            this.tryonPanel.hidden = false;
        }
    }

    async processTryOn() {
        const productUrl = this.productUrlInput.value.trim();
        if (!productUrl) {
            alert('Please enter a product URL');
            return;
        }
        
        try {
            const response = await fetch('/api/tryon/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    product_url: productUrl,
                    user_image_path: this.userImagePath
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.addMessage('Virtual try-on complete! ' + data.fit_analysis.summary, 'bot');
                if (data.size_recommendation) {
                    this.addMessage(`Size recommendation: ${data.size_recommendation.recommended_size}`, 'bot');
                }
                this.announceToScreenReader('Virtual try-on complete');
            } else {
                this.addMessage('Failed to process try-on. Please try again.', 'bot');
            }
        } catch (error) {
            console.error('Error processing try-on:', error);
            this.addMessage('Error processing try-on. Please try again.', 'bot');
        }
    }

    openModal(modal) {
        if (modal) {
            modal.hidden = false;
            // Set focus to first focusable element
            const firstFocusable = modal.querySelector('button, input, select, textarea');
            if (firstFocusable) {
                firstFocusable.focus();
            }
        }
    }

    closeModal(modal) {
        if (modal) {
            modal.hidden = true;
        }
    }

    async saveMeasurements(e) {
        e.preventDefault();
        
        const height = document.getElementById('heightInput').value;
        const weight = document.getElementById('weightInput').value;
        const bodyType = document.getElementById('bodyTypeSelect').value;
        
        try {
            const response = await fetch('/api/user/measurements', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    height_cm: parseFloat(height),
                    weight_kg: parseFloat(weight),
                    body_type: bodyType
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert('Measurements saved successfully!');
                this.closeModal(this.settingsModal);
                this.announceToScreenReader('Measurements saved successfully');
            } else {
                alert('Failed to save measurements');
            }
        } catch (error) {
            console.error('Error saving measurements:', error);
            alert('Error saving measurements');
        }
    }

    async exportData() {
        try {
            const response = await fetch('/api/privacy/export-data');
            const data = await response.json();
            
            if (data.success) {
                // Download data as JSON
                const blob = new Blob([JSON.stringify(data.data, null, 2)], { type: 'application/json' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `fashion-chatbot-data-${new Date().toISOString()}.json`;
                a.click();
                URL.revokeObjectURL(url);
                
                this.announceToScreenReader('Data exported successfully');
            }
        } catch (error) {
            console.error('Error exporting data:', error);
            alert('Error exporting data');
        }
    }

    async deleteData() {
        if (!confirm('Are you sure you want to delete all your data? This action cannot be undone.')) {
            return;
        }
        
        try {
            const response = await fetch('/api/privacy/delete-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ data_type: 'all' })
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert('All data deleted successfully');
                this.closeModal(this.privacyModal);
                location.reload();
            }
        } catch (error) {
            console.error('Error deleting data:', error);
            alert('Error deleting data');
        }
    }

    changeFontSize(size) {
        document.body.classList.remove('font-large', 'font-x-large');
        if (size !== 'normal') {
            document.body.classList.add(`font-${size}`);
        }
        localStorage.setItem('fontSize', size);
        this.announceToScreenReader(`Font size changed to ${size}`);
    }

    toggleHighContrast(enabled) {
        if (enabled) {
            document.body.classList.add('high-contrast');
        } else {
            document.body.classList.remove('high-contrast');
        }
        localStorage.setItem('highContrast', enabled);
        this.announceToScreenReader(`High contrast mode ${enabled ? 'enabled' : 'disabled'}`);
    }

    loadAccessibilitySettings() {
        const fontSize = localStorage.getItem('fontSize');
        const highContrast = localStorage.getItem('highContrast') === 'true';
        
        if (fontSize && fontSize !== 'normal') {
            document.body.classList.add(`font-${fontSize}`);
            if (this.fontSizeSelect) {
                this.fontSizeSelect.value = fontSize;
            }
        }
        
        if (highContrast) {
            document.body.classList.add('high-contrast');
            if (this.contrastToggle) {
                this.contrastToggle.checked = true;
            }
        }
    }

    announceToScreenReader(message) {
        if (this.srStatus) {
            this.srStatus.textContent = message;
            setTimeout(() => {
                this.srStatus.textContent = '';
            }, 1000);
        }
    }

    handleKeyboardShortcuts(e) {
        // Alt+M: Focus message input
        if (e.altKey && e.key === 'm') {
            e.preventDefault();
            this.messageInput.focus();
        }
        
        // Alt+S: Open settings
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            this.openModal(this.settingsModal);
        }
        
        // Escape: Close modals
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal:not([hidden])').forEach(modal => {
                this.closeModal(modal);
            });
        }
    }
}

// Initialize the chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.fashionChatbot = new FashionChatbot();
});
