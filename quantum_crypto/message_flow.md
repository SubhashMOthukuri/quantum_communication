# Message Flow in Quantum Secure Chat

## 1. User Sends Message

When a user (Alice or Bob) clicks the send button, the following happens:

```javascript
function sendMessage(sender) {
  // 1. Get message from input field
  const messageInput = document.getElementById(`${sender}Message`);
  const message = messageInput.value.trim();

  // 2. Show message in sender's chat immediately
  const chatId = `${sender}-chat`;
  const chat = document.getElementById(chatId);

  // 3. Create message element
  const messageDiv = document.createElement("div");
  messageDiv.className = "message sent";
  messageDiv.innerHTML = `
        <div class="message-content">
            <div class="message-text">${message}</div>
        </div>
    `;

  // 4. Add message to sender's chat
  chat.appendChild(messageDiv);
  chat.scrollTop = chat.scrollHeight;

  // 5. Clear input field
  messageInput.value = "";

  // 6. Generate encryption details
  const quantumKey = Math.random().toString(36).substring(2, 15);
  const encryptedMessage = Math.random().toString(36).substring(2, 15);

  // 7. Send message to server via Socket.IO
  socket.emit("message", {
    message: message,
    sender: sender,
    eve_enabled: eveEnabled,
    quantum_key: quantumKey,
    encrypted_message: encryptedMessage,
  });
}
```

## 2. Server Receives Message

The server receives the message through Socket.IO and broadcasts it to all connected clients.

## 3. Message Handling on Receiver's Side

When the message is received, the following happens:

```javascript
function handleMessage(data) {
  // 1. Determine which chat to show the message in
  const sender = data.sender;
  const message = data.message;
  const chatId = sender === "alice" ? "bob-chat" : "alice-chat";
  const chat = document.getElementById(chatId);

  // 2. Create message element
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${sender === "alice" ? "received" : "sent"}`;

  // 3. Create message content with encryption details
  let messageContent = `
        <div class="message-content">
            <div class="message-text">${message}</div>
            ${
              eveEnabled
                ? `
                <div class="encryption-details">
                    <div class="key-info">Key: ${
                      data.quantum_key || "Generated Key"
                    }</div>
                    <div class="encrypted-info">Encrypted: ${
                      data.encrypted_message || "Encrypted Message"
                    }</div>
                    <div class="eve-warning">⚠️ Someone is intercepting your message!</div>
                </div>
            `
                : `
                <div class="encryption-details">
                    <div class="key-info">Key: ${
                      data.quantum_key || "Generated Key"
                    }</div>
                    <div class="encrypted-info">Encrypted: ${
                      data.encrypted_message || "Encrypted Message"
                    }</div>
                </div>
            `
            }
        </div>
    `;

  // 4. Add message to receiver's chat
  messageDiv.innerHTML = messageContent;
  chat.appendChild(messageDiv);
  chat.scrollTop = chat.scrollHeight;
}
```

## Flow Summary:

1. User types message and clicks send
2. Message appears immediately in sender's chat
3. Input field is cleared
4. Random encryption details are generated
5. Message is sent to server via Socket.IO
6. Server broadcasts message to all clients
7. Receiver's chat displays message with:
   - Original message text
   - Quantum key
   - Encrypted message
   - Eve warning (if Eve is enabled)

## Eve Detection:

- If Eve is enabled (eveEnabled = true):
  - The connection line turns red
  - The Eve control button turns red
  - Each message shows a warning about interception
- If Eve is disabled (eveEnabled = false):
  - The connection line remains white
  - The Eve control button remains white
  - Messages show only encryption details without warnings
