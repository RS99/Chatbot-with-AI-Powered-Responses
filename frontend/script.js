document.addEventListener("DOMContentLoaded", () => {
    const chatbox = document.getElementById("chatbox");
    chatbox.innerHTML += `<div class="message bot">Bot: Hello! How can I help you?</div>`;
});

// Toggle the upload menu when clicking "+"
function toggleUploadMenu() {
    const uploadMenu = document.getElementById("upload-menu");
    uploadMenu.classList.toggle("visible");
}

// Trigger file selection when clicking "Upload File"
function triggerFileInput() {
    document.getElementById("fileInput").click();
}

async function uploadFile() {
    const fileInput = document.getElementById("fileInput");
    if (fileInput.files.length === 0) {
        alert("Please select a file to upload.");
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:5000/api/upload", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if (data.file) {
        const chatbox = document.getElementById("chatbox");

        // Show uploaded file in chat
        chatbox.innerHTML += `<div class="message user">📄 Uploaded: <strong>${data.file}</strong></div>`;

        // If a summary is returned, display it
        if (data.summary) {
            chatbox.innerHTML += `<div class="message bot">📝 Summary: ${data.summary}</div>`;
        }

        chatbox.scrollTop = chatbox.scrollHeight;
    } else {
        alert(data.message);
    }
}


// Trigger file input when clicking upload button
function triggerFileInput() {
    document.getElementById("fileInput").click();
}


// Send message function (same as before)
async function sendMessage() {
    const inputField = document.getElementById("userInput");
    const message = inputField.value.trim();
    if (!message) return;

    const chatbox = document.getElementById("chatbox");

    // Add user message to chat
    chatbox.innerHTML += `<div class="message user">${message}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;

    // Show loading indicator
    const typingIndicator = document.createElement("div");
    typingIndicator.classList.add("message", "bot", "loading");
    typingIndicator.innerHTML = "⏳ Loading...";
    chatbox.appendChild(typingIndicator);
    chatbox.scrollTop = chatbox.scrollHeight;

    // Send request to backend
    const response = await fetch("http://127.0.0.1:5000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message })
    });

    const data = await response.json();
    typingIndicator.remove(); // Remove loading indicator

    // Display bot response
    chatbox.innerHTML += `<div class="message bot">${data.response}</div>`;
    chatbox.scrollTop = chatbox.scrollHeight;

    inputField.value = ""; // Clear input field
}

// Attach file input change event to upload file
document.getElementById("fileInput").addEventListener("change", uploadFile);
