// Main JavaScript for PetroRAG application

document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const clearChatBtn = document.createElement('button');
    
    // Session ID for memory functionality - no longer used in stateless mode
    let currentSessionId = null;
    
    // Add clear chat button (hidden in stateless mode)
    clearChatBtn.textContent = 'Clear Chat';
    clearChatBtn.className = 'btn btn-secondary mt-2';
    clearChatBtn.style.display = 'none'; // Always hidden in stateless mode
    chatForm.parentNode.appendChild(clearChatBtn);
    
    // Handle clear chat button click - no longer used in stateless mode
    clearChatBtn.addEventListener('click', function() {
        // This functionality is disabled in stateless mode
        return;
    });

    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const query = userInput.value.trim();
        if (!query) return;
        
        // Add user message to chat
        addMessage(query, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Show loading spinner
        loadingSpinner.style.display = 'flex';
        
        // Prepare request body - no session ID in stateless mode
        const requestBody = { query: query };
        
        // Send query to API
        fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Server error: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            
            // Add bot response to chat
            if (data.error) {
                addMessage('Error: ' + data.error, 'bot');
            } else {
                addMessage(data.answer, 'bot');
            }
            
            // Scroll to bottom
            scrollToBottom();
        })
        .catch(error => {
            // Hide loading spinner
            loadingSpinner.style.display = 'none';
            
            // Add error message
            addMessage('Error: ' + error.message, 'bot');
            
            // Scroll to bottom
            scrollToBottom();
        });
    });

    // Function to add a message to the chat
    function addMessage(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'message user-message' : 
                              (sender === 'system' ? 'message system-message' : 'message bot-message');
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = message;
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        scrollToBottom();
    }

    // Function to scroll to the bottom of the chat
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}); 