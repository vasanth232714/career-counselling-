document.addEventListener("DOMContentLoaded", function() {
    const chatForm = document.getElementById('chat-form');
    const chatInputField = document.getElementById('chat-input-field');
    const chatHistory = document.querySelector('.chat-history');

    // Listen for the Enter key to send the message
    chatInputField.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();  // Prevent the default form submission
            sendMessage();  // Trigger the send message function
        }
    });

    // Listen for the send button click
    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the form from submitting the traditional way
        sendMessage();
    });

    function sendMessage() {
        const userInput = chatInputField.value.trim();

        if (userInput) {
            displayMessage('You', userInput, 'user-message');

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
                displayMessage('Bot', data, 'bot-message');
            })
            .catch(error => {
                console.error('Error:', error);
                displayMessage('Bot', 'Sorry, something went wrong.', 'bot-message');
            });

            // Clear input field
            chatInputField.value = '';
        }
    }

    function displayMessage(sender, message, className) {
        const messageElement = document.createElement('div');
        messageElement.classList.add(className);
        
        const profilePic = document.createElement('div');
        profilePic.classList.add('profile-pic');
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.innerText = `${sender}: ${message}`;

        messageElement.appendChild(profilePic);
        messageElement.appendChild(messageContent);

        chatHistory.appendChild(messageElement);
        chatHistory.scrollTop = chatHistory.scrollHeight;  // Scroll to the bottom
    }
});
