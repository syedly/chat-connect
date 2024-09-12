let deleteMessageId = null;

// Open the modal on delete button click
$('.delete-btn').on('click', function (e) {
    e.preventDefault();
    deleteMessageId = $(this).data('message-id');
    $('#deleteModal').modal('show');
});

// Handle the confirm delete action in the modal
$('#confirmDelete').on('click', function () {
    if (deleteMessageId) {
        $.ajax({
            url: `{% url 'delete-message' 0 %}`.replace('0', deleteMessageId),
            type: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}'  // Ensure CSRF token is included
            },
            success: function (response) {
                // Remove the message from the DOM if the delete is successful
                $(`div[data-message-id="${deleteMessageId}"]`).remove();
                // Close the modal
                $('#deleteModal').modal('hide');
            },
            error: function (error) {
                alert('Error deleting the message.');
            }
        });
    }
});

// WebSocket functionality for chat
const recipientId = "{{ recipient.id }}";
const chatSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/chat/' + recipientId + '/'
);

chatSocket.onopen = function() {
    console.log('WebSocket connection established');
};

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.sender && data.message) {
        const messageElement = document.createElement('div');
        messageElement.innerHTML = `<strong>${data.sender}:</strong> ${data.message}`;
        document.getElementById('chat-log').appendChild(messageElement);
        document.getElementById('chat-log').scrollTop = document.getElementById('chat-log').scrollHeight;
    }
};

chatSocket.onerror = function(e) {
    console.error('WebSocket error:', e);
};

chatSocket.onclose = function(e) {
    console.log('WebSocket connection closed:', e);
};

document.getElementById('send-button').onclick = function() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    if (message) {
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = '';
    }
};

document.getElementById('message-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        document.getElementById('send-button').click();
    }
});
