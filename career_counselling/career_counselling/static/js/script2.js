document.getElementById('chat-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from refreshing the page

    const userInput = document.getElementById('user-input').value.trim();
    if (userInput) {
        addMessage('You', userInput, 'user-message');
        
        // Send user input to the Flask backend via POST request
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `user_input=${encodeURIComponent(userInput)}`
        })
        .then(response => response.text())
        .then(data => {
            // Add bot's response to the chat
            addMessage('Bot', data, 'bot-message');
        });

        // Clear input field
        document.getElementById('user-input').value = '';
    }
});

function addMessage(sender, message, className) {
    const chatBox = document.getElementById('chat-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', className);
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to the bottom
}
