from flask import Flask, render_template, request, jsonify
import json
import os
from utils.genai_utils import generate_text
from utils.code_utils import generate_code
from utils.audio_utils import generate_audio

app = Flask(__name__)

HISTORY_FILE = "storage/history.json"

def save_history(entry):
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)

    with open(HISTORY_FILE, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=4)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/history")
def history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as f:
            data = json.load(f)
    else:
        data = []
    return render_template("history.html", history=data)

@app.route("/generate-text", methods=["POST"])
def text():
    topic = request.json.get("topic")
    depth = request.json.get("depth")
    result = generate_text(f"Explain {topic} in {depth} level.")
    save_history({"type": "Text", "topic": topic})
    return jsonify({"result": result})

@app.route("/generate-code", methods=["POST"])
def code():
    topic = request.json.get("topic")
    result = generate_code(topic)
    save_history({"type": "Code", "topic": topic})
    return jsonify({"result": result})

@app.route("/generate-audio", methods=["POST"])
def audio():
    topic = request.json.get("topic")
    text = generate_text(f"Explain {topic} briefly.")
    file_path = generate_audio(text)
    save_history({"type": "Audio", "topic": topic})
    return jsonify({"audio_url": file_path})

if __name__ == "__main__":
    app.run(debug=True)