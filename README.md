# Chatbot-with-AI-Powered-Responses

## Overview
This project is a chatbot application that integrates AI-powered text responses, Wikipedia summaries, and file upload functionalities. The backend is built using Flask (Python), while the frontend is a responsive web interface powered by HTML, CSS, and JavaScript.

## Features
- **AI-Powered Chatbot**: Uses GPT-2 to generate intelligent responses.
- **Mathematical Solver**: Can solve algebraic and geometric equations.
- **Wikipedia Integration**: Fetches summarized Wikipedia content.
- **File Upload & Summarization**: Users can upload `.pdf`, `.txt`, and `.md` files to get an automatic summary.
- **User-Friendly Interface**: Modern UI with real-time chat interactions.
- **Dual Backend**: Flask-based AI processing with a Node.js server for status checks.

## Tech Stack
### Frontend
- **HTML, CSS, JavaScript**: Creates an interactive and user-friendly chat interface.

### Backend
- **Flask (Python)**: Handles chat logic, AI integration, and file processing.
- **Node.js**: Runs a status-checking server.
- **Transformers (Hugging Face)**: GPT-2 text generation model.
- **Wikipedia API**: Fetches knowledge-based responses.
- **NLTK**: Text processing and tokenization.
- **SymPy**: Solves mathematical equations.
- **BeautifulSoup**: HTML parsing for clean responses.
- **PyMuPDF**: Extracts text from PDF files.

## Installation & Setup
### 1. Clone the Repository
```sh
 git clone https://github.com/your-username/chatbot-ai.git
 cd chatbot-ai
```

### 2. Install Python Dependencies
Make sure you have Python installed, then install the required packages:
```sh
 pip install flask flask-cors wikipedia nltk transformers beautifulsoup4 sympy pymupdf
```

### 3. Install Node.js Dependencies
Ensure Node.js is installed, then run:
```sh
 npm install
```

### 4. Run the Application
Start the Flask backend:
```sh
 python app.py
```

Start the Node.js status server:
```sh
 node server.js
```

Open a browser and visit:
```
http://127.0.0.1:5000/
```

## File Structure
```
├── backend/
│   ├── app.py          # Flask AI backend
    ├── server.js           # Node.js status checker
├── frontend/
│   ├── index.html      # Chat UI
│   ├── styles.css      # Chat styling
│   ├── script.js       # Handles chat interactions
├── knowledge_db.json   # Sample knowledge base
├── README.md           # Documentation
```

## API Endpoints
### 1. Chat with AI
```http
POST /api/chat
```
**Request Body:**
```json
{
    "message": "What is a black hole?"
}
```
**Response:**
```json
{
    "response": "A black hole is a region of spacetime where gravity is so strong that nothing, not even light, can escape it."
}
```

### 2. File Upload & Summarization
```http
POST /api/upload
```
**Request:** Multipart form-data with a file.
**Response:** JSON object containing the file summary.

### 3. Check Server Status
```http
GET /api/status
```
**Response:**
```json
{
    "status": "ready"
}
```

## Contributing
Pull requests are welcome! If you’d like to contribute, please fork the repository and create a new branch.

## License
This project is licensed under the MIT License.

---
### Author: Your Name
GitHub: [RS99](https://github.com//RS99)

