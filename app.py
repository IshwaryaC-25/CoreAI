from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai
import os
from dotenv import load_dotenv

# =============================
# CONFIGURATION
# =============================
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

# =============================
# HTML TEMPLATE (Embedded)
# =============================
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>GyanGuru - AI ML Learning Assistant</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            background: #f4f6f9;
        }
        nav {
            background: #1e293b;
            color: white;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
        }
        nav a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
        }
        .container {
            padding: 40px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 8px;
            width: 450px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
        input, select, button {
            width: 100%;
            margin: 10px 0;
            padding: 10px;
        }
        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
            border-radius: 5px;
        }
        button:hover {
            background: #1d4ed8;
        }
        .result {
            margin-top: 30px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>

<nav>
    <h2>🧠 GyanGuru</h2>
    <div>AI Powered ML Learning Assistant</div>
</nav>

<div class="container">
    <div class="card">
        <h3>Generate ML Explanation</h3>
        <input type="text" id="topic" placeholder="Enter ML Topic (e.g. Neural Networks)">
        
        <select id="level">
            <option>Beginner</option>
            <option>Intermediate</option>
            <option>Advanced</option>
        </select>

        <button onclick="generateText()">Generate Explanation</button>
    </div>

    <div id="output" class="result"></div>
</div>

<script>
function generateText() {
    const topic = document.getElementById("topic").value;
    const level = document.getElementById("level").value;

    fetch("/generate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({topic: topic, level: level})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("output").innerText = data.result;
    });
}
</script>

</body>
</html>
"""

# =============================
# ROUTES
# =============================

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    topic = data.get("topic")
    level = data.get("level")

    prompt = f"""
    Explain {topic} in Machine Learning.
    Level: {level}.
    Include:
    - Definition
    - Key Concepts
    - Example
    """

    response = model.generate_content(prompt)
    return jsonify({"result": response.text})

# =============================
# RUN APP
# =============================
if __name__ == "__main__":
    app.run(debug=True)