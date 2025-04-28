document.addEventListener('DOMContentLoaded', () => {
    const chatHistory = document.getElementById('chat-history');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const executeButton = document.getElementById('execute-button');
    const statusMessage = document.getElementById('status-message');
    const newChatBtn = document.getElementById('new-chat-btn');
    const conversationList = document.getElementById('conversation-list');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    
    // Function to toggle sidebar
    function toggleSidebar() {
        sidebar.classList.toggle('collapsed');
        
        // Change button icon based on sidebar state
        if  (!sidebar.classList.contains('collapsed')) {
            sidebarToggle.innerHTML = '<i class="fas fa-bars"></i>';
            sidebarToggle.setAttribute('title', 'Hiện thanh bên');
        } else {
            sidebarToggle.innerHTML = '<i class="fas fa-expand"></i>';
            sidebarToggle.setAttribute('title', 'Ẩn thanh bên');
        }
        
        // Save sidebar state in localStorage
        localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
    }
    
    // Initialize sidebar state from localStorage
    if (localStorage.getItem('sidebarCollapsed') === 'true') {
        sidebar.classList.add('collapsed');
        sidebarToggle.innerHTML = '<i class="fas fa-expand"></i>';
        sidebarToggle.setAttribute('title', 'Hiện thanh bên');
    }
    
    // Add click event to sidebar toggle button
    sidebarToggle.addEventListener('click', toggleSidebar);

    // Function to add a message to the chat display
    function addMessage(type, content, simulateTyping = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type === 'user' ? 'user-message' : 'assistant-message');

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        
        // Format JSON code blocks
        content = content.replace(/```json\n([\s\S]*?)\n```/g, '\n<pre><code>$1</code></pre>\n');
        
        if (type === 'assistant' && simulateTyping) {
            // For assistant messages with typing simulation
            contentDiv.innerHTML = '';
            messageDiv.appendChild(contentDiv);
            chatHistory.appendChild(messageDiv);
            
            // Start the typing simulation
            simulateTypingEffect(contentDiv, content);
        } else {
            // For user messages or assistant messages without typing simulation
            contentDiv.innerHTML = content;
            messageDiv.appendChild(contentDiv);
            chatHistory.appendChild(messageDiv);
        }
        
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    // Function to simulate typing effect
    function simulateTypingEffect(element, text) {
        let index = 0;
        const speed = 2; // milliseconds per character
        
        // Process HTML tags
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = text;
        const textContent = tempDiv.textContent;
        
        // Function to handle HTML tags while typing
        function processTextWithTags() {
            if (index < text.length) {
                // Add one character at a time
                element.innerHTML = text.substring(0, index + 1);
                index++;
                
                // Calculate typing speed based on character (slower for punctuation)
                let currentSpeed = speed;
                const currentChar = text[index-1];
                if (['.', '!', '?', ',', ';', ':'].includes(currentChar)) {
                    currentSpeed = speed * 3; // Pause longer at punctuation
                }
                
                // Scroll to the bottom as text is typed
                chatHistory.scrollTop = chatHistory.scrollHeight;
                
                // Continue typing
                setTimeout(processTextWithTags, currentSpeed);
            }
        }
        
        // Start the typing effect
        processTextWithTags();
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('typing-indicator');
        typingDiv.id = 'typing-indicator';
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            typingDiv.appendChild(dot);
        }
        
        chatHistory.appendChild(typingDiv);
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    // Function to handle sending messages
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage('user', message);
        messageInput.value = '';
        sendButton.disabled = true;
        executeButton.style.display = 'none';
        
        // Show typing indicator
        showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            // Remove typing indicator before adding the response
            removeTypingIndicator();
            
            // Add assistant message to chat with typing simulation
            addMessage('assistant', data.response, true);

            // Show execute button if needed
            if (data.show_action_button) {
                executeButton.style.display = 'inline-block';
            } else {
                executeButton.style.display = 'none';
            }
            
            // Refresh conversation list after first message
            updateConversationList();

        } catch (error) {
            console.error('Error sending message:', error);
            removeTypingIndicator();
            // Also use typing simulation for error messages
            addMessage('assistant', `Lỗi: ${error.message}`, true);
        } finally {
            sendButton.disabled = false;
        }
    }

    // Function to handle execute action
    async function executeAction() {
        executeButton.disabled = true;
        statusMessage.textContent = 'Đang thực hiện...';

        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.success) {
                executeButton.style.display = 'none';
                // Apply typing simulation to successful execution messages
                addMessage('assistant', data.message, true);
            } else {
                // Apply typing simulation to error messages too
                addMessage('assistant', `Lỗi: ${data.message}`, true);
            }

        } catch (error) {
            console.error('Error executing action:', error);
            addMessage('assistant', `Lỗi thực hiện: ${error.message}`, true);
        } finally {
            executeButton.disabled = false;
            statusMessage.textContent = '';
        }
    }
    
    // Function to start a new conversation
    async function createNewConversation() {
        try {
            const response = await fetch('/new_conversation', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Clear chat history
                chatHistory.innerHTML = '';
                // Hide execute button
                executeButton.style.display = 'none';
                // Update conversation list
                updateConversationList();
                // Update chat ID in the UI
                document.getElementById('user-id').textContent = data.chat_id || '';
            }
            
        } catch (error) {
            console.error('Error creating new conversation:', error);
            statusMessage.textContent = `Lỗi: ${error.message}`;
        }
    }
    
    // Function to load a conversation
    async function loadConversation(chatId) {
        try {
            const response = await fetch(`/load_conversation/${chatId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Clear and reload chat history
                chatHistory.innerHTML = '';
                
                // Add all messages from the loaded conversation
                data.chat_history.forEach(message => {
                    addMessage(message.type, message.content);
                });
                
                // Hide execute button
                executeButton.style.display = 'none';
                
                // Update conversation list UI
                updateConversationList();
                
                // Update chat ID in the UI
                document.getElementById('user-id').textContent = chatId;
                
                // Update current conversation highlight
                document.querySelectorAll('.conversation-item').forEach(item => {
                    if (item.dataset.id === chatId) {
                        item.classList.add('current-conversation');
                    } else {
                        item.classList.remove('current-conversation');
                    }
                });
            }
            
        } catch (error) {
            console.error('Error loading conversation:', error);
            statusMessage.textContent = `Lỗi: ${error.message}`;
        }
    }
    
    // Function to delete a conversation
    async function deleteConversation(chatId) {
        if (!confirm('Bạn có chắc chắn muốn xóa cuộc hội thoại này không?')) {
            return;
        }
        
        try {
            const response = await fetch(`/delete_conversation/${chatId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                // If we deleted the current conversation, clear the chat history
                const currentChatId = document.getElementById('user-id').textContent;
                if (chatId === currentChatId) {
                    chatHistory.innerHTML = '';
                    executeButton.style.display = 'none';
                }
                
                // Update conversation list
                updateConversationList();
            } else {
                statusMessage.textContent = data.message;
            }
            
        } catch (error) {
            console.error('Error deleting conversation:', error);
            statusMessage.textContent = `Lỗi: ${error.message}`;
        }
    }
    
    // Function to update the conversation list
    async function updateConversationList() {
        try {
            const response = await fetch('/get_conversations', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            const currentChatId = document.getElementById('user-id').textContent;
            
            // Clear the current list
            conversationList.innerHTML = '';
            
            // Add all conversations to the list
            data.conversations.forEach(conv => {
                const timeStr = conv.updated_at ? formatDateTime(conv.updated_at) : 'Không rõ thời gian';
                
                const name = conv.conversation_name || 'Hội thoại không tên';
                const chatId = conv.chat_id || '';
                
                const itemDiv = document.createElement('div');
                itemDiv.classList.add('conversation-item');
                itemDiv.dataset.id = chatId;
                
                if (chatId === currentChatId) {
                    itemDiv.classList.add('current-conversation');
                }
                
                itemDiv.innerHTML = `
                    <span class="conversation-title">${chatId === currentChatId ? '🔵 ' : '📝 '}${name}</span>
                    <br>
                    <span class="conversation-time">${timeStr}</span>
                    <button class="delete-btn" data-id="${chatId}"><i class="fas fa-trash-alt"></i></button>
                `;
                
                conversationList.appendChild(itemDiv);
                
                // Add click event to load conversation
                itemDiv.addEventListener('click', function(e) {
                    // Don't load if clicked on delete button
                    if (e.target.classList.contains('delete-btn')) {
                        return;
                    }
                    loadConversation(chatId);
                });
                
                // Add click event to delete button
                itemDiv.querySelector('.delete-btn').addEventListener('click', function(e) {
                    e.stopPropagation();
                    deleteConversation(chatId);
                });
            });
            
        } catch (error) {
            console.error('Error updating conversation list:', error);
        }
    }

    // Function to format date and time
    function formatDateTime(dateString) {
        // Xử lý trực tiếp chuỗi ISO với múi giờ
        const d = new Date(dateString);
        // Format dd/mm/yyyy HH:MM
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const year = d.getFullYear();
        const hour = String(d.getHours()).padStart(2, '0');
        const minute = String(d.getMinutes()).padStart(2, '0');
        return `${day}/${month}/${year} ${hour}:${minute}`;
    }

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    executeButton.addEventListener('click', executeAction);
    
    newChatBtn.addEventListener('click', createNewConversation);
    
    // Initialize conversation item click events
    document.querySelectorAll('.conversation-item').forEach(item => {
        item.addEventListener('click', function(e) {
            if (!e.target.classList.contains('delete-btn')) {
                loadConversation(this.dataset.id);
            }
        });
    });
    
    // Initialize delete buttons
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation();
            deleteConversation(this.dataset.id);
        });
    });

    // Scroll to bottom on initial load
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    // Hide execute button on load
    executeButton.style.display = 'none';
});