document.addEventListener("DOMContentLoaded", () => {
    const chatContainer = document.getElementById("chat-container");
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");

    function appendMessage(text) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("chat-message");
        messageDiv.textContent = text;
        chatContainer.insertBefore(messageDiv, chatContainer.firstChild);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    sendButton.addEventListener("click", () => {
        const messageText = messageInput.value.trim();
        if (messageText !== "") {
            appendMessage(messageText);
            messageInput.value = "";
        }
    });

    messageInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            sendButton.click();
        }
    });

    // Initial scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;
});