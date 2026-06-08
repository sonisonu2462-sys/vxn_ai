from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

# 🔐 API KEY (Render Environment Variable)
openai.api_key = os.environ.get("OPENAI_API_KEY")


# ---------------- HOME ----------------
@app.route("/")
def home():
    return "VXN AI Backend Running 🚀"


# ---------------- GENERATE ----------------
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        topic = data.get("topic", "")
        mode = data.get("mode", "study")

        # ---------------- MODES ----------------

        if mode == "study":
            prompt = f"""
You are a teacher.

Topic: {topic}

Give:
- Simple definition
- Key points
- Example
- Summary
"""

        elif mode == "ppt":
            prompt = f"""
Create PPT for students.

Topic: {topic}

6-7 slides:
Title + bullets
"""

        elif mode == "code":
            prompt = f"""
You are a coding teacher.

Topic: {topic}

Give:
1. Code
2. Explanation
3. Output
"""

        elif mode == "deep":
            prompt = f"""
Explain deeply:

Topic: {topic}

Include:
- Concept
- Details
- Applications
"""

        else:
            prompt = f"Explain {topic} simply"

        # ---------------- OPENAI CALL ----------------
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response["choices"][0]["message"]["content"]

        return jsonify({
            "result": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
