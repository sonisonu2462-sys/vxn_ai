from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# 🔐 API KEY from Render Environment Variables
openai.api_key = os.environ.get("OPENAI_API_KEY")


# ---------------- HOME ROUTE ----------------
@app.route("/")
def home():
    return "VXN AI is running successfully 🚀"


# ---------------- GENERATE ROUTE ----------------
@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json()

        topic = data.get("topic", "")
        mode = data.get("mode", "study")

        # ---------------- MODE PROMPTS ----------------

        if mode == "study":
            prompt = f"""
You are a professional teacher for Indian students.

Topic: {topic}

Create structured STUDY NOTES:
- Simple definition
- Key points in bullets
- Exam important points
- Real-life example
- Short revision summary
"""

        elif mode == "ppt":
            prompt = f"""
You are a PowerPoint expert.

Create a clean PPT for students.

Topic: {topic}

Rules:
- 6 to 8 slides
- Each slide: title + 3-4 bullets
- Simple English

Format:
Slide 1: Title
Slide 2: Introduction
Slide 3: Main Concept
Slide 4: Explanation
Slide 5: Examples
Slide 6: Uses
Slide 7: Conclusion
"""

        elif mode == "code":
            prompt = f"""
You are a coding teacher.

Topic: {topic}

Give:
1. Working code
2. Explanation
3. Output example
4. Common mistakes
"""

        elif mode == "deep":
            prompt = f"""
You are an advanced AI tutor.

Topic: {topic}

Give full deep explanation:
- Concept
- Step-by-step breakdown
- Real-life applications
- Viva questions
- Summary
"""

        else:
            prompt = f"Explain {topic} in simple terms"

        # ---------------- OPENAI CALL ----------------
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        result = response["choices"][0]["message"]["content"]

        return jsonify({
            "result": result,
            "mode": mode,
            "topic": topic
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
