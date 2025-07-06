# AI Notetaking Assistant

An AI-powered note-taking web application that lets you chat with a GPT-powered assistant and automatically save important parts of the conversation as organized notes.

## 🚀 Features

* **Chat with AI**

  Send messages to an OpenAI GPT-4.1-mini model and receive intelligent responses via the `/chat` endpoint .
* **Function-based note tools**
  
  The assistant can call functions like `save_note`, `delete_note`, `clear_notes`, `clear_chat`, and `export_notes` to manage your notes seamlessly .
* **Automatic note saving**
  
  Conversations are evaluated for “note-worthiness” and auto-saved using the `save_note` tool when appropriate .
* **Manual note management**
  
  Save the latest Q\&A as a note with a custom title, edit or delete notes right from the UI .
* **Search & sort**
  
  Real-time filtering, and toggle between Newest, Oldest, or Alphabetical sorting of notes .
* **Import/Export**
  
  Export all notes to JSON or import existing exports to merge into your collection .
* **Health check**
  
  Monitor backend status at `/health` .

## 🛠 Tech Stack

* **Frontend**:

  * Plain HTML/CSS/JavaScript (ES6)
  * [Marked.js](https://github.com/markedjs/marked) for Markdown rendering
  * LocalStorage for client-side persistence
* **Backend**:

  * Python 3.8+
  * [Flask](https://flask.palletsprojects.com/) & [flask-cors](https://github.com/corydolphin/flask-cors)
  * [python-dotenv](https://github.com/theskumar/python-dotenv) for environment vars
  * [OpenAI Python SDK](https://github.com/openai/openai-python)

## 📋 Prerequisites

* Python ≥3.8
* A valid OpenAI API key (set in `.env`)

## ⚙️ Setup

1. **Clone this repository**

   ```bash
   git clone https://github.com/your-username/ai-notetaking-assistant.git
   cd ai-notetaking-assistant
   ```

2. **Backend**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install flask flask-cors openai python-dotenv
   ```

   Create a `.env` file in the project root:

   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

   Run the server:

   ```bash
   python app.py
   ```

   The backend will start on `http://localhost:3001` and list available tools .

3. **Frontend**
   Simply serve the static HTML (or open directly in your browser). To avoid CORS/file-protocol issues, you can use Python’s simple HTTP server:

   ```bash
   python3 -m http.server 8000
   ```

   Then navigate to `http://localhost:8000/ai-notetaking-app.html` .

4. **Usage**

   * Enter your OpenAI API key in the sidebar and click “🔌 Connect API”
   * Chat with the assistant, save notes manually or let it auto-save
   * Search, sort, edit, delete, import, or export your notes

## 📂 File Structure

```
.
├── app.py                   # Flask backend with /chat, /notes, /health endpoints 
├── ai-notetaking-app.html   # Single-page frontend UI 
├── .env.example             # Example env file
├── requirements.txt         # (optional) pip dependencies
└── README.md                # This document
```

## 🔧 API Endpoints

* **POST** `/chat`
  Accepts `{ messages: [{ role, content }] }`, proxies to OpenAI with function-calling enabled, and returns either `{ message }` or `{ tool_used, tool_args }` .
* **GET** `/notes`
  Returns all notes in memory .
* **POST** `/notes`
  Add a manual note via JSON `{ title, content }` .
* **DELETE** `/notes/<note_id>`
  Remove a note by its index.
* **GET** `/health`
  Returns `{ status, notes_count, timestamp }` for monitoring .

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
