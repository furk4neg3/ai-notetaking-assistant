import os
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)
CORS(app)

# Global notes storage (unused by /chat now)
notes = []

# Define the available tools for GPT
tools = [
    {
      "name": "save_note",
      "description": "Save a new note with title and content",
      "parameters": {
        "type": "object",
        "properties": {
          "title":   { "type": "string", "description": "Short title for the note" },
          "content": { "type": "string", "description": "Content of the note" }
        },
        "required": ["title", "content"]
      }
    },
    {
      "name": "delete_note",
      "description": "Delete a note by its title or part of the title",
      "parameters": {
        "type": "object",
        "properties": {
          "title": { "type": "string", "description": "Title or a unique substring of the note to delete" }
        },
        "required": ["title"]
      }
    },
    {
      "name": "clear_notes",
      "description": "Delete all saved notes",
      "parameters": { "type": "object", "properties": { } }
    },
    {
      "name": "clear_chat",
      "description": "Clear the chat history",
      "parameters": { "type": "object", "properties": { } }
    },
    {
      "name": "export_notes",
      "description": "Export all notes",
      "parameters": { "type": "object", "properties": { } }
    }
]

@app.route("/chat", methods=["POST"])
def chat():
    # pull in the last N messages (including your system prompt)
    user_messages = request.json["messages"]

    # load your key and init client
    api_key = os.getenv("OPENAI_API_KEY")
    client  = openai.OpenAI(api_key=api_key)

    # let the model decide if it needs to call a function
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=user_messages,
        functions=tools,          # ← your flattened list
        function_call="auto",
        temperature=0.7,
        max_tokens=1000
    )

    message = response.choices[0].message

    # if it chose to invoke a function, forward name+args to the frontend
    if getattr(message, "function_call", None):
        fn = message.function_call
        return jsonify({
            "tool_used": fn.name,
            "tool_args": json.loads(fn.arguments)
        })

    # otherwise just return the assistant’s text
    return jsonify({ "message": message.content })

@app.route("/notes", methods=["GET"])
def get_notes():
    """Get all notes"""
    return jsonify({"notes": notes})

@app.route("/notes", methods=["POST"])
def add_note():
    """Manually add a note"""
    global notes
    data = request.json

    note = {
        "title": data.get("title", "Untitled"),
        "content": data.get("content", ""),
        "timestamp": datetime.now().isoformat(),
        "type": "manual"
    }

    notes.insert(0, note)
    return jsonify({"message": "Note added", "notes": notes})

@app.route("/notes/<int:note_id>", methods=["DELETE"])
def delete_note_by_id(note_id):
    """Delete a note by index"""
    global notes
    if 0 <= note_id < len(notes):
        deleted = notes.pop(note_id)
        return jsonify({"message": f"Deleted note: {deleted['title']}", "notes": notes})
    else:
        return jsonify({"error": "Note not found"}), 404

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "notes_count": len(notes),
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🚀 Starting AI Notetaking Backend...")
    print("📝 Server running on http://localhost:3001")
    print("🔧 Tools available:", [tool["name"] for tool in tools])
    app.run(host='localhost', port=3001, debug=True)